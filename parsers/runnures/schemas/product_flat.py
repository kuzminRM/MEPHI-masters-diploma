import json
import re
from typing import Any
from uuid import uuid4
from pydantic import BaseModel, Field, field_validator, root_validator

from parsers.runnures.schemas.product import StoreEnum, CategoryEnum, Product


class ProductFlat(BaseModel):
    uid: str
    store: StoreEnum
    title: str
    url: str
    category: CategoryEnum
    description: str | None = None
    images: list[str] = Field(default_factory=list)
    images__0: str | None = None
    images__1: str | None = None
    images__2: str | None = None
    images__3: str | None = None
    images__4: str | None = None
    images__5: str | None = None
    price: float
    properties__as_text: str
    properties__as_dict: dict[str, str] | None = None
    properties__brand: str | None = None
    properties__label: str | None = None
    properties__country: str | None = None
    properties__color: str | None = None
    properties__material: str | None = None
    properties__mass__raw: str | None = None
    properties__mass__num: float | None = None
    properties__mass__unit: str | None = None
    properties__volume__raw: str | None = None
    properties__volume__num: float | None = None
    properties__volume__unit: str | None = None
    properties__dimensions__raw: str | None = None
    properties__dimensions__d_list: list[float] | None = None
    properties__dimensions__d_list__0: float | None = None
    properties__dimensions__d_list__1: float | None = None
    properties__dimensions__d_list__2: float | None = None
    properties__dimensions__d_list__3: float | None = None
    properties__dimensions__d_list__4: float | None = None
    properties__dimensions__d_list__5: float | None = None
    properties__dimensions__all_units_parsed: bool | None = None
    properties__art_codes: list[str] = Field(default_factory=list)
    properties__art_codes__0: str | None = None
    properties__art_codes__1: str | None = None
    properties__art_codes__2: str | None = None
    properties__art_codes__3: str | None = None
    properties__art_codes__4: str | None = None
    properties__art_codes__5: str | None = None
    properties__category_list_raw: list[str] = Field(default_factory=list)
    properties__category_list_raw__0: str | None = None
    properties__category_list_raw__1: str | None = None
    properties__category_list_raw__2: str | None = None
    properties__category_list_raw__3: str | None = None
    properties__category_list_raw__4: str | None = None
    properties__category_list_raw__5: str | None = None

    @field_validator('properties__category_list_raw', 'properties__art_codes', 'images', mode='before')
    @classmethod
    def to_list_str(cls, value: Any) -> list[str]:
        if isinstance(value, str):
            return json.loads(
                value
                .replace('"', "\\\"")
                .replace("['", '["')
                .replace("']", '"]')
                .replace(", '", ', "')
                .replace("',", '",')
                .replace("\\xa0", ' ')
            )
        return value

    @field_validator('properties__dimensions__d_list', mode='before')
    @classmethod
    def to_list_float(cls, value: Any) -> list[float]:
        if isinstance(value, str):
            return json.loads(value)
        return value

    @field_validator('properties__as_dict', mode='before')
    @classmethod
    def to_list_dict(cls, value: Any) -> dict:
        if isinstance(value, str):
            return json.loads(re.sub(
                r'(\d),(\d)',
                r'\1.\2',
                value
                .replace('"', "'")
                .replace("{'", '{"')
                .replace("'}", '"}')
                .replace("', '", '", "')
                .replace("': '", '": "')
                .replace("\\xa0", ' ')
            ))
        return value

    @field_validator('properties__as_text', mode='before')
    @classmethod
    def none_to_str(cls, value: Any) -> str:
        if value is None:
            return ''
        return value

    @root_validator(pre=True)
    @classmethod
    def convert_empty_strings(cls, values):
        return {k: (None if v == "" else v) for k, v in values.items()}


def flatten_product(product: Product) -> ProductFlat:
    # Инициализируем словарь для хранения данных в плоском формате
    flat_data = {
        "uid": product.uid,
        "store": product.store,
        "title": product.title,
        "url": product.url,
        "category": product.category,
        "description": product.description,
        "price": product.price,
    }

    # Обработка поля images
    flat_data["images"] = product.images
    for i in range(6):  # Разворачиваем список до 6 элементов
        flat_data[f"images__{i}"] = product.images[i] if i < len(product.images) else None

    # Обработка поля properties
    flat_data["properties__as_text"] = product.properties.as_text
    flat_data["properties__as_dict"] = product.properties.as_dict
    flat_data["properties__brand"] = product.properties.brand
    flat_data["properties__label"] = product.properties.label
    flat_data["properties__country"] = product.properties.country
    flat_data["properties__color"] = product.properties.color
    flat_data["properties__material"] = product.properties.material

    # Обработка properties.mass
    if product.properties.mass:
        flat_data["properties__mass__raw"] = product.properties.mass.raw
        flat_data["properties__mass__num"] = product.properties.mass.num
        flat_data["properties__mass__unit"] = product.properties.mass.unit
    else:
        flat_data["properties__mass__raw"] = None
        flat_data["properties__mass__num"] = None
        flat_data["properties__mass__unit"] = None

    # Обработка properties.volume
    if product.properties.volume:
        flat_data["properties__volume__raw"] = product.properties.volume.raw
        flat_data["properties__volume__num"] = product.properties.volume.num
        flat_data["properties__volume__unit"] = product.properties.volume.unit
    else:
        flat_data["properties__volume__raw"] = None
        flat_data["properties__volume__num"] = None
        flat_data["properties__volume__unit"] = None

    # Обработка properties.dimensions
    if product.properties.dimensions:
        flat_data["properties__dimensions__raw"] = product.properties.dimensions.raw
        flat_data["properties__dimensions__d_list"] = product.properties.dimensions.d_list
        for i in range(6):  # Разворачиваем список до 6 элементов
            flat_data[f"properties__dimensions__d_list__{i}"] = (
                product.properties.dimensions.d_list[i]
                if i < len(product.properties.dimensions.d_list)
                else None
            )
        flat_data["properties__dimensions__all_units_parsed"] = product.properties.dimensions.all_units_parsed
    else:
        flat_data["properties__dimensions__raw"] = None
        flat_data["properties__dimensions__d_list"] = []
        for i in range(6):  # Разворачиваем список до 6 элементов
            flat_data[f"properties__dimensions__d_list__{i}"] = None
        flat_data["properties__dimensions__all_units_parsed"] = None

    # Обработка списка art_codes
    flat_data["properties__art_codes"] = product.properties.art_codes
    for i in range(6):  # Разворачиваем список до 6 элементов
        flat_data[f"properties__art_codes__{i}"] = product.properties.art_codes[i] if i < len(
            product.properties.art_codes) else None

    # Обработка списка category_list_raw
    flat_data["properties__category_list_raw"] = product.properties.category_list_raw
    for i in range(6):  # Разворачиваем список до 6 элементов
        flat_data[f"properties__category_list_raw__{i}"] = product.properties.category_list_raw[i] if i < len(
            product.properties.category_list_raw) else None

    # Возвращаем плоскую модель, создавая экземпляр ProductFlat
    return ProductFlat(**flat_data)
