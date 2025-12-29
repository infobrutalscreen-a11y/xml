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


def xml_tag(name: str) -> str:
    """Нормализует имя поля в допустимый XML-тег: заменяет точки/пробелы на подчёркивания
    и оставляет только буквы, цифры и подчёркивания.
    """
    import re

    tag = name.replace(".", "_").replace(" ", "_")
    tag = re.sub(r'[^0-9A-Za-z_]', '_', tag)
    # XML tag must not start with digit; prefix with '_' if so
    if tag and tag[0].isdigit():
        tag = f"_{tag}"
    return tag
