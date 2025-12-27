from .yml import format_yml
from .avito_auto import format_avito_auto

# сюда будешь добавлять новые:
# from .avito_new import format_avito_new
# from .avito_used import format_avito_used
# from .auto_ru import format_auto_ru
# ...

FORMATTERS = {
    "yml": format_yml,
    "avito_auto": format_avito_auto,
    # "avito_new": format_avito_new,
    # "avito_used": format_avito_used,
    # "auto_ru": format_auto_ru,
}

class Formatter:
    def __init__(self, fn):
        self.fn = fn

    def render(self, cars):
        return self.fn(cars)

    def __call__(self, cars):
        return self.fn(cars)

def list_formats():
    return sorted(FORMATTERS.keys())

def get_formatter(name: str) -> Formatter:
    fn = FORMATTERS.get(name)
    if not fn:
        raise ValueError("Unsupported format")
    return Formatter(fn)
