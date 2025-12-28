from dataclasses import dataclass
from typing import Optional


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

    # new fields for better NEW/USED detection
    mileage_km: Optional[int] = None
    condition_hint: Optional[str] = None  # e.g. "new"/"used"/"с пробегом"/"новый"

    @property
    def condition(self) -> str:
        """
        Determine "new" / "used" with multiple rules:
        1) explicit hint (condition/state/is_new)
        2) owners_number
        3) mileage_km
        Default: "new"
        """
        # 1) explicit hint
        if self.condition_hint:
            txt = self.condition_hint.strip().lower()
            if txt in ("new", "новый", "новое", "новая", "без пробега", "0", "yes", "true", "1"):
                return "new"
            if txt in ("used", "с пробегом", "б/у", "бу", "подержанный", "подержанная", "no", "false"):
                return "used"

        # 2) owners_number rule (your old logic)
        if self.owners_number_raw:
            txt = self.owners_number_raw.strip().lower()

            if "не было" in txt:
                return "new"

            digits = "".join([c for c in txt if c.isdigit()])
            if digits:
                try:
                    return "used" if int(digits) > 0 else "new"
                except Exception:
                    pass

            if "владел" in txt:
                return "used"

        # 3) mileage rule
        if self.mileage_km is not None:
            try:
                return "new" if int(self.mileage_km) <= 0 else "used"
            except Exception:
                return "used"

        return "new"
