import xml.etree.ElementTree as ET
from typing import List, Optional

from convert import Car


def _get_text(parent: ET.Element, tag: str) -> Optional[str]:
    el = parent.find(tag)
    if el is not None and el.text:
        return el.text.strip()
    return None


def _clean_price(value: Optional[str]) -> Optional[int]:
    if not value:
        return None
    digits = "".join([c for c in value if c.isdigit()])
    return int(digits) if digits else None


def _get_first_picture(car: ET.Element) -> Optional[str]:
    images_tag = car.find("images")
    if images_tag is None:
        return None
    image = images_tag.find("image")
    if image is not None and image.text and image.text.strip():
        return image.text.strip()
    return None


def _get_phone(car: ET.Element) -> Optional[str]:
    contact = car.find(".//contact/phone")
    if contact is not None and contact.text:
        return contact.text.strip()
    return None


def parse_cars(xml_bytes: bytes) -> List[Car]:
    """
    XML -> List[Car]
    Ожидаем структуру с тегами <car>...</car>
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

        if not (mark_id and folder_id and modification_id and year_raw and price_raw and url):
            continue

        price = _clean_price(price_raw)
        if not price:
            continue

        try:
            year = int(year_raw)
        except:
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
