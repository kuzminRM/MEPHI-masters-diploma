import os

from core.root_path import ROOT_PATH
from create_embeddings.schemas.embedding import ModelEnum, EmbeddingsFieldsEnum
from create_embeddings.schemas.embedding_model import EmbeddingModelCsvFile, embedding_size_map


def get_all_fies(add_root_path: bool = True) -> list[str]:
    files_dir_path = ROOT_PATH + '/create_embeddings/data/'
    return [files_dir_path + f for f in os.listdir(files_dir_path)]


def get_all_csv_files(add_root_path: bool = True) -> list[str]:
    return [f for f in get_all_fies(add_root_path) if f.endswith('.csv')]


def get_csv_file_info(path: str) -> EmbeddingModelCsvFile:
    date_time, info = path.split('_products_embeddings_')
    info_list = info.split('_')
    store = info_list[0]
    field = EmbeddingsFieldsEnum(info_list[1])
    model = "_".join(info_list[2:]).removesuffix('.csv')
    model_enum = getattr(ModelEnum, model)
    return EmbeddingModelCsvFile(
        embedding_model_name=model_enum,
        field=field,
        embedding_size=embedding_size_map[model_enum],
        file_path=path,
    )


def get_csv_files_info() -> list[EmbeddingModelCsvFile]:
    return [get_csv_file_info(path) for path in get_all_csv_files()]
