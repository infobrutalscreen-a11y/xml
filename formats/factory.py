from .yml import format_yml
from .avito_auto import format_avito_auto, format_avito_auto_new, format_avito_auto_used


class Formatter:
    def __init__(self, fn):
        self.fn = fn

    def render(self, cars):
        return self.fn(cars)

    def __call__(self, cars):
        return self.fn(cars)


def get_formatter(name: str) -> Formatter:
    if name == "yml":
        return Formatter(format_yml)

    if name == "avito_auto":
        return Formatter(format_avito_auto)

    if name == "avito_auto_new":
        return Formatter(format_avito_auto_new)

    if name == "avito_auto_used":
        return Formatter(format_avito_auto_used)

    raise ValueError(f"Unsupported format: {name}")
