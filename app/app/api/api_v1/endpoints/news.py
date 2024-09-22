import uuid  # Import uuid for generating unique job IDs
import logging  # Import logging for debugging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.businesslogic.news_service import NewsService
from pydantic import BaseModel

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RSSUrlRequest(BaseModel):
    rss_url: str

def get_news_service(db: Session = Depends(get_db)) -> NewsService:
    return NewsService(db=db)

@router.post("/start-collection", summary="Start news collection")
def start_collection(request: RSSUrlRequest, service: NewsService = Depends(get_news_service)):
    logger.info(f"Received request to start collection for URL: {request.rss_url}")
    
    if not request.rss_url.startswith("http"):
        logger.error(f"Invalid URL format: {request.rss_url}")
        raise HTTPException(status_code=400, detail="Invalid URL format")
    
    job_id = service.collect_and_classify_news(request.rss_url)
    logger.info(f"Started news collection. Job ID: {job_id}")
    
    return {"job_id": job_id, "message": "News collection started"}

@router.get("/poll-results/{job_id}", summary="Check job status")
def poll_results(job_id: str, service: NewsService = Depends(get_news_service)):
    logger.info(f"Polling results for Job ID: {job_id}")
    
    status = service.check_job_status(job_id)
    
    if status is None:
        logger.warning(f"Job ID {job_id} not found.")
        raise HTTPException(status_code=404, detail="Job not found")
    
    logger.info(f"Job ID {job_id} status: {status}")
    return {"job_id": job_id, "status": status}

@router.get("/news/{topic}", summary="Get news by topic")
def get_news_by_topic(topic: str, service: NewsService = Depends(get_news_service)):
    logger.info(f"Retrieving news for topic: {topic}")
    
    news_items = service.get_news_by_topic(topic)
    
    if not news_items:
        logger.info(f"No news items found for topic: {topic}")
    
    return news_items  # Return the list even if empty, no need for a 404
