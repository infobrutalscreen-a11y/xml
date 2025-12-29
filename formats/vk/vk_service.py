import csv
from io import StringIO
from typing import List, Dict

from formats.vk.vk_helpers import safe_get

VK_SERVICE_HEADERS = [
    "id","title","price","link","image_link","brand","worker_type",
    "description","location.address","location.locality",
    "location.region","location.country","metro.name","min_price",
    "max_price","product_type","rating","reviews_count","custom_label"
]


def parse_input(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    items = []
    for row in data:
        item = {}
        item["id"] = safe_get(row, ["id","ID"], "")
        item["title"] = safe_get(row, ["title","name"], "")
        item["price"] = safe_get(row, ["price"], "")
        item["link"] = safe_get(row, ["link","url"], "")
        item["image_link"] = safe_get(row, ["image_link","image"], "")
        item["brand"] = safe_get(row, ["brand"], "")
        item["worker_type"] = safe_get(row, ["worker_type"], "")
        item["description"] = safe_get(row, ["description","descr"], "")
        item["location.address"] = safe_get(row, ["location.address","address"], "")
        item["location.locality"] = safe_get(row, ["location.locality","locality"], "")
        item["location.region"] = safe_get(row, ["location.region","region"], "")
        item["location.country"] = safe_get(row, ["location.country","country"], "")
        item["metro.name"] = safe_get(row, ["metro.name"], "")
        item["min_price"] = safe_get(row, ["min_price"], "")
        item["max_price"] = safe_get(row, ["max_price"], "")
        item["product_type"] = safe_get(row, ["product_type"], "")
        item["rating"] = safe_get(row, ["rating"], "")
        item["reviews_count"] = safe_get(row, ["reviews_count"], "")
        item["custom_label"] = safe_get(row, ["custom_label"], "")
        items.append(item)
    return items


def render_csv(items: List[dict]) -> str:
    output = StringIO()
    writer = csv.writer(output, delimiter=",")
    writer.writerow(VK_SERVICE_HEADERS)
    for i in items:
        writer.writerow([i.get(h, "") for h in VK_SERVICE_HEADERS])
    return output.getvalue()

def render_tsv(items: List[dict]) -> str:
    output = StringIO()
    writer = csv.writer(output, delimiter="\t")
    writer.writerow(VK_SERVICE_HEADERS)
    for i in items:
        writer.writerow([i.get(h, "") for h in VK_SERVICE_HEADERS])
    return output.getvalue()

def format_vk_service(data: List[dict], output_format: str = "csv") -> str:
    items = parse_input(data)
    if output_format == "csv":
        return render_csv(items)
    if output_format == "tsv":
        return render_tsv(items)
    raise ValueError(f"Unsupported VK output format: {output_format}")
