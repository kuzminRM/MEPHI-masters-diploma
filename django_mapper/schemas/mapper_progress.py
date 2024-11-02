from __future__ import annotations

from pydantic import BaseModel

from django_mapper.models import Product, Match
from parsers.runnures.schemas.product import StoreEnum


class MatchingProgress(BaseModel):
    total: int
    matched: int
    nomatches: int
    unmatched: int
    matched_percent: int
    nomatches_percent: int
    unmatched_percent: int

    @classmethod
    def get_progress(cls) -> MatchingProgress:
        total = Product.objects.filter(store=StoreEnum.STROYDVOR).count()
        matched = Match.objects.filter(product_2__isnull=False).count()
        nomatches = Match.objects.filter(product_2__isnull=True).count()
        unmatched = total - matched - nomatches
        matched_percent = round(matched / total * 100)
        nomatches_percent = round(nomatches / total * 100)
        unmatched_percent = 100 - matched_percent - nomatches_percent
        return cls(
            total=total,
            matched=matched,
            nomatches=nomatches,
            unmatched=unmatched,
            matched_percent=matched_percent,
            nomatches_percent=nomatches_percent,
            unmatched_percent=unmatched_percent,
        )
