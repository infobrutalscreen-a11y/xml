from typing import List
from formats.vk.vk_auto import format_vk_auto
from formats.vk.vk_goods import format_vk_goods
from formats.vk.vk_avia import format_vk_avia
from formats.vk.vk_hotel import format_vk_hotel
from formats.vk.vk_estate import format_vk_estate
from formats.vk.vk_service import format_vk_service

def get_vk_formatter(category: str):
    """
    Возвращает функцию-форматтер по категории VK.
    category: "auto", "goods", "avia", "hotel", "estate", "service"
    """
    cat = category.lower()
    if cat == "auto":
        return format_vk_auto
    if cat == "goods":
        return format_vk_goods
    if cat == "avia":
        return format_vk_avia
    if cat == "hotel":
        return format_vk_hotel
    if cat == "estate":
        return format_vk_estate
    if cat == "service":
        return format_vk_service
    raise ValueError(f"Unsupported VK category: {category}")
