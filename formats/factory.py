from .yml import format_yml
from .avito_auto import format_avito_auto


class Formatter:
    def __init__(self, fn):
        self.fn = fn

    def render(self, cars):
        return self.fn(cars)


def get_formatter(name: str) -> Formatter:
    if name == "yml":
        return Formatter(format_yml)

    if name == "avito_auto":
        return Formatter(format_avito_auto)

    raise ValueError("Unsupported format")
