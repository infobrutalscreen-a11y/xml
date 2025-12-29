from formats.parser import parse_bytes_by_format, parse_yaml_bytes


def test_parse_yaml_list_and_dict():
    yml_list = b"- id: 1\n  title: Item 1\n- id: 2\n  title: Item 2\n"
    rows = parse_yaml_bytes(yml_list)
    assert isinstance(rows, list)
    assert len(rows) == 2

    yml_dict_wrap = b"root:\n  - id: 3\n    title: Item 3\n"
    rows2 = parse_yaml_bytes(yml_dict_wrap)
    assert isinstance(rows2, list)
    assert len(rows2) == 1


def test_parse_csv_bom_and_headers():
    b = "\ufeffid,title\n1,Товар\n".encode("utf-8")
    rows = parse_bytes_by_format(b, "csv")
    assert rows[0]["id"] == "1"
    assert rows[0]["title"] == "Товар"


def test_xml_tag_helper():
    from formats.vk.vk_helpers import xml_tag
    assert xml_tag("location.country") == "location_country"
    assert xml_tag("123field") == "_123field"
    assert xml_tag("name with spaces") == "name_with_spaces"