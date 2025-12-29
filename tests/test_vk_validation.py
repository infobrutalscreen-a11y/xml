from fastapi.testclient import TestClient
from api import app, API_KEY

client = TestClient(app)


def test_vk_goods_validation_json():
    # missing price in the fixture
    content = b"id,title\n1,Item without price\n"
    r = client.post(
        "/api/v1/convert/vk/json",
        files={"file": ("goods.csv", content, "text/csv")},
        data={"vk_category": "goods", "output_format": "csv"},
        headers={"X-API-Key": API_KEY}
    )
    assert r.status_code == 200
    body = r.json()
    assert "warnings" in body
    assert len(body["warnings"]) >= 1


def test_vk_goods_validation_headers():
    # missing price
    content = b"id,title\n1,Item without price\n"
    r = client.post(
        "/api/v1/convert/vk",
        files={"file": ("goods.csv", content, "text/csv")},
        data={"vk_category": "goods", "output_format": "csv"},
        headers={"X-API-Key": API_KEY}
    )
    assert r.status_code == 200
    assert r.headers.get("X-Validation-Warnings") == "1"
    assert "row 1: missing required field 'price'" in r.headers.get("X-Validation-First", "")
