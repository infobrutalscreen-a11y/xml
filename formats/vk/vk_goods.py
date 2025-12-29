import csv
from io import StringIO
from typing import List, Dict

from formats.vk.vk_helpers import safe_get

VK_GOODS_HEADERS = [
    "id","title","price","link","image_link","brand","availability",
    "description","condition","google_product_category","sale_price",
    "gender","age_group"
]


def parse_input(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    items = []
    for row in data:
        item = {}
        item["id"] = safe_get(row, ["id", "ID"], "")
        item["title"] = safe_get(row, ["title", "name"], "")
        item["price"] = safe_get(row, ["price", "cost"], "")
        item["link"] = safe_get(row, ["link", "url"], "")
        item["image_link"] = safe_get(row, ["image_link", "image"], "")
        item["brand"] = safe_get(row, ["brand"], "")
        item["availability"] = safe_get(row, ["availability"], "")
        item["description"] = safe_get(row, ["description", "descr"], "")
        item["condition"] = safe_get(row, ["condition"], "")
        item["google_product_category"] = safe_get(row, ["google_product_category"], "")
        item["sale_price"] = safe_get(row, ["sale_price"], "")
        item["gender"] = safe_get(row, ["gender"], "")
        item["age_group"] = safe_get(row, ["age_group"], "")

        items.append(item)
    return items


def render_csv(items: List[dict]) -> str:
    output = StringIO()
    writer = csv.writer(output, delimiter=",")
    writer.writerow(VK_GOODS_HEADERS)
    for i in items:
        writer.writerow([i.get(h, "") for h in VK_GOODS_HEADERS])
    return output.getvalue()


def render_tsv(items: List[dict]) -> str:
    output = StringIO()
    writer = csv.writer(output, delimiter="\t")
    writer.writerow(VK_GOODS_HEADERS)
    for i in items:
        writer.writerow([i.get(h, "") for h in VK_GOODS_HEADERS])
    return output.getvalue()


def render_xml(items: List[dict]) -> str:
    import xml.etree.ElementTree as ET

    root = ET.Element("Items")
    for item in items:
        el = ET.SubElement(root, "Item")
        for field in VK_GOODS_HEADERS:
            child = ET.SubElement(el, field)
            child.text = str(item.get(field, "")) or ""
    return ET.tostring(root, encoding="utf-8").decode("utf-8")


def format_vk_goods(data: List[dict], output_format: str = "csv") -> str:
    items = parse_input(data)
    if output_format == "csv":
        return render_csv(items)
    if output_format == "tsv":
        return render_tsv(items)
    if output_format == "xml":
        return render_xml(items)
    raise ValueError(f"Unsupported VK output format: {output_format}")
