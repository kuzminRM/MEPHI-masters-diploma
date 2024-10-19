import datetime
import logging
import re
from typing import Generator
from uuid import uuid4

import requests
from bs4 import BeautifulSoup
from requests import Response, ReadTimeout

from core.logging import service_log, add_file_log
from parsers.runnures.obi.get_top_categories import category_links
from parsers.runnures.schemas.product import StoreEnum, Product, CategoryEnum, PropertiesData, MassData, VolumeData, \
    DimensionsData
from parsers.runnures.schemas.product_flat import flatten_product, ProductFlat
from parsers.runnures.utils.common import get_int_from_string
from parsers.runnures.utils.csv import CsvWriter
from parsers.runnures.utils.units import get_num_and_unit, mass_unit_map, volume_unit_map, dimensions_unit_map

logger = logging.getLogger(__name__)
STORE = StoreEnum.OBI
BASE_URL = 'https://obi.ru'
start_from_page: int | None = None
start_from_page_for_category_url: str | None = None


def start_parser():
    csv_product_writer: CsvWriter[ProductFlat] = CsvWriter('products.csv', ProductFlat)
    counter = 0
    for category_name, category_link in category_links.items():
        logger.info(f'start category "{category_name}" - {category_link}')
        for product_url in get_products_list(category_link):
            product: Product | None = parse_product(product_url)
            if product:
                csv_product_writer.write_line(flatten_product(product))
                counter += 1
            if counter % 100 == 0:
                logger.info(f'####################################### Parsed {counter} products #######################################')


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


def get_product_page_url(category_link, page) -> str:
    return f'{category_link}?page={page}'


def get_products_list(category_link) -> Generator[str, None, None]:
    current_page = 1
    total_pages = 1
    if start_from_page_for_category_url == category_link and start_from_page:
        current_page = start_from_page
        total_pages = start_from_page
    total_product_num: int | None = None
    while current_page <= total_pages:
        page_url = get_product_page_url(category_link, current_page)
        logger.info(f'calling page {current_page} of {total_pages} [#{total_product_num}] in {category_link}')
        response: Response | None = call_api(page_url)
        current_page += 1
        if response:
            soup = BeautifulSoup(response.text, "html.parser")
            total_product_num_tag_list = soup.select('#__next > main > div > div > div > aside > p')
            if len(total_product_num_tag_list) == 1:
                total_product_num: int | None = get_int_from_string(total_product_num_tag_list[0].text)
                if total_product_num:
                    total_pages = total_product_num // 40 + 1
                    product_links = soup.select('#__next > main > div > div > div > div > div > div > div > a')
                    for product_link in product_links:
                        yield get_product_url(product_link.get('href'))
            else:
                logger.error(f'Error 4894: no total product number tag {page_url}')
        else:
            logger.error(f'Error 0176: no response {page_url}')


def get_product_url(url: str) -> str:
    return BASE_URL + url


def parse_product(product_url: str) -> Product | None:
    logger.info(f'calling product {product_url}')
    try:
        response: Response | None = call_api(product_url)
        if response is None:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.select('#__next > main > section > div > div > article > h2')[0].text
        price = get_int_from_string(soup.select('#__next > main > section > div > div > article > div > div > div > div > div > div > div > div > span')[0].text)

        description_selector = soup.find(id='Description')
        description_text: str | None = None
        if description_selector:
            description_text = description_selector.text.removeprefix('Описание')

        images_list_selector = soup.select('#__next > main > section > div > div > div > div > div > div > div > div > div > div > div > div > picture')
        images_list = []
        url_regexp = re.compile(r'https://\S+')
        for image_selector in images_list_selector:
            match = url_regexp.search(str(image_selector))
            if not match:
                continue
            images_list.append(match[0])

        product = Product(
            uid=str(uuid4()),
            store=STORE,
            title=title,
            url=product_url,
            category=CategoryEnum.NDY,
            description=description_text,
            images=images_list,
            price=price,
            properties=define_properties(soup, product_url),
        )
        return product
    except Exception as e:
        logger.error(f'Error 0174: parsing product {product_url}, {e.__repr__()}', exc_info=True)
        return None


def define_properties(soup, url) -> PropertiesData:
    properties_block = soup.find(id='Characteristics')
    as_text = properties_block.text.strip()
    properties_dict: dict[str, str] = {}
    try:
        for property_table in properties_block.find_all('dl', elem="Attributes"):
            for property_ in property_table.find_all('div'):
                property_tuple = tuple(property_.children)
                if len(property_tuple) == 2 and property_tuple[0] and property_tuple[1]:
                    properties_dict[property_tuple[0].text.strip()] = property_tuple[1].text.strip()

        as_text_from_dict = ', '.join(map(lambda x: f'{x[0]}: {x[1]}', properties_dict.items()))
        if as_text_from_dict:
            as_text = as_text_from_dict

        mass_raw = properties_dict.get('Вес') or properties_dict.get('Вес брутто')
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
        primary_dimensions_name_set = None
        # "Длина" скорее всего нет на сайте
        dimension_property_names = {'Ширина', 'Высота', 'Глубина', 'Длина', 'Толщина'}
        dimension_property_names_second = {'Ширина брутто', 'Высота брутто', 'Глубина брутто', 'Длина брутто', 'Толщина брутто'}
        if set(properties_dict.keys()) & dimension_property_names:
            primary_dimensions_name_set = dimension_property_names
        if set(properties_dict.keys()) & dimension_property_names_second:
            primary_dimensions_name_set = dimension_property_names_second
        if primary_dimensions_name_set:
            dimensions_list_values = []
            dimensions_list_units = []
            dimensions_list_raw = []
            for dimension_property_name in primary_dimensions_name_set:
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

        color = properties_dict.get('Основной цвет')
        if color:
            color = color.lower()

        art_codes = []
        art_code_block = soup.select('#__next > main > section > div > div > article > section > span > span')
        if art_code_block and art_code_block[0]:
            local_art = art_code_block[0].text.strip()
            if local_art:
                art_codes.append(local_art)
        model_name = properties_dict.get('Модель')
        if model_name:
            art_codes.append(model_name)
        properties_art = properties_dict.get('Артикул')  # скорее всего нет на сайте
        if properties_art:
            art_codes.append(properties_art)

        category_list_raw = [item.text for item in soup.find('nav', attrs={"aria-label": "Breadcrumbs navigation"}).find_all('a')[1:]][::-1]

        return PropertiesData(
            as_text=as_text,
            as_dict=properties_dict if properties_dict else None,
            brand=properties_dict.get('Бренд'),
            label=properties_dict.get('Модель') or properties_dict.get('Наименование товара'),
            country=None,
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
            as_text=as_text,
            as_dict=properties_dict if properties_dict else None,
        )


if __name__ == '__main__':
    service_log()
    add_file_log()
    datetime_start = datetime.datetime.now()
    logger.info('start')
    start_parser()
    datetime_end = datetime.datetime.now()
    logger.info(f'end | runtime: {datetime_end - datetime_start}')