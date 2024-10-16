import datetime
import logging
import re
from typing import Generator
from uuid import uuid4

import requests
from bs4 import BeautifulSoup

from core.logging import service_log, add_file_log
from requests import Response, ReadTimeout

from core.root_path import ROOT_PATH
from parsers.runnures.schemas.product import Product, StoreEnum, PropertiesData, MassData, \
    DimensionsData, VolumeData, CategoryEnum
from parsers.runnures.schemas.product_flat import ProductFlat, flatten_product
from parsers.runnures.schemas.stroydvor.categories import Category
from parsers.runnures.utils.csv import CsvReader, CsvWriter
from parsers.runnures.utils.pydantic import BaseModelCamelToSnake
from parsers.runnures.utils.units import mass_unit_map, dimensions_unit_map, volume_unit_map, get_num_and_unit

logger = logging.getLogger(__name__)
CATEGORIES_FILE_NAME = ROOT_PATH + '/parsers/runnures/stroydvor/data/2024-10-12_13-35_bottom_categories_reverse.csv'
STORE = StoreEnum.STROYDVOR


class PaginationProductPageApiData(BaseModelCamelToSnake):
    current_page: int
    page_size: int
    total_pages: int
    total_results: int


class SingleProductPageApiData(BaseModelCamelToSnake):
    code: str
    slug: str


class ProductPageApiData(BaseModelCamelToSnake):
    pagination: PaginationProductPageApiData
    products: list[SingleProductPageApiData]


def start_parser():
    csv_category_reader: CsvReader[Category] = CsvReader(CATEGORIES_FILE_NAME, Category)
    csv_product_writer: CsvWriter[ProductFlat] = CsvWriter('products.csv', ProductFlat)
    counter = 0
    for category in csv_category_reader:
        logger.info(f'start category {category.name}')
        for api_product in get_products_list(category):
            product: Product | None = None
            try:
                product = parse_product(api_product)
            except Exception as e:
                logger.error(f'Error 0174: parsing product {api_product.slug}-{api_product.code}, {e.__repr__()}', exc_info=True)

            if product:
                csv_product_writer.write_line(flatten_product(product))
                counter += 1
            if counter % 100 == 0:
                logger.info(f'####################################### Parsed {counter} products #######################################')


def parse_product(api_product: SingleProductPageApiData) -> Product | None:
    url = get_product_url(api_product)
    logger.info(f'calling product {url}')
    response: Response | None = call_api(url)
    if response is None:
        return

    soup = BeautifulSoup(response.text, "html.parser")
    digit_regexp = re.compile(r'\d+')
    try:
        summary_block = soup.find('cx-page-slot', position='Summary')
        price_block = soup.find('sd-available-price')
        description_block = soup.find(id='ProductDetailsTabComponent_tab').find(class_='content')
        images_block = soup.find('sd-product-images')
        images_carousel = images_block.find(class_='carousel-panel')
        if images_carousel:
            images_list = [img.get('src') for img in images_carousel.find_all('img')]
        else:
            images_list = [img.get('src') for img in images_block.find_all('img')]

        description: str | None = None
        if description_block:
            description = description_block.select('div > sd-spoiler > div > div')[0].text.strip()

        if price_block:
            price = digit_regexp.search(price_block.find('span', class_='main').text)[0]
        else:
            price = digit_regexp.search(soup.find('div', class_='price').text)[0]

        product = Product(
            uid=str(uuid4()),
            store=STORE,
            title=summary_block.find('h1').text.strip(),
            url=url,
            category=CategoryEnum.NDY,
            description=description,
            images=images_list,
            price=price,
            properties=define_properties(soup, url),
        )
        return product
    except Exception as e:
        logger.error(f'Error 9873: parsing product {url}, {e.__repr__()}', exc_info=True)
        return


