from typing import List, Dict
from xml.etree import ElementTree as ET
from formats.vk.vk_helpers import safe_get, extract_text

VK_AUTO_HEADERS = [
    "id", "title", "link", "brand", "model", "image_link", "price",
    "description", "availability", "condition", "state_of_vehicle", "year",
    "exterior_color", "mileage.value", "mileage.unit", "body_style",
    "vin", "sale_price", "min_price", "max_price", "custom_label",
    "vehicle_type", "location.address", "location.country",
    "location.region", "location.locality", "metro.name"
]

def parse_input(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Приводим входные данные в общую JSON‑структуру.
    data — список dict от XML/CSV/TSV/YML
    """
    items = []
    for row in data:
        item = {}
        item["id"] = safe_get(row, ["id", "ID", "Id"], "")
        item["title"] = safe_get(row, ["title", "name"], "")
        item["link"] = safe_get(row, ["link", "url"], "")
        item["brand"] = safe_get(row, ["brand", "make"], "")
        item["model"] = safe_get(row, ["model", "series", "modification"], "")
        item["image_link"] = safe_get(row, ["image_link", "picture", "image"], "")
        item["price"] = safe_get(row, ["price", "cost"], "")
        item["description"] = safe_get(row, ["description", "descr"], "")

        # дополнительные поля
        item["availability"] = safe_get(row, ["availability"], "")
        item["condition"] = safe_get(row, ["condition"], "")
        item["state_of_vehicle"] = safe_get(row, ["state_of_vehicle"], "")
        item["year"] = safe_get(row, ["year"], "")
        item["exterior_color"] = safe_get(row, ["exterior_color"], "")
        item["mileage.value"] = safe_get(row, ["mileage.value", "mileage"], "")
        item["mileage.unit"] = safe_get(row, ["mileage.unit"], "")
        item["body_style"] = safe_get(row, ["body_style"], "")
        item["vin"] = safe_get(row, ["vin"], "")
        item["sale_price"] = safe_get(row, ["sale_price"], "")
        item["min_price"] = safe_get(row, ["min_price"], "")
        item["max_price"] = safe_get(row, ["max_price"], "")
        item["custom_label"] = safe_get(row, ["custom_label"], "")
        item["vehicle_type"] = safe_get(row, ["vehicle_type"], "")
        item["location.address"] = safe_get(row, ["location.address", "address"], "")
        item["location.country"] = safe_get(row, ["location.country"], "")
        item["location.region"] = safe_get(row, ["location.region"], "")
        item["location.locality"] = safe_get(row, ["location.locality", "city"], "")
        item["metro.name"] = safe_get(row, ["metro.name"], "")

        items.append(item)
    return items

def render_csv(items: List[dict]) -> str:
    """
    Renderer -> CSV
    """
    import csv
    from io import StringIO

    output = StringIO()
    writer = csv.writer(output, delimiter=",")
    writer.writerow(VK_AUTO_HEADERS)
    for item in items:
        writer.writerow([item.get(h, "") for h in VK_AUTO_HEADERS])
    return output.getvalue()

def render_tsv(items: List[dict]) -> str:
    import csv
    from io import StringIO

    output = StringIO()
    writer = csv.writer(output, delimiter="\t")
    writer.writerow(VK_AUTO_HEADERS)
    for item in items:
        writer.writerow([item.get(h, "") for h in VK_AUTO_HEADERS])
    return output.getvalue()

def render_xml(items: List[dict]) -> str:
    """
    Renderer -> XML
    """
    root = ET.Element("Items")
    for item in items:
        el = ET.SubElement(root, "Item")
        for field in VK_AUTO_HEADERS:
            child = ET.SubElement(el, field.replace(".", "_"))
            child.text = str(item.get(field, "")) or ""
    return ET.tostring(root, encoding="utf-8").decode("utf-8")


def format_vk_auto(data: List[dict], output_format: str = "csv") -> str:
    """
    data — это список словарей, полученный из парсера входного файла
    output_format — "csv", "tsv" или "xml"
    """
    items = parse_input(data)

    if output_format == "csv":
        return render_csv(items)
    if output_format == "tsv":
        return render_tsv(items)
    if output_format == "xml":
        return render_xml(items)

    raise ValueError(f"Unsupported VK output format: {output_format}")
