import asyncio
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

async def send_requests(feed_url):
    response = client.post("/api/v1/start-collection/", json={"rss_url": feed_url})
    return response.json()

def test_concurrent_requests():
    feed_urls = [
        "https://www.aljazeera.com/xml/rss/all.xml",
        "http://feeds.bbci.co.uk/news/world/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
    ]

    # Use asyncio to send requests concurrently
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(asyncio.gather(*(send_requests(url) for url in feed_urls)))

    for result in results:
        assert "job_id" in result  # Ensure each response has a job_id
