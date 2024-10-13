import datetime
import logging

logger = logging.getLogger(__name__)


def get_file_name(filename: str, add_timestamp: bool = True) -> str:
    timestamp: str = ''
    if add_timestamp:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M_')
    return timestamp + filename


def save_file(filename: str, file_content: str, add_timestamp: bool = True):
    filename = get_file_name(filename, add_timestamp=add_timestamp)
    logger.info(f'save to {filename=}, len={len(file_content)}')
    with open(filename, 'w') as f:
        f.write(file_content)


def read_file(filename: str) -> str:
    logger.info(f'read from {filename=}')
    with open(filename, 'r') as f:
        return f.read()
