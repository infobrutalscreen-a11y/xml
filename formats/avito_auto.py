# formats/avito_auto.py
from typing import List, Optional

from convert import Car


def _xml_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def _car_title(car: Car) -> str:
    # Пример: "HONGQI HS3 — Hongqi HS3 Deluxe"
    parts = []
    if car.mark_id:
        parts.append(car.mark_id)
    if car.folder_id:
        parts.append(car.folder_id)
    title = " ".join(parts).strip()
    if car.modification_id:
        if title:
            return f"{title} — {car.modification_id}"
        return car.modification_id
    return title or "Автомобиль"


def _render_avito(cars: List[Car], only: Optional[str] = None) -> str:
    """
    only: None | "new" | "used"
    """
    items = cars
    if only in ("new", "used"):
        items = [c for c in cars if c.condition == only]

    out = []
    out.append('<?xml version="1.0" encoding="UTF-8"?>')
    out.append('<Ads formatVersion="3" target="Avito.ru">')

    for idx, car in enumerate(items, start=1):
        # стабильный id
        ad_id = car.vin or f"{car.folder_id}-{idx}"
        out.append("  <Ad>")
        out.append(f"    <Id>{_xml_escape(ad_id)}</Id>")
        out.append(f"    <Title>{_xml_escape(_car_title(car))}</Title>")
        out.append("    <Category>Автомобили</Category>")
        out.append(f"    <Price>{car.price}</Price>")
        out.append(f"    <Url>{_xml_escape(car.url)}</Url>")
        out.append(f"    <Year>{car.year}</Year>")
        out.append(f"    <Make>{_xml_escape(car.mark_id)}</Make>")
        out.append(f"    <Model>{_xml_escape(car.folder_id)}</Model>")
        out.append(f"    <Condition>{'Новое' if car.condition == 'new' else 'С пробегом'}</Condition>")

        if car.body_type:
            out.append(f"    <BodyType>{_xml_escape(car.body_type)}</BodyType>")
        if car.vin:
            out.append(f"    <VIN>{_xml_escape(car.vin)}</VIN>")
        if car.poi_id:
            out.append(f"    <Address>{_xml_escape(car.poi_id)}</Address>")
        if car.phone:
            out.append(f"    <ContactPhone>{_xml_escape(car.phone)}</ContactPhone>")

        if car.picture:
            out.append("    <Images>")
            out.append(f"      <Image url=\"{_xml_escape(car.picture)}\"/>")
            out.append("    </Images>")

        out.append("  </Ad>")

    out.append("</Ads>")
    return "\n".join(out)


def format_avito_auto(cars: List[Car]) -> str:
    # по умолчанию — как раньше: отдаём всё
    return _render_avito(cars, only=None)


def format_avito_auto_new(cars: List[Car]) -> str:
    return _render_avito(cars, only="new")


def format_avito_auto_used(cars: List[Car]) -> str:
    return _render_avito(cars, only="used")
