from log import Log, Levels


class Folder:
    __path = ''
    __sep = ''
    __name = ''
    __log = Log(__name__)

    def __init__(self, folder):
        if len(folder) != 3:
            self.__log.add(Levels.error, f'Экземпляр папки не создан, массив должен быть из 3-х элементов, а передано {len(folder)}')
            return
        self.__path = folder[0]
        self.__sep = folder[1]
        self.__name = folder[2]

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_path(self, path):
        self.__path = path

    def get_path(self):
        return self.__path

    def set_sep(self, sep):
        self.__sep = sep

    def __str__(self):
        return f'{self.__path} {self.__sep} {self.__name}'
