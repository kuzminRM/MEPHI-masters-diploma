import re
from enum import StrEnum
from typing import TypeVar

from parsers.runnures.schemas.product import MassUnitsEnum, DimensionUnitsEnum, VolumeUnitsEnum

mass_unit_map = {
    'т': MassUnitsEnum.TONNE,
    'кг': MassUnitsEnum.KILOGRAM,
    'гр': MassUnitsEnum.GRAM,
}

mass_converter_map = {
    MassUnitsEnum.TONNE: 1000,
    MassUnitsEnum.KILOGRAM: 1,
    MassUnitsEnum.GRAM: 0.001,
}

dimensions_unit_map = {
    'мм': DimensionUnitsEnum.MILLIMETERS,
    'см': DimensionUnitsEnum.CENTIMETERS,
    'м': DimensionUnitsEnum.METERS,
}
dimensions_converter_map = {
    DimensionUnitsEnum.MILLIMETERS: 1,
    DimensionUnitsEnum.CENTIMETERS: 10,
    DimensionUnitsEnum.METERS: 1000,
}

volume_unit_map = {
    'л': VolumeUnitsEnum.LITER,
    'мл': VolumeUnitsEnum.MILLILITER,
}

volume_converter_map = {
    VolumeUnitsEnum.LITER: 1,
    VolumeUnitsEnum.MILLILITER: 0.001,
}


def extract_num(value: str | None, set_0_on_none: bool = False) -> float | None:
    if value is None:
        return 0 if set_0_on_none else None
    digit_regexp = re.compile(r'[\d,. ]+')
    match = digit_regexp.search(value)
    if not match:
        return 0 if set_0_on_none else None
    num_str = match[0]
    return float(num_str.replace(',', '.').replace(' ', ''))


T = TypeVar('T', bound=StrEnum)


def extract_unit(value: str | None, unit_map: dict[str, T]) -> T | None:
    if value is None:
        return None
    char_regexp = re.compile(r'[a-zA-Zа-яА-ЯёЁ]+')
    match = char_regexp.search(value)
    if not match:
        return None
    return unit_map.get(match[0].lower())


def unify_measure(value: float | None, unit: T | None) -> tuple[float | None, T | None]:
    if unit is None or value is None:
        return value, unit

    converter_map = {}
    base_unit = None
    if isinstance(unit, DimensionUnitsEnum):
        converter_map = dimensions_converter_map
        base_unit = DimensionUnitsEnum.MILLIMETERS
    if isinstance(unit, MassUnitsEnum):
        converter_map = mass_converter_map
        base_unit = MassUnitsEnum.KILOGRAM
    if isinstance(unit, VolumeUnitsEnum):
        converter_map = volume_converter_map
        base_unit = VolumeUnitsEnum.LITER

    return value * converter_map.get(unit), base_unit


def get_num_and_unit(
        raw_value: str | None,
        unit_map: dict[str, T],
        set_0_on_none: bool = False
) -> tuple[float | None, T | None]:
    num = extract_num(raw_value, set_0_on_none=set_0_on_none)
    unit = extract_unit(raw_value, unit_map)
    return unify_measure(num, unit)
