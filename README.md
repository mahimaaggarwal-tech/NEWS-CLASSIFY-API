# News Collection API

A FastAPI-based application for collecting and classifying news articles from various RSS feeds. The application retrieves articles, classifies them into predefined categories, and provides an API for accessing the collected data.

## Features

- Start the collection of top 50 articles from specified RSS feed URLs.
- Retrieve news articles categorized by topics.
- Poll for the status of ongoing collection jobs.
- Handle invalid RSS feed URLs gracefully.
- Return an empty list for topics with no articles.
- capable of handling concurrent requests

## Technologies Used

- FastAPI: framework for building APIs.
- HTTPX: For making HTTP requests.
- scikit-learn: For news classification.
- Celery: Handles background tasks for concurrent news collection requests.
- Redis: Acts as the message broker for Celery tasks.
- SQLAlchemy: ORM used for database interactions.
- PostgreSQL: Database to store collected and classified news articles.
- Docker: For containerization and ease of deployment.
- pytest: For testing the API functionality.

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your machine.

### Running the Application

1. Clone the repository:

   ```bash
   git clone https://github.com/mahima1321/NEWS-CLASSIFY-API.git
   cd NEWS-CLASSIFY-API

2. Build and run the application using Docker Compose:
    docker compose up --build
    
    
3. Access the API at http://localhost:8000

API Endpoints
- Start Collection

    POST /api/v1/start-collection/
    Request Body: { "rss_url": "<RSS feed URL>" }
    Response: { "job_id": "<unique job identifier>" }
- Retrieve News by Topic

    GET /api/v1/news/{topic}
    Response: List of news articles under the specified topic.
- Poll Results

    GET /api/v1/poll-results/{job_id}
    Response: Status and results of the specified job.

4. Running Tests
To run the tests, execute the following command: up --build
    docker compose run tests

5. Documentation
Find System_Design_Document.md and Test_Plan_Document.md in the docs folder

The output will indicate the success or failure of the tests.

Warnings
During testing, you may see some warnings related to deprecations or version inconsistencies. These can typically be ignored but should be addressed in future updates.


