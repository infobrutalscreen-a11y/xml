import csv
from io import StringIO
from typing import List, Dict

from formats.vk.vk_helpers import safe_get

VK_ESTATE_HEADERS = [
    "id","title","address","location.country","location.region",
    "location.locality","price","image_link","link","brand",
    "metro.name","sale_price","min_price","max_price","description",
    "num_rooms","floor","floors_total","property_type","custom_label",
    "listing_type","area_size","area_unit","year","availability"
]


def parse_input(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    items = []
    for row in data:
        item = {}
        item["id"] = safe_get(row, ["id","ID"], "")
        item["title"] = safe_get(row, ["title","name"], "")
        item["address"] = safe_get(row, ["address","location.address"], "")
        item["location.country"] = safe_get(row, ["location.country","country"], "")
        item["location.region"] = safe_get(row, ["location.region","region"], "")
        item["location.locality"] = safe_get(row, ["location.locality","city"], "")
        item["price"] = safe_get(row, ["price"], "")
        item["image_link"] = safe_get(row, ["image_link","image"], "")
        item["link"] = safe_get(row, ["link","url"], "")
        item["brand"] = safe_get(row, ["brand"], "")
        item["metro.name"] = safe_get(row, ["metro.name"], "")
        item["sale_price"] = safe_get(row, ["sale_price"], "")
        item["min_price"] = safe_get(row, ["min_price"], "")
        item["max_price"] = safe_get(row, ["max_price"], "")
        item["description"] = safe_get(row, ["description","descr"], "")
        item["num_rooms"] = safe_get(row, ["num_rooms"], "")
        item["floor"] = safe_get(row, ["floor"], "")
        item["floors_total"] = safe_get(row, ["floors_total"], "")
        item["property_type"] = safe_get(row, ["property_type"], "")
        item["custom_label"] = safe_get(row, ["custom_label"], "")
        item["listing_type"] = safe_get(row, ["listing_type"], "")
        item["area_size"] = safe_get(row, ["area_size"], "")
        item["area_unit"] = safe_get(row, ["area_unit"], "")
        item["year"] = safe_get(row, ["year"], "")
        item["availability"] = safe_get(row, ["availability"], "")
        items.append(item)
    return items


def render_csv(items: List[dict]) -> str:
    output = StringIO()
    writer = csv.writer(output, delimiter=",")
    writer.writerow(VK_ESTATE_HEADERS)
    for i in items:
        writer.writerow([i.get(h, "") for h in VK_ESTATE_HEADERS])
    return output.getvalue()

def render_tsv(items: List[dict]) -> str:
    output = StringIO()
    writer = csv.writer(output, delimiter="\t")
    writer.writerow(VK_ESTATE_HEADERS)
    for i in items:
        writer.writerow([i.get(h, "") for h in VK_ESTATE_HEADERS])
    return output.getvalue()

def format_vk_estate(data: List[dict], output_format: str = "csv") -> str:
    items = parse_input(data)
    if output_format == "csv":
        return render_csv(items)
    if output_format == "tsv":
        return render_tsv(items)
    raise ValueError(f"Unsupported VK output format: {output_format}")
