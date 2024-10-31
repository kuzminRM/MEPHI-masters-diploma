import json
from typing import Any

from pydantic import BaseModel, field_validator

from parsers.runnures.schemas.product import StoreEnum
from enum import StrEnum


class EmbeddingsFieldsEnum(StrEnum):
    TITLE = "title"
    DESCRIPTION = "description"


class ModelEnum(StrEnum):
    RUBERT_TINY_TURBO = 'sergeyzh/rubert-tiny-turbo'
    RUBERT_TINY2 = 'cointegrated/rubert-tiny2'
    LABSE_RU_TURBO = 'sergeyzh/LaBSE-ru-turbo'
    MULTILINGUAL_E5_LARGE_INSTRUCT = 'intfloat/multilingual-e5-large-instruct'
    BGE_M3 = 'BAAI/bge-m3'


class ProductEmbedding(BaseModel):
    uid: str
    field: EmbeddingsFieldsEnum
    store: StoreEnum
    model: ModelEnum
    embedding: list[float]

    @field_validator('embedding', mode='before')
    @classmethod
    def to_list_float(cls, value: Any) -> list[float]:
        if isinstance(value, str):
            return json.loads(value)
        return value
