from fastapi.testclient import TestClient
from app.main import app
import logging

logger = logging.getLogger(__name__)

client = TestClient(app)

# List of dynamic RSS feed URLs
rss_feed_urls = [
    "https://www.aljazeera.com/xml/rss/all.xml",
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
]

# List of all categories from the 20 Newsgroups dataset
valid_categories = [
    "alt.atheism",
    "comp.graphics",
    "comp.os.ms-windows.misc",
    "comp.sys.ibm.pc.hardware",
    "comp.sys.mac.hardware",
    "comp.windows.x",
    "misc.forsale",
    "rec.autos",
    "rec.motorcycles",
    "rec.sport.baseball",
    "rec.sport.hockey",
    "sci.crypt",
    "sci.electronics",
    "sci.med",
    "sci.space",
    "soc.religion.christian",
    "talk.politics.guns",
    "talk.politics.mideast",
    "talk.politics.misc",
    "talk.religion.misc"
]

def test_start_collection():
    job_ids = []  # Store job IDs for later use
    for feed_url in rss_feed_urls:
        response = client.post("/api/v1/start-collection/", json={"rss_url": feed_url})
        
        assert response.status_code == 200
        assert "job_id" in response.json()
        
        job_ids.append(response.json()["job_id"])  # Store job ID

    return job_ids  # Return all job IDs for further tests

def test_retrieve_news_by_topic():
    job_ids = test_start_collection()  # Start collecting articles

    # Now retrieve news specifically by the topic 'sci.space'
    topic = "sci.space"
    response = client.get(f"/api/v1/news/{topic}")
    assert response.status_code == 200
    news_items = response.json()
    
    assert isinstance(news_items, list)  # Ensure response is a list
    for item in news_items:
        assert "title" in item  # Each item should have a title
        assert "description" in item  # Each item should have a description
        assert "category" in item  # Each item should have a category
        assert item["category"] == topic  # Ensure the item is from the correct topic


def test_start_collection_invalid_url():
    # Test with an invalid RSS feed URL
    response = client.post("/api/v1/start-collection/", json={"rss_url": "invalid_url"})
    assert response.status_code == 400  # Expect a Bad Request error (status 400)

def test_retrieve_news_by_topic_no_articles():
    # Test retrieving news by a topic with no articles
    topic = "NonexistentTopic"  # Use a topic that has no articles
    response = client.get(f"/api/v1/news/{topic}")
    assert response.status_code == 200
    news_items = response.json()
    assert isinstance(news_items, list)
    assert len(news_items) == 0  # Should return an empty list

def test_classification_model():
    sample_news = [
        {
            "title": "What are swing states, and why are they critical?",
            "description": "A handful of US states play an outsized role in deciding presidential elections.",
            "category": "talk.politics.misc"
        },
        {
            "title": "Murdered Uganda Olympian Rebecca Cheptegei’s funeral march begins in Kenya",
            "description": "Activists join march as Cheptegei's body begins its final journey.",
            "category": "talk.politics.mideast"
        }
    ]
    
    for news_item in sample_news:
        assert news_item["category"] in valid_categories, "Unexpected category in classification"
