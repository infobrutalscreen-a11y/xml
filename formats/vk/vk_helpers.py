from typing import Optional
import xml.etree.ElementTree as ET

def safe_get(data: dict, keys: list[str], default=None):
    """
    Ищем первый встречный ключ из списка похожих.
    Например: ["price", "cost", "цена"]
    """
    for k in keys:
        v = data.get(k)
        if v is not None and v != "":
            return v
    return default

def extract_text(element: ET.Element, tags: list[str]) -> Optional[str]:
    """
    Ищем первое значение из похожих тегов в XML.
    """
    for tag in tags:
        found = element.find(tag)
        if found is not None and found.text:
            return found.text.strip()
    return None
