import time
from pprint import pprint

from django.db import reset_queries, connection


def query_benchmark(show_sql=False):
    """Декоратор для тестирования функций на количество выполняемых запросов
    from core_apps.core.utils import query_benchmark
    @query_benchmark()
    """

    def pseudo_decorator(function, *ps_args, **ps_kwargs):
        def wrapper(*args, **kwargs):
            reset_queries()

            start_queries = len(connection.queries)

            start = time.perf_counter()
            result = function(*args, **kwargs)
            end = time.perf_counter()

            end_queries = len(connection.queries)
            if show_sql:
                print("___________________________")
                pprint(connection.queries)
            print("___________________________")
            print(f"Function : {function.__name__}")
            print(f"Number of Queries : {end_queries - start_queries}")
            print(f"Finished in : {(end - start):.4f}s")
            print("___________________________")
            return result

        return wrapper

    return pseudo_decorator


def generate_key_mapping(model) -> dict[str, str]:
    key_mapping = {}
    for field in model.__fields__:
        # Replace '__' with '_' for each field name
        mapped_key = field.replace('__', '_')
        key_mapping[mapped_key] = field
    return key_mapping


# Function to map keys using the auto-generated key mapping
def map_keys_for_product_flat(data: dict, model) -> dict:
    key_mapping = generate_key_mapping(model)
    return {
        key_mapping.get(k, k): v  # Use mapped key if it exists; otherwise, use original
        for k, v in data.items()
    }
