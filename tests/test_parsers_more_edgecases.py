from formats.parser import parse_bytes_by_format


def test_malformed_csv_inconsistent_columns():
    b = b"id,title,price\n1,One,100\n2,Two\n3,Three,300,extra\n"
    rows = parse_bytes_by_format(b, "csv")
    # should get three rows; extra columns are ignored, missing fields become ''
    assert len(rows) == 3
    assert rows[1].get("price", "") == ""


def test_multiple_validation_warnings():
    # two rows missing required fields
    content = b"id,title\n1,\n,NoID\n"
    r = None
    from fastapi.testclient import TestClient
    from api import app, API_KEY
    client = TestClient(app)

    r = client.post(
        "/api/v1/convert/vk/json",
        files={"file": ("goods.csv", content, "text/csv")},
        data={"vk_category": "goods", "output_format": "csv"},
        headers={"X-API-Key": API_KEY}
    )
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body.get("warnings"), list)
    assert len(body["warnings"]) >= 2
