from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class StoreEnum(StrEnum):
    STROYDVOR = 'STROYDVOR'


class CategoryEnum(StrEnum):
    PLASTER = 'штукатурка'


class Product(BaseModel):
    store: StoreEnum
    title: str
    category: CategoryEnum
    description: str
    images: list[str] = Field(default_factory=list)
    price: float
    properties: PropertiesData


class PropertiesData(BaseModel):
    as_text: str
    as_dict: dict[str, str]
    brand: str | None
    country: str | None
    mass: MassData
    dimensions: MassData
    art_codes: list[str] = Field(default_factory=list)
    art_code_global: str | None


class MassUnitsEnum(StrEnum):
    KILOGRAM = 'kg'


class MassData(BaseModel):
    raw: str | None
    num: float | None
    unit: MassUnitsEnum | None


class DimensionUnitsEnum(StrEnum):
    MILLIMETERS = 'mm'
    METERS = 'm'
    CENTIMETERS = 'cm'


class DimensionsData(BaseModel):
    """d1-d3 отсортированы по убыванию"""
    raw: str | None
    d1: float | None
    d2: float | None
    d3: float | None
    unit: DimensionUnitsEnum | None
