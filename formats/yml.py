from typing import List
from convert import Car


def format_yml(cars: List[Car]) -> str:
    yml = []
    yml.append('<?xml version="1.0" encoding="UTF-8"?>')
    yml.append('<yml_catalog date="2025-01-01">')
    yml.append('  <shop>')
    yml.append('    <name>Feed Converter</name>')
    yml.append('    <company>Feed Converter</company>')
    yml.append('    <currencies>')
    yml.append('      <currency id="RUB" rate="1"/>')
    yml.append('    </currencies>')
    yml.append('    <categories>')
    yml.append('      <category id="1">Автомобили</category>')
    yml.append('    </categories>')
    yml.append('    <offers>')

    for car in cars:
        yml.append(f'      <offer id="{car.folder_id}" available="true">')
        yml.append(f'        <url>{car.url}</url>')
        yml.append(f'        <price>{car.price}</price>')
        yml.append('        <currencyId>RUB</currencyId>')
        yml.append('        <categoryId>1</categoryId>')
        if car.picture:
            yml.append(f'        <picture>{car.picture}</picture>')
        yml.append(f'        <name>{car.modification_id}</name>')
        yml.append(f'        <vendor>{car.mark_id}</vendor>')
        yml.append(f'        <year>{car.year}</year>')
        yml.append('      </offer>')

    yml.append('    </offers>')
    yml.append('  </shop>')
    yml.append('</yml_catalog>')

    return "\n".join(yml)
