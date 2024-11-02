from __future__ import annotations

from pydantic import BaseModel, Field
from qdrant_client.http.models import Record, ScoredPoint
from qdrant_client import models

from db_populate.quadrant_client import client
from django_mapper.constants import CURRENT_RIGHT_STORE
from django_mapper.models import Product, Match
from parsers.runnures.schemas.product import StoreEnum
from parsers.runnures.schemas.product_flat import ProductFlat


class ProductSuggestion(BaseModel):
    product_obj: ProductFlat
    score_rubert_tiny_turbo: float | None = None
    rank_rubert_tiny_turbo: int | None = None
    score_rubert_tiny2: float | None = None
    rank_rubert_tiny2: int | None = None
    score_labse_ru_turbo: float | None = None
    rank_labse_ru_turbo: int | None = None
    score_multilingual_e5: float | None = None
    rank_multilingual_e5: int | None = None


def create_product_suggestion_list(query_result: list[ScoredPoint]) -> list[ProductSuggestion]:
    uid_list = [point.id for point in query_result]
    product_list = Product.objects.filter(uid__in=uid_list)
    uid_product_map = {product.uid: product for product in product_list}
    uid_suggestion_score_map = {point.id: point for point in query_result}
    uid_suggestion_rank_map = {point.id: i + 1 for i, point in enumerate(query_result)}

    result = []
    for uid in uid_list:
        result.append(
            ProductSuggestion(
                product_obj=ProductFlat.model_validate(uid_product_map[uid], from_attributes=True),
                score_rubert_tiny_turbo=uid_suggestion_score_map[uid],
                rank_rubert_tiny_turbo=uid_suggestion_rank_map[uid],
            )
        )
    return result


class ProductSuggestions(BaseModel):
    total: int
    max_rank: int
    max_score_rubert_tiny_turbo: float | None
    max_score_rubert_tiny2: float | None
    max_score_labse_ru_turbo: float | None
    max_score_multilingual_e5: float | None
    suggestions: list[ProductSuggestion] = Field(default_factory=list)

    @classmethod
    def get_suggestions(cls, main_product: Product) -> ProductSuggestions:
        vector_data_list = client.retrieve(
            collection_name="RUBERT_TINY_TURBO_TITLE",
            ids=[main_product.uid],
            with_vectors=True
        )
        if len(vector_data_list) != 1:
            ValueError(f'Wrong number of vectors. Expected 1, got {len(vector_data_list)}')
        vector_data: Record = vector_data_list[0]

        hits: list[ScoredPoint] = client.query_points(
            collection_name="RUBERT_TINY_TURBO_TITLE",
            query=vector_data.vector,
            query_filter=models.Filter(
                must=[models.FieldCondition(key="store", match=models.MatchValue(value=CURRENT_RIGHT_STORE))]
            ),
            limit=10,
        ).points

        suggestion_list = create_product_suggestion_list(hits)

        return cls(
            total=10,
            max_rank=1,
            max_score_rubert_tiny_turbo=1,
            max_score_rubert_tiny2=None,
            max_score_labse_ru_turbo=None,
            max_score_multilingual_e5=None,
            suggestions=suggestion_list,
        )
