from typing import List, Optional
from datetime import datetime
from xml.sax.saxutils import escape

from convert import Car


COND_MAP = {
    "new": "Новый",
    "used": "С пробегом",
}


def detect_condition(car: Car) -> str:
    """
    Вариант B:
    1) owners_number (car.condition)
    2) fallback: vin/year
    """
    # основной признак
    if car.owners_number_raw:
        return car.condition

    # доп. признаки
    if car.vin and car.vin.strip():
        return "used"

    current_year = datetime.utcnow().year
    if car.year and car.year < current_year:
        return "used"

    return "new"


def _render_ads(cars: List[Car], only: Optional[str] = None) -> str:
    out: List[str] = []
    out.append('<?xml version="1.0" encoding="UTF-8"?>')
    out.append('<Ads formatVersion="3" target="Avito.ru">')

    for car in cars:
        cond = detect_condition(car)
        if only and cond != only:
            continue

        out.append("  <Ad>")
        # Id — желательно стабильный
        out.append(f"    <Id>{escape(car.folder_id)}</Id>")

        # Минимальные поля (под свои реальные требования Avito подстроишь)
        out.append("    <Category>Транспорт</Category>")
        out.append("    <VehicleType>Автомобили</VehicleType>")

        out.append(f"    <Make>{escape(car.mark_id)}</Make>")
        out.append(f"    <Model>{escape(car.folder_id)}</Model>")
        out.append(f"    <Year>{car.year}</Year>")
        out.append(f"    <Price>{car.price}</Price>")

        # Состояние
        out.append(f"    <Condition>{COND_MAP.get(cond, 'С пробегом')}</Condition>")

        # URL
        if car.url:
            out.append(f"    <URL>{escape(car.url)}</URL>")

        # VIN
        if car.vin:
            out.append(f"    <VIN>{escape(car.vin)}</VIN>")

        # Фото
        if car.picture:
            out.append("    <Images>")
            out.append(f"      <Image url=\"{escape(car.picture)}\"/>")
            out.append("    </Images>")

        # Телефон (если нужен)
        if car.phone:
            out.append(f"    <ContactPhone>{escape(car.phone)}</ContactPhone>")

        out.append("  </Ad>")

    out.append("</Ads>")
    return "\n".join(out)


def format_avito_auto(cars: List[Car]) -> str:
    return _render_ads(cars, only=None)


def format_avito_auto_new(cars: List[Car]) -> str:
    return _render_ads(cars, only="new")


def format_avito_auto_used(cars: List[Car]) -> str:
    return _render_ads(cars, only="used")
