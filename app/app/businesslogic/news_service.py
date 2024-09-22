import uuid  # For generating unique job IDs
import feedparser
import requests
import logging
from app.db.news_items import NewsItem
from app.db.job_status import JobStatus  # Import the JobStatus model
from app.businesslogic.news_classifier import NewsClassificationModel
from sqlalchemy.orm import Session
from typing import List
from requests.exceptions import RequestException
from fastapi import HTTPException  # For handling HTTP exceptions

# Configure logging
logger = logging.getLogger(__name__)

class NewsService:
    def __init__(self, db: Session):
        self.db = db
        self.classifier = NewsClassificationModel(model_path="app/models")
        self.classifier.load_model()

    def parse_rss_feed(self, rss_url: str) -> List[dict]:
        """
        Parse the RSS feed from the given URL and extract relevant data for classification.
        :param rss_url: URL of the RSS feed
        :return: List of news items with title, description, and publication date
        """
        try:
            logger.info(f"Fetching RSS feed from {rss_url}")
            response = requests.get(rss_url)
            response.raise_for_status()  # Raise an error for bad responses
        except RequestException as e:
            logger.error(f"Failed to fetch RSS feed: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Failed to fetch RSS feed: {str(e)}")

        feed = feedparser.parse(response.content)
        news_items = []
        # Limit to top 50 articles
        for entry in feed.entries[:50]:  # Get only the top 50 entries
            title = entry.title
            description = entry.description
            pub_date = entry.published if 'published' in entry else "No Publish Date"

            if title and description:
                logger.info(f"Found article: {title}")
                news_items.append({
                    "title": title,
                    "description": description,
                    "pub_date": pub_date
                })

        logger.info(f"Parsed {len(news_items)} articles from the feed.")
        return news_items

    def classify_and_store(self, articles: List[dict]):
        """
        Classifies and stores news articles in the database.
        """
        for article in articles:
            # Combine title and description for classification
            logger.info(f"Classifying article: {article['title']}")
            category = self.classifier.predict([f"{article['title']} {article['description']}"])[0]

            # Handle publication date
            pub_date = article['pub_date'] if article['pub_date'] != "No Publish Date" else None

            # Store classified news in the database
            news_item = NewsItem(
                title=article['title'],
                description=article['description'],
                link='No Link',  # Update as needed
                category=category,
                pub_date=pub_date  # Use the processed pub_date
            )
            self.db.add(news_item)
            logger.info(f"Stored article: {article['title']} in the database with category: {category}")

        self.db.commit()  # Commit all at once after storing all articles
        logger.info(f"Stored {len(articles)} articles in the database.")

    def collect_and_classify_news(self, rss_url: str) -> str:
        """
        Initiates the process of collecting and classifying news from the RSS feed URL.
        Generates and returns a unique job ID.
        """
        job_id = str(uuid.uuid4())
        job_status = JobStatus(job_id=job_id, status="Processing")
        self.db.add(job_status)  # Store initial job status in the database
        self.db.commit()  # Commit to save job status

        logger.info(f"Started job {job_id} for RSS URL: {rss_url}")

        try:
            articles = self.parse_rss_feed(rss_url)
            self.classify_and_store(articles)
            job_status.status = "Completed"
            logger.info(f"Completed job {job_id}.")
        except Exception as e:
            job_status.status = f"Failed: {str(e)}"
            logger.error(f"Job {job_id} failed: {str(e)}")
        finally:
            self.db.commit()  # Commit job status update

        return job_id

    def check_job_status(self, job_id: str):
        """
        Check job status from the database.
        Returns job status if found, otherwise raises an HTTP exception.
        """
        status = self.db.query(JobStatus).filter(JobStatus.job_id == job_id).first()
        
        if status is None:
            logger.warning(f"Job ID {job_id} not found.")
            raise HTTPException(status_code=404, detail="Job ID not found")
        
        logger.info(f"Job ID {job_id} status: {status.status}")
        return {"job_id": job_id, "status": status.status}

    def get_news_by_topic(self, topic: str):
        """
        Retrieves classified news articles by topic.
        """
        news_items = self.db.query(NewsItem).filter(NewsItem.category == topic).all()
        logger.info(f"Retrieved {len(news_items)} articles for topic: {topic}")
        return [item.to_dict() for item in news_items] or []  # Return an empty list if no items found
