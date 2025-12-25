from formats.yml import format_yml
from formats.avito_auto import format_avito_auto


def get_formatter(fmt: str):
    fmt = fmt.lower()

    if fmt == "yml":
        return format_yml

    if fmt in ("avito", "avito_auto"):
        return format_avito_auto

    raise ValueError(f"Unsupported format: {fmt}")
