import re
import time

from django.forms import model_to_dict
from ollama import generate
from ollama import GenerateResponse

from django_mapper.constants import CURRENT_LEFT_STORE
from django_mapper.models import Product
from django_mapper.schemas.product_suggestions import ProductSuggestions
from django_mapper.service import get_next_product
from django_mapper.utils import map_keys_for_product_flat
from llm.compare_two.latest import MODEL_NAME, AnswerEnum
from parsers.runnures.schemas.product_flat import ProductFlat, ProductFlatId

sys_prompt = """Your task is to decide if two product matches. 
There could be some difference in titles or skipped information.
Answer STRONGLY with 'Yes' or 'No', WITHOUT ANY EXPLANATIONS. After 'Yes' or 'No' write your confidence level from 0 to 100 as integer, like this 'Yes 86'
For example, this two products are not the same because of difference in number of teeth 36 vs 24 and brand. (correct answer 'No'):
Product 1: 'Title: Диск пильный по дереву 190х30 мм 36 зубьев'
Product 2: 'Title: Отрезной диск по дереву КАЛИБР 190х30 мм' 'Description: Диск для циркулярных пил с посадочным отверстием: 30 мм. Диаметр: 190 мм. Диск имеет 24 зуба. Грубый рез, высокая скорость распила. Предназначен для работы по дереву, где не требуется высокое качество реза.'
This two products are identical but they have different brand (correct answer 'No'):
Product 1: 'Title: Набор коронок Yoko по дереву 19-127 мм' 'Description: Набор коронок Yoko по дереву 19-127 мм Набор из 12 кольцевых цельнометаллических коронок по дереву'
Product 2: 'Title: Коронка по дереву ЗУБР 19-127 мм 12 шт.'
This products are the same. They have all the same properties including brand, quantity, sizes and so on (correct answer 'Yes'):
Product 1: 'Title: Коронка 57 мм 5/8" Bi-Metal Elitech 1820.061600'
Product 2: 'Title: Коронка пильная ELITECH 1820.061600 57мм 5/8" Bi-Metal'
"""


def get_prompt(product_1: ProductFlat, product_2: ProductFlat) -> str:
    return f"""{sys_prompt}
Do the following two product titles matches?
Product 1: 'Title: {product_1.title}' 'Description: {product_1.description[:200] if product_1.description else ''}' 'Specifications: Brand: {product_1.properties__brand}, Label: {product_1.properties__label}, Country: {product_1.properties__country}, Dimentions: {product_1.properties__dimensions__raw}, Weight: {product_1.properties__mass__raw}, Volume: {product_1.properties__volume__raw} Material: {product_1.properties__material}'
Product 2: 'Title: {product_2.title}' 'Description: {product_2.description[:200] if product_2.description else ''}' 'Specifications: Brand: {product_2.properties__brand}, Label: {product_2.properties__label}, Country: {product_2.properties__country}, Dimentions: {product_2.properties__dimensions__raw}, Weight: {product_2.properties__mass__raw}, Volume: {product_2.properties__volume__raw} Material: {product_2.properties__material}'"""


def next_products() -> list[tuple[ProductFlat, ProductFlat]]:
    next_product_id: int = get_next_product(CURRENT_LEFT_STORE)
    next_product_id = 5882
    print('Next product id: ', next_product_id, f'http://127.0.0.1:8000/mapper/{next_product_id}/')
    main_product_obj = Product.objects.get(pk=next_product_id)
    suggestions = ProductSuggestions.get_suggestions(main_product_obj)

    mapped_data = map_keys_for_product_flat(model_to_dict(main_product_obj), ProductFlatId)
    main_product_flat = ProductFlatId(**mapped_data)

    return [(main_product_flat, suggestion.product_obj) for suggestion in suggestions.suggestions]


def main():
    products = next_products()
    print('Length of products: ', len(products))
    print()

    start = time.time()
    match: list[ProductFlat] = []
    analog: list[ProductFlat] = []
    error: list[ProductFlat] = []
    for product_1, product_2 in products[:5]:
        compare_result = compare(product_1, product_2)
        if compare_result == AnswerEnum.YES:
            match.append(product_2)
        elif compare_result == AnswerEnum.ANALOG:
            analog.append(product_2)
        elif compare_result is None:
            error.append(product_2)

    print("\n\nOriginal: ", product_1.uid, product_1.title)
    print("Match: ", [(product.uid, product.title) for product in match])
    print("Analog: ", [(product.uid, product.title) for product in analog])
    print("Error: ", [(product.uid, product.title) for product in error])

    print("\nTotal duration:", time.time() - start)


def compare(product_1: ProductFlat, product_2: ProductFlat) -> AnswerEnum:
    prompt = get_prompt(product_1, product_2)
    print("Prompt: ", prompt.replace('\n', ''))
    response: GenerateResponse = generate(
        model=MODEL_NAME,
        prompt=prompt,
        options={
            "temperature": 0,
            # "num_predict": 5,
            "top_k": 10,
            "top_p": 0.5,
        }
    )
    print("Response: ", response.response, 'Duration: ', response.total_duration / 1e9)
    result = map_answer_to_enum(response.response)
    print("Result: ", result)
    return result


def map_answer_to_enum(answer: str) -> AnswerEnum | None:
    match = re.search(r'[a-zA-Z]+', answer)
    if not match:
        return None
    parsed_answer = match[0].lower()

    try:
        return AnswerEnum(parsed_answer)
    except ValueError:
        return None


if __name__ == '__main__':
    main()
