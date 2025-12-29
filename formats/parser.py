# formats/parser.py
import xml.etree.ElementTree as ET
import csv
import yaml
from io import StringIO
from typing import List, Optional, Dict

from convert import Car


def _normalize_row(row: Dict[str, str]) -> Dict[str, str]:
    return {k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in row.items()}


def parse_csv_bytes(b: bytes, delimiter: str = ',') -> List[Dict[str, str]]:
    s = b.decode('utf-8-sig')
    f = StringIO(s)
    reader = csv.DictReader(f, delimiter=delimiter)
    rows: List[Dict[str, str]] = []
    for r in reader:
        rows.append(_normalize_row({k: (v if v is not None else '') for k, v in r.items()}))
    return rows


def parse_yaml_bytes(b: bytes) -> List[Dict[str, str]]:
    s = b.decode('utf-8')
    data = yaml.safe_load(s)
    if isinstance(data, list):
        return [_normalize_row(r) for r in data]
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, list):
                return [_normalize_row(r) for r in v]
        return [_normalize_row(data)]
    return []


def parse_xml_bytes(b: bytes) -> List[Dict[str, str]]:
    root = ET.fromstring(b)

    tag_counts: Dict[str, int] = {}
    for child in root:
        tag_counts[child.tag] = tag_counts.get(child.tag, 0) + 1

    rows_tag = None
    max_count = 0
    for tag, cnt in tag_counts.items():
        if cnt > max_count:
            max_count = cnt
            rows_tag = tag

    items: List[Dict[str, str]] = []
    if rows_tag and max_count > 1:
        for el in root.findall(rows_tag):
            d: Dict[str, str] = {}
            for child in list(el):
                if len(list(child)) == 0:
                    d[child.tag] = (child.text or '').strip()
                else:
                    d[child.tag] = ''.join(ET.tostring(c, encoding='unicode') for c in child)
            items.append(d)
        return items

    for tag in ('car', 'item', 'offer', 'row', 'entry'):
        found = root.findall(f'.//{tag}')
        if found:
            for el in found:
                d: Dict[str, str] = {}
                for child in list(el):
                    if len(list(child)) == 0:
                        d[child.tag] = (child.text or '').strip()
                    else:
                        d[child.tag] = ''.join(ET.tostring(c, encoding='unicode') for c in child)
                items.append(d)
            return items

    for child in root:
        d: Dict[str, str] = {}
        for c in list(child):
            if len(list(c)) == 0:
                d[c.tag] = (c.text or '').strip()
            else:
                d[c.tag] = ''.join(ET.tostring(cc, encoding='unicode') for cc in c)
        if d:
            items.append(d)

    return items


def parse_bytes_by_format(b: bytes, fmt: str) -> List[Dict[str, str]]:
    fmt = (fmt or '').lower()
    if fmt in ('csv', '.csv'):
        return parse_csv_bytes(b, delimiter=',')
    if fmt in ('tsv', '.tsv', 'txt'):
        return parse_csv_bytes(b, delimiter='\t')
    if fmt in ('yml', 'yaml', '.yml', '.yaml'):
        return parse_yaml_bytes(b)
    if fmt in ('xml', '.xml'):
        return parse_xml_bytes(b)

    s = b.lstrip()
    if s.startswith(b'<'):
        return parse_xml_bytes(b)
    if s.startswith(b'-') or b'\n- ' in s:
        return parse_yaml_bytes(b)
    return parse_csv_bytes(b)


def _clean_price(value: Optional[str]) -> Optional[int]:
    if not value:
        return None
    digits = "".join(c for c in value if c.isdigit())
    return int(digits) if digits else None


def _get_first_picture(car: ET.Element) -> Optional[str]:
    images_tag = car.find("images")
    if images_tag is None:
        return None

    # берём первый непустой <image>
    for img in images_tag.findall("image"):
        if img is not None and img.text:
            t = img.text.strip()
            if t:
                return t
    return None


def _get_phone(car: ET.Element) -> Optional[str]:
    # варианты структуры
    for path in (".//contact/phone", ".//contact_info/contact/phone", ".//phone"):
        el = car.find(path)
        if el is not None and el.text:
            t = el.text.strip()
            if t:
                return t
    return None


def parse_cars(xml_bytes: bytes) -> List[Car]:
    """
    XML -> List[Car]
    Требуемые поля: mark_id, folder_id, modification_id, year, price, url
    """
    root = ET.fromstring(xml_bytes)
    cars: List[Car] = []

    for car in root.findall(".//car"):
        mark_id = _get_text(car, "mark_id") or ""
        folder_id = _get_text(car, "folder_id") or ""
        modification_id = _get_text(car, "modification_id") or ""
        body_type = _get_text(car, "body_type") or ""
        year_raw = _get_text(car, "year")
        price_raw = _get_text(car, "price")
        vin = _get_text(car, "vin")
        url = _get_text(car, "url") or ""
        owners_number = _get_text(car, "owners_number")
        poi_id = _get_text(car, "poi_id")
        phone = _get_phone(car)
        picture = _get_first_picture(car)

        # обязательные
        if not (mark_id and folder_id and modification_id and year_raw and price_raw and url):
            continue

        price = _clean_price(price_raw)
        if not price:
            continue

        try:
            year = int(year_raw)
        except Exception:
            continue

        cars.append(
            Car(
                mark_id=mark_id,
                folder_id=folder_id,
                modification_id=modification_id,
                body_type=body_type,
                year=year,
                price=price,
                vin=vin,
                url=url,
                picture=picture,
                owners_number_raw=owners_number,
                poi_id=poi_id,
                phone=phone,
            )
        )

    return cars
