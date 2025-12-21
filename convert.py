import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Optional

# =====================
# ВНУТРЕННЯЯ МОДЕЛЬ
# =====================

@dataclass
class Car:
    name: str
    price: int
    url: str
    picture: Optional[str] = None


# =====================
# КОНВЕРТАЦИЯ
# =====================
def get_text(parent, *tags):
    for tag in tags:
        el = parent.find(tag)
        if el is not None and el.text:
            return el.text.strip()
    return None


def clean_price(value):
    if not value:
        return None
    return int("".join(c for c in value if c.isdigit()))

def convert(input_xml: str, output_yml: str):
    tree = ET.parse(input_xml)
    root = tree.getroot()

    cars = []

    # --- XML → Car ---
    for i, car in enumerate(root.findall("car"), start=1):
        name = get_text(car, "name", "title", "model")
        price_raw = get_text(car, "price", "cost", "amount")
        url = get_text(car, "url", "link")
        picture = get_text(car, "picture", "image", "photo")

        price = clean_price(price_raw)
        
        if not name or not price or not url:
          print(f"Пропущен товар #{i} — некорректные данные")
          continue

        cars.append(
            Car(
                name=name,
                price=int(price),
                url=url,
                picture=picture
            )
        )

    # --- Car → YML ---
    yml = """<?xml version="1.0" encoding="UTF-8"?>
<yml_catalog date="2025-01-01">
  <shop>
    <name>Feed Converter</name>
    <company>Feed Converter</company>
    <currencies>
      <currency id="RUB" rate="1"/>
    </currencies>
    <categories>
      <category id="1">Автомобили</category>
    </categories>
    <offers>
"""

    for car in cars:
        yml += f"""
      <offer available="true">
        <url>{car.url}</url>
        <price>{car.price}</price>
        <currencyId>RUB</currencyId>
        <categoryId>1</categoryId>
"""

        if car.picture:
            yml += f"""
        <picture>{car.picture}</picture>
"""

        yml += f"""
        <name>{car.name}</name>
      </offer>
"""

    yml += """
    </offers>
  </shop>
</yml_catalog>
"""

    with open(output_yml, "w", encoding="utf-8") as f:
        f.write(yml)

