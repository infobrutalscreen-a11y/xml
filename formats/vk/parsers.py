# Thin compatibility wrapper — unified parsers are located in `formats.parser`
from formats.parser import (
    parse_bytes_by_format,
    parse_csv_bytes,
    parse_yaml_bytes,
    parse_xml_bytes,
)

__all__ = [
    'parse_bytes_by_format',
    'parse_csv_bytes',
    'parse_yaml_bytes',
    'parse_xml_bytes',
]