def define_properties(soup, url) -> PropertiesData:
    digit_regexp = re.compile(r'\d+')
    summary_block = soup.find('cx-page-slot', position='Summary')
    properties_block = soup.find('sd-product-attributes-view')
    properties_dict: dict[str, str] = {}
    try:
        for property_ in properties_block.find_all('li'):
            property_tuple = tuple(property_.children)
            if len(property_tuple) == 2 and property_tuple[0] and property_tuple[1]:
                properties_dict[property_tuple[0].text.strip()] = property_tuple[1].text.strip()

        mass_raw = properties_dict.get('Вес')
        mass = None
        if mass_raw:
            mass_num, mass_unit = get_num_and_unit(mass_raw, mass_unit_map)
            mass = MassData(
                raw=mass_raw,
                num=mass_num,
                unit=mass_unit,
            )

        volume_raw = properties_dict.get('Объем')
        volume = None
        if volume_raw:
            volume_num, volume_unit = get_num_and_unit(volume_raw, volume_unit_map)
            volume = VolumeData(
                raw=volume_raw,
                num=volume_num,
                unit=volume_unit,
            )

        dimensions = None
        dimension_property_names = {'Ширина', 'Высота', 'Длина', 'Толщина', 'Толщина металла'}
        if set(properties_dict.keys()) & dimension_property_names:
            dimensions_list_values = []
            dimensions_list_units = []
            dimensions_list_raw = []
            for dimension_property_name in dimension_property_names:
                d_raw = properties_dict.get(dimension_property_name)
                if d_raw:
                    dimensions_list_raw.append(f'{dimension_property_name} {d_raw}')
                    d_value, d_unit = get_num_and_unit(d_raw, dimensions_unit_map)
                    if d_value:
                        dimensions_list_values.append(d_value)
                        dimensions_list_units.append(d_unit)
            dimensions_list_values.sort(reverse=True)
            dimensions_raw = ', '.join(dimensions_list_raw)
            dimensions = DimensionsData(
                raw=dimensions_raw if dimensions_raw else None,
                d_list=dimensions_list_values,
                all_units_parsed=all(dimensions_list_units),
            )

        color = properties_dict.get('Цвет')
        if color:
            color = color.lower()

        art_codes = []
        local_art = digit_regexp.search(summary_block.find('span', class_='code').text)[0]
        if local_art:
            art_codes.append(local_art)
        properties_art = properties_dict.get('Артикул')
        if properties_art:
            art_codes.append(properties_art)
        model_name = properties_dict.get('Модель')
        if model_name:
            art_codes.append(model_name)

        category_list_raw = [item.text for item in soup.find('nav').find_all('a')[1:]][::-1]

        return PropertiesData(
            as_text=properties_block.text.strip(),
            as_dict=properties_dict if properties_dict else None,
            brand=properties_dict.get('Бренд'),
            label=properties_dict.get('Название') or properties_dict.get('Тип') or properties_dict.get('Модель'),
            country=properties_dict.get('Страна производитель'),
            color=color,
            material=properties_dict.get('Материал'),
            mass=mass,
            volume=volume,
            dimensions=dimensions,
            art_codes=art_codes,
            category_list_raw=category_list_raw,
        )
    except Exception as e:
        logger.error(f'Error 4963: parsing properties of {url}, {e.__repr__()}', exc_info=True)
        return PropertiesData(
            as_text=properties_block.text.strip(),
            as_dict=properties_dict if properties_dict else None,
        )


def call_api(url: str) -> Response | None:
    try:
        response = requests.get(url, timeout=5)
    except ReadTimeout as e:
        logger.error(f'Error 4864: red timeout {url}, {e.__repr__()}')
        return None
    if response.status_code != 200:
        logger.error(f'Error 6548: HTTP status code {response.status_code} {url}')
        return None
    return response


def get_products_list(category: Category) -> Generator[SingleProductPageApiData, None, None]:
    total_pages = 1
    current_page = 0
    while current_page < total_pages:
        url = get_products_list_url(category.code, current_page)
        current_page += 1
        logger.info(f'calling page {current_page} of {total_pages} in {category.name}')
        response: Response | None = call_api(url)
        if response is None:
            continue
        try:
            data: ProductPageApiData = ProductPageApiData(**response.json())
            total_pages = data.pagination.total_pages
            for product in data.products:
                yield product
        except Exception as e:
            logger.error(f'Error 1678: could not get products from page {url} {e.__repr__()}', exc_info=True)


def get_products_list_url(code: str, page: int) -> str:
    return (
        'https://api-ecomm.sdvor.com/occ/v2/sd/products/search?'
        'fields=algorithmsForAddingRelatedProducts%2CcategoryCode%2Cproducts(code%2Cslug)%2Cpagination(DEFAULT)&'
        f'currentPage={page}&'
        'pageSize=18&'
        'sort=personal-price-asc&'
        f'facets=allCategories%3A{code}&'
        'lang=ru&'
        'curr=RUB&'
        'deviceType=tablet&'
        'baseStore=moscow'
    )


def get_product_url(api_product: SingleProductPageApiData) -> str:
    return f'https://www.sdvor.com/moscow/product/{api_product.slug}-{api_product.code}'


if __name__ == '__main__':
    service_log()
    add_file_log()
    datetime_start = datetime.datetime.now()
    logger.info('start')
    start_parser()
    datetime_end = datetime.datetime.now()
    logger.info(f'end | runtime: {datetime_end - datetime_start}')
