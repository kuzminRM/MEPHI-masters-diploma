from create_embeddings.schemas.embedding import ModelEnum, EmbeddingsFieldsEnum
from pydantic import BaseModel


class EmbeddingModelCsvFile(BaseModel):
    embedding_model_name: ModelEnum
    field: EmbeddingsFieldsEnum
    embedding_size: int
    file_path: str


embedding_size_map: dict[ModelEnum, int] = {
    ModelEnum.RUBERT_TINY_TURBO: 312,
    ModelEnum.RUBERT_TINY2: 312,
    ModelEnum.LABSE_RU_TURBO: 768,
    ModelEnum.MULTILINGUAL_E5_LARGE_INSTRUCT: 1024,
    ModelEnum.BGE_M3: 1024,
}
