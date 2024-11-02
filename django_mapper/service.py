from sqlalchemy import or_, select
from sqlalchemy.orm import Session, aliased

from db_populate.models import Match as SaMatch
from db_populate.models import Product as SaProduct
from db_populate.session import db_session_as_kwarg
from parsers.runnures.schemas.product import StoreEnum


@db_session_as_kwarg
def get_next_product(store: StoreEnum, session: Session) -> int:
    match_alias = aliased(SaMatch)

    query = session.scalars(
        select(SaProduct.id)
        .outerjoin(match_alias, or_(SaProduct.id == match_alias.product_1_id, SaProduct.id == match_alias.product_2_id))
        .filter(match_alias.product_1_id.is_(None))
        .filter(SaProduct.store == store)
        .limit(1)
    )
    sa_result: int | None = query.one_or_none()
    if sa_result is None:
        raise ValueError("No next product found")

    return sa_result
