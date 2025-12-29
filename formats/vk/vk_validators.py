from typing import List, Dict
import re


def _is_numberish(s) -> bool:
    if s is None:
        return False
    try:
        s = str(s).strip()
    except Exception:
        return False
    return bool(re.search(r"\d", s))


def validate_goods(items: List[Dict[str, str]]) -> List[str]:
    warnings: List[str] = []
    req = ["id", "title", "price"]
    for idx, item in enumerate(items):
        for f in req:
            v = item.get(f, "")
            if not v:
                warnings.append(f"row {idx+1}: missing required field '{f}'")
        price = item.get("price", "")
        if price and not _is_numberish(price):
            warnings.append(f"row {idx+1}: price looks non-numeric: '{price}'")
    return warnings


def validate_auto(items: List[Dict[str, str]]) -> List[str]:
    warnings: List[str] = []
    req = ["id", "title", "price"]
    for idx, item in enumerate(items):
        for f in req:
            v = item.get(f, "")
            if not v:
                warnings.append(f"row {idx+1}: missing required field '{f}'")
        year = item.get("year", "")
        if year and not str(year).strip().isdigit():
            warnings.append(f"row {idx+1}: year looks invalid: '{year}'")
        price = item.get("price", "")
        if price and not _is_numberish(price):
            warnings.append(f"row {idx+1}: price looks non-numeric: '{price}'")
    return warnings


def validate_vk_category(category: str, items: List[Dict[str, str]]) -> List[str]:
    cat = (category or "").lower()
    if cat == "goods":
        return validate_goods(items)
    if cat == "auto":
        return validate_auto(items)
    # default: no validation
    return []
