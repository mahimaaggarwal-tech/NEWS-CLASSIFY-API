from fastapi import FastAPI
from app.api.api_v1.endpoints.news import router as news_router
from app.core.config import settings
from app.db.session import engine
from sqlalchemy.orm import sessionmaker
from app.core.celery import celery_app
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()  # This will also output to the console
    ]
)
# Initialize FastAPI app
app = FastAPI()

# Include the news API router
app.include_router(news_router, prefix="/api/v1", tags=["news"])

# Database setup
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    # Startup logic such as establishing database connections
    print("Starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    # Shutdown logic such as closing database connections
    print("Shutting down...")

# Example route
@app.get("/")
async def read_root():
    return {"message": "Welcome to the News Classifier API"}

# Example Celery task route
@app.post("/api/start-collection")
async def start_collection(url: str):
    """
    Trigger background task for collecting news articles.
    """
    # Trigger Celery task for collecting and classifying news articles
    task = celery_app.send_task("app.business.news_service.collect_news", args=[url])
    return {"job_id": task.id}

@app.get("/api/poll-results/{job_id}")
async def poll_results(job_id: str):
    """
    Poll results from the task.
    """
    # Implement task status checking logic
    return {"job_id": job_id, "status": "pending"}  # Example response

@app.get("/api/retrieve-news/{topic}")
async def retrieve_news(topic: str):
    """
    Retrieve news articles by topic.
    """
    # Implement logic to retrieve news items based on the topic
    return {"topic": topic, "news_items": []}  # Example response
