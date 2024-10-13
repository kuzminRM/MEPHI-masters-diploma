from __future__ import annotations

from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, Field


class StoreEnum(StrEnum):
    STROYDVOR = 'STROYDVOR'
    OBI = 'OBI'


class CategoryEnum(StrEnum):
    STROITELNIE_SMESI = 'STROITELNIE_SMESI'
    NDY = 'NOT_DEFINED_YET'


class Product(BaseModel):
    uid: str
    store: StoreEnum
    title: str
    url: str
    category: CategoryEnum
    description: str | None = None
    images: list[str] = Field(default_factory=list)
    price: float
    properties: PropertiesData


class PropertiesData(BaseModel):
    as_text: str
    as_dict: dict[str, str] | None = None
    brand: str | None = None
    label: str | None = None
    country: str | None = None
    color: str | None = None
    material: str | None = None
    mass: MassData | None = None
    volume: VolumeData | None = None
    dimensions: DimensionsData | None = None
    art_codes: list[str] = Field(default_factory=list)
    category_list_raw: list[str] = Field(default_factory=list)


class VolumeUnitsEnum(StrEnum):
    LITER = 'l'
    MILLILITER = 'ml'


class VolumeData(BaseModel):
    raw: str | None
    num: float | None
    unit: VolumeUnitsEnum | None


class MassUnitsEnum(StrEnum):
    TONNE = 't'
    KILOGRAM = 'kg'
    GRAM = 'gr'


class MassData(BaseModel):
    raw: str | None
    num: float | None
    unit: MassUnitsEnum | None


class DimensionUnitsEnum(StrEnum):
    MILLIMETERS = 'mm'
    METERS = 'm'
    CENTIMETERS = 'cm'


class DimensionsData(BaseModel):
    """d_list отсортирован по убыванию"""
    raw: str | None
    d_list: list[float] = Field(default_factory=list)
    all_units_parsed: bool | None
