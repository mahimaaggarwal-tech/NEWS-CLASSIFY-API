import concurrent.futures
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
valid_topic = "sci.space"  # Example topic for concurrent retrieval

def retrieve_news_by_topic():
    response = client.get(f"/api/v1/news/{valid_topic}")
    assert response.status_code == 200
    news_items = response.json()
    assert isinstance(news_items, list)
    for item in news_items:
        assert "title" in item
        assert "description" in item
        assert "category" in item
        assert item["category"] == valid_topic

def test_concurrent_retrieve_news():
    # Test concurrent retrievals
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(retrieve_news_by_topic) for _ in range(10)]
        for future in concurrent.futures.as_completed(futures):
            future.result()  # Will raise any exceptions encountered in the threads
