from formats.vk.vk_validators import validate_vk_category, validate_goods, validate_auto


def test_validate_goods_empty():
    assert validate_goods([]) == []


def test_validate_goods_missing_fields():
    items = [{"id": "1", "title": "", "price": ""}]
    warnings = validate_goods(items)
    assert any("missing required field" in w for w in warnings)


def test_validate_auto_year_price():
    items = [{"id": "1", "title": "Car", "price": "2000", "year": "2020"}, {"id": "2", "title": "Car2", "price": "notnum", "year": "twenty"}]
    w = validate_auto(items)
    assert any("price looks non-numeric" in x for x in w)
    assert any("year looks invalid" in x for x in w)


def test_validate_vk_category_unknown():
    assert validate_vk_category("unknown", [{"a": "b"}]) == []
