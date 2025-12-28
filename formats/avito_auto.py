from typing import List
from convert import Car


def _render_avito(cars: List[Car]) -> str:
    out = []
    out.append('<?xml version="1.0" encoding="UTF-8"?>')
    out.append('<Ads formatVersion="3" target="Avito.ru">')

    for car in cars:
        out.append("  <Ad>")
        out.append("    <Category>Автомобили</Category>")
        out.append(f"    <Title>{car.mark_id} {car.modification_id}</Title>")
        out.append(f"    <Price>{car.price}</Price>")
        out.append("    <Currency>RUB</Currency>")
        out.append(f"    <Year>{car.year}</Year>")
        out.append(f"    <Url>{car.url}</Url>")

        if car.vin:
            out.append(f"    <VIN>{car.vin}</VIN>")

        if car.picture:
            out.append("    <Images>")
            out.append(f"      <Image url=\"{car.picture}\" />")
            out.append("    </Images>")

        # key point: NEW/USED from our unified logic
        out.append(f"    <Condition>{'Новое' if car.condition == 'new' else 'С пробегом'}</Condition>")

        out.append("  </Ad>")

    out.append("</Ads>")
    return "\n".join(out)


def format_avito_auto(cars: List[Car]) -> str:
    return _render_avito(cars)


def format_avito_auto_new(cars: List[Car]) -> str:
    return _render_avito([c for c in cars if c.condition == "new"])


def format_avito_auto_used(cars: List[Car]) -> str:
    return _render_avito([c for c in cars if c.condition == "used"])
