import re

from bs4 import Tag


def get_digits_from_string(value: str) -> str | None:
    num_str = re.sub(r'\D', '', value)
    if not num_str:
        return None
    return num_str


def get_int_from_string(value: str) -> int | None:
    num_str = get_digits_from_string(value)
    if not num_str:
        return None
    return int(num_str)


def get_from_selector(selector: list[Tag]) -> Tag:
    if len(selector) != 1:
        raise
    return selector[0]
