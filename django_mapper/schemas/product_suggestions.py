from __future__ import annotations

from typing import TYPE_CHECKING

from django.forms import model_to_dict
from pydantic import BaseModel, Field
from qdrant_client.http.models import Record, ScoredPoint
from qdrant_client import models

from db_populate.quadrant_client import client
from django_mapper.constants import CURRENT_RIGHT_STORE
from django_mapper.utils import map_keys_for_product_flat
from parsers.runnures.schemas.product_flat import ProductFlat, ProductFlatId

if TYPE_CHECKING:
    from django_mapper.models import Product


class ProductSuggestion(BaseModel):
    product_obj: ProductFlat
    total_rank: int
    score_rubert_tiny_turbo: float | None = None
    rank_rubert_tiny_turbo: int | None = None
    score_rubert_tiny2: float | None = None
    rank_rubert_tiny2: int | None = None
    score_labse_ru_turbo: float | None = None
    rank_labse_ru_turbo: int | None = None
    score_multilingual_e5: float | None = None
    rank_multilingual_e5: int | None = None


def create_product_suggestion_list(
        hits_rubert_tiny_turbo: list[ScoredPoint],
        hits_rubert_tiny2: list[ScoredPoint] = None,
        hits_labse_ru_turbo: list[ScoredPoint] = None,
        hits_multilingual_e5: list[ScoredPoint] = None,
) -> list[ProductSuggestion]:
    from django_mapper.models import Product
    # Initialize dictionaries for scores and ranks across models
    uid_suggestion_score_map = {}
    uid_suggestion_rank_map = {}

    # Helper function to populate score and rank maps
    def process_hits(hits, model_name):
        if not hits:
            return
        for i, point in enumerate(hits):
            rank = i + 1
            uid_suggestion_score_map.setdefault(point.id, {})[model_name] = round(point.score * 100, 2)
            uid_suggestion_rank_map.setdefault(point.id, {})[model_name] = rank

    # Process each list of hits with the helper function
    process_hits(hits_rubert_tiny_turbo, 'rubert_tiny_turbo')
    process_hits(hits_rubert_tiny2, 'rubert_tiny2')
    process_hits(hits_labse_ru_turbo, 'labse_ru_turbo')
    process_hits(hits_multilingual_e5, 'multilingual_e5')

    # Get all unique UIDs from the union of all hit lists
    all_uids = set(uid_suggestion_score_map.keys())

    # Fetch product details for all unique UIDs
    product_list = Product.objects.filter(uid__in=all_uids)
    uid_product_map = {product.uid: product for product in product_list}

    # Create ProductSuggestion entries
    result = []
    for uid in all_uids:
        # Calculate sum of ranks, using 10 for any missing model rank
        total_rank = sum(
            uid_suggestion_rank_map[uid].get(model, 11) for model in
            ['rubert_tiny_turbo', 'rubert_tiny2', 'labse_ru_turbo', 'multilingual_e5']
        )

        # Prepare the ProductSuggestion attributes
        mapped_data = map_keys_for_product_flat(model_to_dict(uid_product_map[uid]), ProductFlatId)
        product_flat_id = ProductFlatId(**mapped_data)

        # Create the ProductSuggestion object with all available scores and ranks
        result.append(
            ProductSuggestion(
                product_obj=product_flat_id,
                score_rubert_tiny_turbo=uid_suggestion_score_map[uid].get('rubert_tiny_turbo'),
                rank_rubert_tiny_turbo=uid_suggestion_rank_map[uid].get('rubert_tiny_turbo'),
                score_rubert_tiny2=uid_suggestion_score_map[uid].get('rubert_tiny2'),
                rank_rubert_tiny2=uid_suggestion_rank_map[uid].get('rubert_tiny2'),
                score_labse_ru_turbo=uid_suggestion_score_map[uid].get('labse_ru_turbo'),
                rank_labse_ru_turbo=uid_suggestion_rank_map[uid].get('labse_ru_turbo'),
                score_multilingual_e5=uid_suggestion_score_map[uid].get('multilingual_e5'),
                rank_multilingual_e5=uid_suggestion_rank_map[uid].get('multilingual_e5'),
                total_rank=total_rank,
            )
        )

    # Sort results by the computed total rank
    result.sort(key=lambda suggestion: suggestion.total_rank)

    return result


def query_product_suggestions(uid: str, collection_name: str, limit: int = 10) -> list[ScoredPoint]:
    vector_data_list_tiny_turbo = client.retrieve(
        collection_name=collection_name,
        ids=[uid],
        with_vectors=True
    )
    if len(vector_data_list_tiny_turbo) != 1:
        ValueError(f'Wrong number of vectors. Expected 1, got {len(vector_data_list_tiny_turbo)}')
    vector_data: Record = vector_data_list_tiny_turbo[0]
    hits: list[ScoredPoint] = client.query_points(
        collection_name=collection_name,
        query=vector_data.vector,
        query_filter=models.Filter(
            must=[models.FieldCondition(key="store", match=models.MatchValue(value=CURRENT_RIGHT_STORE))]
        ),
        limit=limit,
    ).points
    return hits


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
        hits_rubert_tiny_turbo = query_product_suggestions(main_product.uid, "RUBERT_TINY_TURBO_TITLE")
        hits_rubert_tiny2 = query_product_suggestions(main_product.uid, "RUBERT_TINY2_TITLE")
        hits_labse_ru_turbo = query_product_suggestions(main_product.uid, "LABSE_RU_TURBO_TITLE")
        hits_multilingual_e5 = query_product_suggestions(main_product.uid, "MULTILINGUAL_E5_LARGE_INSTRUCT_TITLE")
        suggestion_list = create_product_suggestion_list(
            hits_rubert_tiny_turbo,
            hits_rubert_tiny2,
            hits_labse_ru_turbo,
            hits_multilingual_e5,
        )

        return cls(
            total=10,
            max_rank=1,
            max_score_rubert_tiny_turbo=1,
            max_score_rubert_tiny2=None,
            max_score_labse_ru_turbo=None,
            max_score_multilingual_e5=None,
            suggestions=suggestion_list,
        )
