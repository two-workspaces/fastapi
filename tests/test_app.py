from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_docs():
    assert client.get("/docs").status_code == 200
    assert client.get("/openapi.json").json()["info"]["title"]


def test_items_crud():
    r = client.post("/items", json={"name": "Coffee", "price": 3.5, "tags": ["drink"]})
    assert r.status_code == 201
    item = r.json()
    assert client.get(f"/items/{item['id']}").json()["name"] == "Coffee"
    r = client.put(f"/items/{item['id']}", json={"name": "Tea", "price": 2})
    assert r.json()["name"] == "Tea"
    assert client.delete(f"/items/{item['id']}").status_code == 204
    assert client.get(f"/items/{item['id']}").status_code == 404


def test_validation():
    r = client.post("/items", json={"name": "", "price": -1})
    assert r.status_code == 422
