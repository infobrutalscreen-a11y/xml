from formats.vk.vk_validators import validate_goods, validate_auto


def test_validate_goods_nonstring_price_and_none():
    items = [
        {"id": 1, "title": "Item1", "price": 100},
        {"id": "2", "title": "Item2", "price": None},
    ]
    # should not raise and should report missing/ok appropriately
    w = validate_goods(items)
    assert isinstance(w, list)
    assert any("missing required field 'price'" in msg for msg in w) or any("price looks non-numeric" in msg for msg in w)


def test_validate_auto_nonstring_year_price():
    items = [
        {"id": 1, "title": "C1", "price": 2000, "year": 2020},
        {"id": 2, "title": "C2", "price": "nope", "year": None},
    ]
    w = validate_auto(items)
    assert isinstance(w, list)
    assert any("price looks non-numeric" in msg for msg in w) or any("year looks invalid" in msg for msg in w)
