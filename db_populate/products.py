import datetime
import logging

from sqlalchemy.orm import Session

from core.logging import service_log, add_file_log
from db_populate.models import Product
from db_populate.session import db_session_as_kwarg
from parsers.runnures.schemas.product_flat import ProductFlat
from parsers.runnures.utils.csv import CsvReader

logger = logging.getLogger(__name__)

files = [
    '/home/roman/PycharmProjects/personal/diploma/parsers/runnures/stroydvor/data/products.csv',
    '/home/roman/PycharmProjects/personal/diploma/parsers/runnures/obi/data/products_merged.csv'
]
batch_size = 100


def pydantic_to_sqlalchemy(pydantic_model: ProductFlat) -> Product:
    pydantic_dict_real = pydantic_model.dict()
    pydantic_dict_new = {}

    for key, value in pydantic_dict_real.items():
        new_key = key.replace("__", "_")
        pydantic_dict_new[new_key] = value
    return Product(**pydantic_dict_new)


@db_session_as_kwarg
def populate_products(session: Session):
    for file in files:
        logger.info(f'Start populate from {file}')
        csv_category_reader: CsvReader[ProductFlat] = CsvReader(file, ProductFlat, none_on_error=True)
        batch: list[Product] = []
        i = 0
        ve = 0
        for row in csv_category_reader:
            if row is None:
                ve += 1
                continue
            i += 1
            batch.append(pydantic_to_sqlalchemy(row))
            if len(batch) == batch_size:
                logger.info(f'element  {i} written')
                session.add_all(batch)
                session.commit()
                batch = []

        logger.info(f'element  {i} written')
        session.add_all(batch)
        session.commit()
        batch = []
    logger.info(f'Validation errors total: {ve}')


if __name__ == '__main__':
    service_log()
    add_file_log('./db_populate/data/products.log')
    populate_products()
