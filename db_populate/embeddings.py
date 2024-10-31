import datetime
import json
import logging

from qdrant_client import QdrantClient, models
from qdrant_client.http.exceptions import UnexpectedResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.logging import service_log, add_file_log
from create_embeddings.schemas.embedding import EmbeddingsFieldsEnum, ModelEnum, ProductEmbedding
from create_embeddings.schemas.embedding_model import EmbeddingModelCsvFile
from create_embeddings.utils import get_csv_files_info
from db_populate.models import Product
from db_populate.payload_model import PayloadModel
from db_populate.session import db_session_as_kwarg
from parsers.runnures.utils.csv import CsvReader
from quadrant_client import client

logger = logging.getLogger(__name__)
BATCH_SIZE = 100


def get_collection_name(field: EmbeddingsFieldsEnum, model: ModelEnum) -> str:
    return f"{model.name}_{field.name}"


def get_payload_by_uid(uid: str, session: Session) -> dict[str, str]:
    result = session.scalars(select(Product).filter(Product.uid == uid).limit(1)).one_or_none()
    if result is None:
        return {}

    properties_category_list = result.properties_category_list_raw
    if len(properties_category_list) == 0:
        properties_category_first, properties_category_last = None, None
    else:
        properties_category_first, properties_category_last = properties_category_list[0], properties_category_list[-1]
    return PayloadModel(
        store=result.store,
        properties_category_first=properties_category_first,
        properties_category_last=properties_category_last,
    ).dict()


@db_session_as_kwarg
def populate_embeddings(session: Session):
    csv_files_info: list[EmbeddingModelCsvFile] = get_csv_files_info()

    for csv_file_info in csv_files_info:
        collection_name = get_collection_name(csv_file_info.field, csv_file_info.embedding_model_name)
        logger.info(f'start new file {csv_file_info.file_path.split("/")[-1]}')
        try:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=csv_file_info.embedding_size, distance=models.Distance.COSINE, on_disk=True
                ),
                hnsw_config=models.HnswConfigDiff(m=64, ef_construct=512, on_disk=True),
                optimizers_config=models.OptimizersConfigDiff(indexing_threshold=0),
            )
            logger.info(f'collection created {collection_name}')
        except UnexpectedResponse as e:
            logger.info(f'collection already exists {collection_name}')

        batch = []
        i = 0
        csv_reader: CsvReader[ProductEmbedding] = CsvReader(csv_file_info.file_path, ProductEmbedding)
        for uid_vector in csv_reader:
            i += 1
            batch.append(models.PointStruct(
                id=uid_vector.uid,
                vector=uid_vector.embedding,
                payload=get_payload_by_uid(uid_vector.uid, session),
            ))
            if len(batch) == BATCH_SIZE:
                logger.info(f'upload {i} points to collection {collection_name}')
                client.upload_points(
                    collection_name=collection_name,
                    points=batch,
                )
                batch = []

        client.upload_points(
            collection_name=collection_name,
            points=batch,
        )
        batch = []


def set_indexing_threshold():
    logger.info('start indexing')
    csv_files_info: list[EmbeddingModelCsvFile] = get_csv_files_info()
    collection_names_set = set()
    for csv_file_info in csv_files_info:
        collection_names_set.add(
            get_collection_name(csv_file_info.field, csv_file_info.embedding_model_name)
        )

    for collection_name in collection_names_set:
        logger.info(f'set indexing_threshold for {collection_name}')
        client.update_collection(
            collection_name=collection_name,
            optimizer_config=models.OptimizersConfigDiff(indexing_threshold=10_000),
        )


if __name__ == '__main__':
    service_log()
    logging.getLogger("httpx").setLevel(logging.WARNING)
    add_file_log('./db_populate/data/embeddings.log')
    datetime_start = datetime.datetime.now()
    logger.info('start')
    populate_embeddings()
    set_indexing_threshold()
    datetime_end = datetime.datetime.now()
    logger.info(f'end | runtime: {datetime_end - datetime_start}')
