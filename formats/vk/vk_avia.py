import csv
from io import StringIO
from typing import List, Dict

from formats.vk.vk_helpers import safe_get

VK_AVIA_HEADERS = [
    "ID","Destination ID","Origin ID","Destination name",
    "Origin name","Flight description","Image URL","Final URL",
    "Flight price","Sale Price"
]


def parse_input(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    items = []
    for row in data:
        item = {}
        item["ID"] = safe_get(row, ["id", "ID"], "")
        item["Destination ID"] = safe_get(row, ["Destination ID","dest_id","destination_id"], "")
        item["Origin ID"] = safe_get(row, ["Origin ID","orig_id","origin_id"], "")
        item["Destination name"] = safe_get(row, ["Destination name","destination"], "")
        item["Origin name"] = safe_get(row, ["Origin name","origin"], "")
        item["Flight description"] = safe_get(row, ["Flight description","description"], "")
        item["Image URL"] = safe_get(row, ["image","image_link"], "")
        item["Final URL"] = safe_get(row, ["link","final_url"], "")
        item["Flight price"] = safe_get(row, ["Flight price","price"], "")
        item["Sale Price"] = safe_get(row, ["Sale Price","sale_price"], "")
        items.append(item)
    return items


def render_csv(items: List[dict]) -> str:
    output = StringIO()
    writer = csv.writer(output, delimiter=",")
    writer.writerow(VK_AVIA_HEADERS)
    for i in items:
        writer.writerow([i.get(h, "") for h in VK_AVIA_HEADERS])
    return output.getvalue()


def render_tsv(items: List[dict]) -> str:
    output = StringIO()
    writer = csv.writer(output, delimiter="\t")
    writer.writerow(VK_AVIA_HEADERS)
    for i in items:
        writer.writerow([i.get(h, "") for h in VK_AVIA_HEADERS])
    return output.getvalue()


def render_xml(items: List[dict]) -> str:
    import xml.etree.ElementTree as ET
    from formats.vk.vk_helpers import xml_tag

    root = ET.Element("Items")
    for item in items:
        el = ET.SubElement(root, "Item")
        for field in VK_AVIA_HEADERS:
            child = ET.SubElement(el, xml_tag(field))
            child.text = str(item.get(field, "")) or ""
    return ET.tostring(root, encoding="utf-8").decode("utf-8")


def format_vk_avia(data: List[dict], output_format: str = "csv") -> str:
    items = parse_input(data)
    if output_format == "csv":
        return render_csv(items)
    if output_format == "tsv":
        return render_tsv(items)
    if output_format == "xml":
        return render_xml(items)
    raise ValueError(f"Unsupported VK output format: {output_format}")
