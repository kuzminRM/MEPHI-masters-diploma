from enum import StrEnum

from pydantic import BaseModel


class StoreEnum(StrEnum):
    STROYDVOR = 'STROYDVOR'

class CategoryEnum(StrEnum):
    PLASTER = 'штукатурка'


class Product(BaseModel):
    store: StoreEnum
