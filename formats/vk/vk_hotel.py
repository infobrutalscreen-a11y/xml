import csv
from io import StringIO
from typing import List, Dict

from formats.vk.vk_helpers import safe_get

VK_HOTEL_HEADERS = [
    "Property ID","Property name","Final URL","Image URL",
    "Destination name","Description","Price","Address","Locality",
    "Region","Country","Metro","Sale Price","Min Price",
    "custom_label_0","Score"
]

def parse_input(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    items = []
    for row in data:
        item = {}
        for h in VK_HOTEL_HEADERS:
            item[h] = safe_get(row, [h, h.lower().replace(" ","_")], "")
        items.append(item)
    return items

def render_csv(items: List[dict]) -> str:
    output = StringIO()
    writer = csv.writer(output, delimiter=",")
    writer.writerow(VK_HOTEL_HEADERS)
    for i in items:
        writer.writerow([i.get(h, "") for h in VK_HOTEL_HEADERS])
    return output.getvalue()

def render_tsv(items: List[dict]) -> str:
    output = StringIO()
    writer = csv.writer(output, delimiter="\t")
    writer.writerow(VK_HOTEL_HEADERS)
    for i in items:
        writer.writerow([i.get(h, "") for h in VK_HOTEL_HEADERS])
    return output.getvalue()

def format_vk_hotel(data: List[dict], output_format: str = "csv") -> str:
    items = parse_input(data)
    if output_format == "csv":
        return render_csv(items)
    if output_format == "tsv":
        return render_tsv(items)
    raise ValueError(f"Unsupported VK output format: {output_format}")
