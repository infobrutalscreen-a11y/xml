import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Optional, List


# =====================
# ВНУТРЕННЯЯ МОДЕЛЬ
# =====================

@dataclass
class Car:
    mark_id: str
    folder_id: str
    modification_id: str
    body_type: str
    year: int
    price: int
    vin: Optional[str]
    url: str
    picture: Optional[str]
    owners_number_raw: Optional[str]
    poi_id: Optional[str]
    phone: Optional[str]

    @property
    def condition(self) -> str:
        """
        Определяет NEW / USED на основе owners_number.
        """
        if not self.owners_number_raw:
            return "new"

        txt = self.owners_number_raw.lower()

        if "не было" in txt:
            return "new"

        digits = "".join([c for c in txt if c.isdigit()])
        if digits:
            try:
                return "used" if int(digits) > 0 else "new"
            except:
                return "new"

        if "владел" in txt:
            return "used"

        return "new"


# =====================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# =====================

def get_text(parent, tag: str) -> Optional[str]:
    el = parent.find(tag)
    if el is not None and el.text:
        return el.text.strip()
    return None


def clean_price(value: str) -> Optional[int]:
    if not value:
        return None
    digits = "".join([c for c in value if c.isdigit()])
    return int(digits) if digits else None


def get_first_picture(car: ET.Element) -> Optional[str]:
    images_tag = car.find("images")
    if images_tag is None:
        return None
    image = images_tag.find("image")
    if image is not None and image.text:
        return image.text.strip()
    return None


def get_phone(car: ET.Element) -> Optional[str]:
    contact = car.find(".//contact/phone")
    if contact is not None and contact.text:
        return contact.text.strip()
    return None


# =====================
# XML → List[Car]
# =====================

def parse_cars(xml_bytes: bytes) -> List[Car]:
    root = ET.fromstring(xml_bytes)
    cars: List[Car] = []

    for car in root.findall(".//car"):
        mark_id = get_text(car, "mark_id") or ""
        folder_id = get_text(car, "folder_id") or ""
        modification_id = get_text(car, "modification_id") or ""
        body_type = get_text(car, "body_type") or ""
        year_raw = get_text(car, "year")
        price_raw = get_text(car, "price")
        vin = get_text(car, "vin")
        url = get_text(car, "url") or ""
        owners_number = get_text(car, "owners_number")
        poi_id = get_text(car, "poi_id")
        phone = get_phone(car)
        picture = get_first_picture(car)

        if not (mark_id and folder_id and modification_id and year_raw and price_raw and url):
            continue

        price = clean_price(price_raw)
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
                phone=phone
            )
        )

    return cars


# =====================
# YML FORMATTER (Яндекс)
# =====================

def format_yml(cars: List[Car]) -> str:
    yml = []
    yml.append('<?xml version="1.0" encoding="UTF-8"?>')
    yml.append('<yml_catalog date="2025-01-01">')
    yml.append('  <shop>')
    yml.append('    <name>Feed Converter</name>')
    yml.append('    <company>Feed Converter</company>')
    yml.append('    <currencies>')
    yml.append('      <currency id="RUB" rate="1"/>')
    yml.append('    </currencies>')
    yml.append('    <categories>')
    yml.append('      <category id="1">Автомобили</category>')
    yml.append('    </categories>')
    yml.append('    <offers>')

    for car in cars:
        yml.append(f'      <offer id="{car.folder_id}" available="true">')
        yml.append(f'        <url>{car.url}</url>')
        yml.append(f'        <price>{car.price}</price>')
        yml.append('        <currencyId>RUB</currencyId>')
        yml.append('        <categoryId>1</categoryId>')
        if car.picture:
            yml.append(f'        <picture>{car.picture}</picture>')
        yml.append(f'        <name>{car.modification_id}</name>')
        yml.append(f'        <vendor>{car.mark_id}</vendor>')
        yml.append(f'        <year>{car.year}</year>')
        yml.append(f'      </offer>')

    yml.append('    </offers>')
    yml.append('  </shop>')
    yml.append('</yml_catalog>')

    return "\n".join(yml)
