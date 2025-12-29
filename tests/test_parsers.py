from formats.parser import parse_bytes_by_format


def test_parse_csv_products():
    b = open("tests/fixtures/products.csv", "rb").read()
    rows = parse_bytes_by_format(b, "csv")
    assert isinstance(rows, list)
    assert len(rows) == 1
    r = rows[0]
    assert r.get("id") == "0"
    assert "Худи VK" in r.get("title")


def test_parse_csv_auto():
    b = open("tests/fixtures/auto.csv", "rb").read()
    rows = parse_bytes_by_format(b, "csv")
    assert isinstance(rows, list)
    assert len(rows) == 1
    r = rows[0]
    assert r.get("id") == "K456653443"
    assert r.get("brand") == "Москвич"

