from formats.parser import parse_bytes_by_format
from formats.vk.vk_goods import format_vk_goods


def test_goods_end_to_end_csv_and_xml():
    b = open("tests/fixtures/products.csv", "rb").read()
    rows = parse_bytes_by_format(b, "csv")

    csv_out = format_vk_goods(rows, output_format="csv")
    assert "id,title,price" in csv_out

    tsv_out = format_vk_goods(rows, output_format="tsv")
    assert "id\t" in tsv_out

    xml_out = format_vk_goods(rows, output_format="xml")
    assert "<Items>" in xml_out and "<Item>" in xml_out
