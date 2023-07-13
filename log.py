import logging
from enum import Enum, auto


class Log:
    __logger = None
    __handler = None
    __formatter = None

    def __init__(self, module=__name__, filename='log.txt'):
        self.__logger = logging.getLogger(module)
        self.__set_level()
        self.__set_formatter()
        self.__set_handler(filename)
        self.__add_handler()

    def __set_level(self):
        self.__logger.setLevel(logging.INFO)

    def __set_handler(self, filename):
        self.__handler = logging.FileHandler(filename)
        self.__handler.setFormatter(self.__get_formatter())

    def __get_handler(self):
        return self.__handler

    def __set_formatter(self):
        self.__formatter = logging.Formatter("[%(name)s] [%(asctime)s] [%(levelname)s] %(message)s")

    def __get_formatter(self):
        return self.__formatter

    def __add_handler(self):
        self.__logger.addHandler(self.__get_handler())

    def add(self, level, msg):
        match level:
            case Levels.info:
                self.__logger.info(msg)
            case Levels.warn:
                self.__logger.warning(msg)
            case Levels.error:
                self.__logger.error(msg)
            case Levels.critical:
                self.__logger.critical(msg)
            case _:
                self.add(Levels.warn, 'Недопустимый уровень логирования!')


class Levels(Enum):
    info = auto()
    warn = auto()
    error = auto()
    critical = auto()
