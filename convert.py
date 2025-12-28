import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Optional


def _norm_text(s: str) -> str:
    return s.strip().lower().replace("ё", "е")


def _clean_int(value: Optional[str]) -> Optional[int]:
    if not value:
        return None
    digits = "".join([c for c in value if c.isdigit()])
    return int(digits) if digits else None


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

    # Новый критерий (2-й): пробег/мильяж
    mileage_km: Optional[int] = None

    # Опционально: если в XML есть явное поле condition/is_new и т.п.
    condition_raw: Optional[str] = None

    @property
    def condition(self) -> str:
        """
        Определяет NEW / USED по нескольким сигналам:
        1) явное condition/is_new (если есть)
        2) mileage/run/odometer (0 => new, >0 => used)
        3) owners_number (тексты/цифры)
        """
        # 1) Явный condition/is_new
        if self.condition_raw:
            txt = _norm_text(self.condition_raw)
            new_tokens = {
                "new", "новый", "новое", "новая", "без пробега", "0", "yes", "true", "1"
            }
            used_tokens = {
                "used", "с пробегом", "б/у", "бу", "подержанный", "подержанная", "no", "false"
            }
            if txt in new_tokens:
                return "new"
            if txt in used_tokens:
                return "used"

        # 2) Пробег/мильяж
        if self.mileage_km is not None:
            return "new" if self.mileage_km == 0 else "used"

        # 3) owners_number
        if not self.owners_number_raw:
            return "new"

        txt = _norm_text(self.owners_number_raw)

        # Частые формулировки "новая"
        new_phrases = (
            "не было владельцев",
            "не было собственников",
            "без владельцев",
            "0 владельцев",
            "ноль владельцев",
            "без пробега",
            "новый",
            "новая",
            "новое",
            "новые",
        )
        if any(p in txt for p in new_phrases):
            return "new"

        # Если есть цифры владельцев
        digits = "".join([c for c in txt if c.isdigit()])
        if digits:
            try:
                return "used" if int(digits) > 0 else "new"
            except Exception:
                pass

        # Частые формулировки "б/у"
        used_phrases = (
            "владел",
            "бывш",
            "с пробегом",
            "б/у",
            "бу",
            "подержан",
        )
        if any(p in txt for p in used_phrases):
            return "used"

        # По умолчанию
        return "new"
