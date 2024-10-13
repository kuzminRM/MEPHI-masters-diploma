import datetime
import json
import logging
from queue import Queue

import requests

from core.logging import service_log
from parsers.runnures.schemas.stroydvor.categories import Category, CategoryTreeNode
from parsers.runnures.utils.csv import CsvWriter
from parsers.runnures.utils.file import save_file, read_file

logger = logging.getLogger(__name__)


def get_categories() -> CategoryTreeNode:
    root_node: CategoryTreeNode = CategoryTreeNode(
        name='Корневой элемент',
        url='root-none',
        code='root-none',
        code_link='root-none',
        code_nav='SdCategoryNavNode',
        has_children=True,
    )
    queue: Queue[CategoryTreeNode] = Queue()
    queue.put(root_node)
    all_categories_csv_writer: CsvWriter[Category] = CsvWriter('all_categories.csv', Category)
    bottom_categories_csv_writer: CsvWriter[Category] = CsvWriter('bottom_categories.csv', Category)

    while queue.full():
        current_element: CategoryTreeNode = queue.get()
        all_categories_csv_writer.write_line(Category(**current_element.dict()))
        queue_extension_list: list[CategoryTreeNode] = parse_children(current_element, bottom_categories_csv_writer)
        for queue_extension in queue_extension_list:
            queue.put(queue_extension)
    return root_node


def call_api(code_nav: str) -> dict:
    root_url: str = get_category_url(code_nav)
    logger.info(f'{code_nav=}, {root_url=}')
    response = requests.get(root_url)
    return response.json()


def parse_children(parent_node: CategoryTreeNode, bottom_categories_csv_writer: CsvWriter) -> list[CategoryTreeNode]:
    data = call_api(parent_node.code_nav)
    if not parent_node.has_children:
        bottom_categories_csv_writer.write_line(Category(**parent_node.dict()))
        return []

    next_nodes_to_parse: list[CategoryTreeNode] = []
    for child in data['children']:
        try:
            new_node: CategoryTreeNode = CategoryTreeNode(
                name=child['entries'][0]['linkName'],
                url=child['entries'][0]['url'],
                code=child['entries'][0]['categoryCode'],
                code_link=child['entries'][0]['uid'],
                code_nav=child['uid'],
                has_children=child['hasChildren'],
            )
        except KeyError as e:
            logger.error(f'Error 6387: [{e.__repr__()}] {child=}')
            continue
        next_nodes_to_parse.append(new_node)
        parent_node.children_list.append(new_node)
    return next_nodes_to_parse


def get_category_url(code_nav: str) -> str:
    return f'https://api-ecomm.sdvor.com/occ/v2/sd/cms/menu?fields=DEFAULT&nodeId={code_nav}&level=1&lang=ru&curr=RUB&deviceType=tablet&baseStore=moscow'


def save_to_json():
    root_node = get_categories()
    save_file('stroydvor_categories_tree.json', root_node.json())


if __name__ == '__main__':
    service_log()
    datetime_start = datetime.datetime.now()
    logger.info('start')
    save_to_json()
    datetime_end = datetime.datetime.now()
    logger.info(f'end | runtime: {datetime_end - datetime_start}')
