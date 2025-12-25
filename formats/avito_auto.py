from typing import List
from convert import Car


def format_avito_auto(cars: List[Car]) -> str:
    xml = []
    xml.append('<?xml version="1.0" encoding="UTF-8"?>')
    xml.append('<Ads formatVersion="3" target="Avito.ru">')

    for car in cars:
        condition = "Новое" if car.condition == "new" else "С пробегом"

        xml.append("  <Ad>")
        xml.append("    <Category>Автомобили</Category>")
        xml.append("    <OperationType>Продам</OperationType>")
        xml.append("    <AdType>Автомобиль</AdType>")

        xml.append(f"    <Id>{car.folder_id}</Id>")
        xml.append(f"    <Title>{car.modification_id}</Title>")
        xml.append(f"    <Brand>{car.mark_id}</Brand>")

        xml.append(f"    <Condition>{condition}</Condition>")
        xml.append(f"    <Year>{car.year}</Year>")
        xml.append(f"    <Price>{car.price}</Price>")

        if car.vin:
            xml.append(f"    <VIN>{car.vin}</VIN>")

        if car.picture:
            xml.append("    <Images>")
            xml.append(f"      <Image url=\"{car.picture}\"/>")
            xml.append("    </Images>")

        xml.append("  </Ad>")

    xml.append("</Ads>")
    return "\n".join(xml)
