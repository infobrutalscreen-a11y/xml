from formats.yml import format_yml
from formats.avito import format_avito
from formats.autoru import format_autoru
from formats.avito_auto import format_avito_auto

def get_formatter(fmt: str):
    fmt = fmt.lower()

    if fmt == "yml":
        return format_yml

    if fmt == "avito":
        return format_avito

    if fmt == "autoru":
        return format_autoru

    if fmt == "avito_auto":
        return format_avito_auto

    raise ValueError("Unsupported format")
