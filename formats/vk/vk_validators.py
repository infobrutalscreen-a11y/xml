from typing import List, Dict
import re


def _is_numberish(s: str) -> bool:
    if s is None or s == "":
        return False
    s = str(s).strip()
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
        if year and not year.isdigit():
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
