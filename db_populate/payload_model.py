from pydantic import BaseModel


class PayloadModel(BaseModel):
    store: str
    properties_category_first: str | None = None
    properties_category_last: str | None = None