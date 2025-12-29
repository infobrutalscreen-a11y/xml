from fastapi.testclient import TestClient
from api import app, API_KEY

client = TestClient(app)


def test_api_vk_avia_xml():
    with open("tests/fixtures/avia.csv", "rb") as f:
        r = client.post(
            "/api/v1/convert/vk",
            files={"file": ("avia.csv", f, "text/csv")},
            data={"vk_category": "avia", "output_format": "xml"},
            headers={"X-API-Key": API_KEY}
        )
    assert r.status_code == 200
    assert r.headers.get("content-type", "").startswith("application/xml")
    assert "<Items>" in r.text


def test_api_vk_estate_xml():
    with open("tests/fixtures/estate.csv", "rb") as f:
        r = client.post(
            "/api/v1/convert/vk",
            files={"file": ("estate.csv", f, "text/csv")},
            data={"vk_category": "estate", "output_format": "xml"},
            headers={"X-API-Key": API_KEY}
        )
    assert r.status_code == 200
    assert r.headers.get("content-type", "").startswith("application/xml")
    assert "<Items>" in r.text


def test_api_vk_hotel_xml():
    with open("tests/fixtures/hotel.csv", "rb") as f:
        r = client.post(
            "/api/v1/convert/vk",
            files={"file": ("hotel.csv", f, "text/csv")},
            data={"vk_category": "hotel", "output_format": "xml"},
            headers={"X-API-Key": API_KEY}
        )
    assert r.status_code == 200
    assert r.headers.get("content-type", "").startswith("application/xml")
    assert "<Items>" in r.text


def test_api_vk_service_xml():
    with open("tests/fixtures/service.csv", "rb") as f:
        r = client.post(
            "/api/v1/convert/vk",
            files={"file": ("service.csv", f, "text/csv")},
            data={"vk_category": "service", "output_format": "xml"},
            headers={"X-API-Key": API_KEY}
        )
    assert r.status_code == 200
    assert r.headers.get("content-type", "").startswith("application/xml")
    assert "<Items>" in r.text
