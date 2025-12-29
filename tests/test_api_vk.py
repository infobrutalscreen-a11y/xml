from fastapi.testclient import TestClient
from api import app, API_KEY

client = TestClient(app)


def test_api_vk_convert_goods_csv():
    with open("tests/fixtures/products.csv", "rb") as f:
        r = client.post(
            "/api/v1/convert/vk",
            files={"file": ("products.csv", f, "text/csv")},
            data={"vk_category": "goods", "output_format": "csv"},
            headers={"X-API-Key": API_KEY}
        )
    assert r.status_code == 200
    assert "attachment" in r.headers.get("content-disposition", "")
    assert "id,title,price" in r.text


def test_api_vk_convert_auto_xml():
    with open("tests/fixtures/auto.csv", "rb") as f:
        r = client.post(
            "/api/v1/convert/vk",
            files={"file": ("auto.csv", f, "text/csv")},
            data={"vk_category": "auto", "output_format": "xml"},
            headers={"X-API-Key": API_KEY}
        )
    assert r.status_code == 200
    assert r.headers.get("content-type", "").startswith("application/xml")
    assert "<Items>" in r.text
