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
from parsers.runnures.schemas.product import StoreEnum, Product, CategoryEnum
from parsers.runnures.schemas.product_flat import flatten_product, ProductFlat
from parsers.runnures.utils.common import get_int_from_string
from parsers.runnures.utils.csv import CsvWriter

logger = logging.getLogger(__name__)
STORE = StoreEnum.OBI


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
                break


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


def get_product_url(category_link, page) -> str:
    return f'{category_link}?page={page}'


def get_products_list(category_link) -> Generator[str, None, None]:
    current_page = 1
    total_pages = 1
    total_product_num: int | None = None
    while current_page <= total_pages:
        page_url = get_product_url(category_link, current_page)
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
                        yield product_link.get('href')
            else:
                logger.error(f'Error 4894: no total product number tag {page_url}')
        else:
            logger.error(f'Error 0176: no response {page_url}')


def parse_product(product_url: str) -> Product | None:
    logger.info(f'calling product {product_url}')
    try:
        response: Response | None = call_api(product_url)
        if response is None:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.select('#__next > main > section > div > div > article > h2')[0].text
        price = get_int_from_string(soup.select('#__next > main > section > div > div > article > div > div > div > div > div > div > div > div > span')[0].text)

        description_selector = soup.select('#Description > section > div > div > div')
        description_text: str | None = None
        if description_selector:
            description_text = description_selector[0].text

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
            properties='',  #TODO
        )
        return product
    except Exception as e:
        logger.error(f'Error 0174: parsing product {product_url}, {e.__repr__()}', exc_info=True)
        return None


if __name__ == '__main__':
    service_log()
    add_file_log()
    datetime_start = datetime.datetime.now()
    logger.info('start')
    # start_parser()
    datetime_end = datetime.datetime.now()
    logger.info(f'end | runtime: {datetime_end - datetime_start}')