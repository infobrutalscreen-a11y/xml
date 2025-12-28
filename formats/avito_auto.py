# formats/avito_auto.py
from __future__ import annotations

from typing import List, Optional
from datetime import datetime, timezone

from convert import Car


def _esc(s: Optional[str]) -> str:
    """XML escape."""
    if not s:
        return ""
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def _now_iso() -> str:
    # Avito обычно ок с ISO-датой
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _is_new(car: Car) -> bool:
    # Основное правило: owners_number -> condition (у тебя уже есть в Car.condition)
    return (car.condition or "").lower() == "new"


def _render_avito_ads(cars: List[Car], only: Optional[str] = None) -> str:
    """
    only:
      None  -> все
      "new" -> только новые
      "used"-> только б/у
    """
    out: List[str] = []
    out.append('<?xml version="1.0" encoding="UTF-8"?>')
    out.append('<Ads formatVersion="3" target="Avito.ru">')

    for car in cars:
        is_new = _is_new(car)
        if only == "new" and not is_new:
            continue
        if only == "used" and is_new:
            continue

        # --- Базовые поля объявления ---
        out.append("  <Ad>")
        out.append(f"    <Id>{_esc(car.folder_id)}</Id>")
        out.append(f"    <DateBegin>{_now_iso()}</DateBegin>")
        out.append("    <Category>Автомобили</Category>")
        out.append("    <VehicleType>Легковые автомобили</VehicleType>")

        # Марка/модель/модификация (у тебя эти поля в XML как id/строки)
        out.append(f"    <Make>{_esc(car.mark_id)}</Make>")
        out.append(f"    <Model>{_esc(car.folder_id)}</Model>")
        out.append(f"    <Modification>{_esc(car.modification_id)}</Modification>")

        # Состояние
        out.append(f"    <Condition>{'Новое' if is_new else 'С пробегом'}</Condition>")

        # Год/тип кузова
        out.append(f"    <Year>{int(car.year)}</Year>")
        if car.body_type:
            out.append(f"    <BodyType>{_esc(car.body_type)}</BodyType>")

        # Цена
        out.append(f"    <Price>{int(car.price)}</Price>")

        # VIN (если есть)
        if car.vin:
            out.append(f"    <VIN>{_esc(car.vin)}</VIN>")

        # URL
        if car.url:
            out.append(f"    <Url>{_esc(car.url)}</Url>")

        # Контакты (если есть)
        if car.phone:
            out.append(f"    <ContactPhone>{_esc(car.phone)}</ContactPhone>")
        if car.poi_id:
            out.append(f"    <Address>{_esc(car.poi_id)}</Address>")

        # Фото
        if car.picture:
            out.append("    <Images>")
            out.append(f"      <Image url=\"{_esc(car.picture)}\"/>")
            out.append("    </Images>")

        out.append("  </Ad>")

    out.append("</Ads>")
    return "\n".join(out)


def format_avito_auto(cars: List[Car]) -> str:
    """Один общий фид Avito (и новые, и б/у)."""
    return _render_avito_ads(cars, only=None)


def format_avito_auto_new(cars: List[Car]) -> str:
    """Avito: только новые авто."""
    return _render_avito_ads(cars, only="new")


def format_avito_auto_used(cars: List[Car]) -> str:
    """Avito: только авто с пробегом."""
    return _render_avito_ads(cars, only="used")


__all__ = [
    "format_avito_auto",
    "format_avito_auto_new",
    "format_avito_auto_used",
]
