import csv
from typing import TypeVar, Iterator, Generic

from pydantic import BaseModel

from parsers.runnures.utils.file import get_file_name

T = TypeVar('T', bound=BaseModel)


class CsvWriter(Generic[T]):
    def __init__(self, filename: str, header_model: type[T]):
        """
        Инициализация CsvWriter.

        :param filename: Имя файла, в который будут записываться данные.
        :param header_model: Pydantic модель, представляющая заголовки CSV.
        """
        self.filename = get_file_name(filename)
        self.header_model = header_model

        # Извлечение полей модели для создания заголовков
        self.headers = list(header_model.__fields__.keys())

        # Открываем файл в режиме добавления (append) и создаем writer
        self.file = open(self.filename, mode='a', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)

        # Проверяем, если файл новый (пустой), то записываем заголовки
        if self.file.tell() == 0:  # Проверка, если указатель на начало файла
            self.writer.writerow(self.headers)

    def write_lines(self, data: list[T]):
        """
        Запись строк данных в CSV файл.

        :param data: Список pydantic моделей, представляющих строки для записи.
        """
        # Проверка, что каждая запись является экземпляром той же модели, что и заголовки
        for item in data:
            if not isinstance(item, self.header_model):
                raise ValueError(f"Все элементы должны быть экземплярами {self.header_model.__name__}")

        # Запись всех строк данных в CSV одним вызовом writerows
        self.writer.writerows([item.dict().values() for item in data])

    def write_line(self, item: T):
        if not isinstance(item, self.header_model):
            raise ValueError(f"Элемент должен быть экземпляром {self.header_model.__name__}")
        self.writer.writerow(item.dict().values())

    def __del__(self):
        """
        Закрытие файла при удалении объекта.
        """
        if not self.file.closed:
            self.file.close()


class CsvReader(Generic[T]):
    def __init__(self, filename: str, model: type[T]):
        """
        Инициализация CsvReader.

        :param filename: Имя файла для чтения данных.
        :param model: Pydantic модель, которая будет использоваться для валидации данных.
        """
        self.filename = filename
        self.model = model

    def __iter__(self) -> Iterator[T]:
        """
        Генератор, возвращающий объекты Pydantic модели для каждой строки в CSV файле.

        :return: Итератор объектов Pydantic модели.
        """
        with open(self.filename, mode='r', newline='', encoding='utf-8') as f:
            reader: csv.DictReader[dict] = csv.DictReader(f)  # type: ignore

            # Проход по строкам файла и создание объектов модели
            for row in reader:
                # Преобразование данных строки в объект Pydantic модели
                yield self.model(**row)
