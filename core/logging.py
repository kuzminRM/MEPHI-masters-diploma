import logging


def service_log() -> None:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def add_file_log(file_path: str = './data/log.log') -> None:
    file_handler = logging.FileHandler(file_path)
    file_handler.setLevel(logging.DEBUG)  # not working

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(file_handler)
