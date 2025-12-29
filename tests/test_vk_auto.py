from formats.parser import parse_bytes_by_format
from formats.vk.vk_auto import format_vk_auto


def test_auto_end_to_end_csv_and_xml():
    b = open("tests/fixtures/auto.csv", "rb").read()
    rows = parse_bytes_by_format(b, "csv")

    csv_out = format_vk_auto(rows, output_format="csv")
    assert "id,title,link" in csv_out

    tsv_out = format_vk_auto(rows, output_format="tsv")
    assert "id\t" in tsv_out

    xml_out = format_vk_auto(rows, output_format="xml")
    assert "<Items>" in xml_out and "<Item>" in xml_out
