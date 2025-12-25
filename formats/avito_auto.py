def format_avito_auto(cars):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<Ads formatVersion="3" target="Avito.ru">')

    for car in cars:
        lines.append("  <Ad>")
        lines.append(f"    <Title>{car.name}</Title>")
        lines.append(f"    <Price>{car.price}</Price>")
        lines.append("    <Currency>RUB</Currency>")
        lines.append("    <Category>втомобили</Category>")
        lines.append(f"    <URL>{car.url}</URL>")

        if car.picture:
            lines.append("    <Images>")
            lines.append(f"      <Image url=\"{car.picture}\"/>")
            lines.append("    </Images>")

        lines.append("  </Ad>")

    lines.append("</Ads>")
    return "\n".join(lines)
