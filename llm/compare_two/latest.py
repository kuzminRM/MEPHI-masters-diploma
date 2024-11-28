from enum import StrEnum

from .v1 import compare as compare_v1

MODEL_NAME = 'llama3.1:8b-instruct-q8_0'


class AnswerEnum(StrEnum):
    YES = 'yes'
    NO = 'no'
    ANALOG = 'analog'


def compare(a, b):
    return compare_v1(a, b)
