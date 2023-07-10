from log import Log, Levels
from folder import Folder
from message import Message
import imaplib
from config import config_vars


class Mail:
    __server = ''
    __login = ''
    __password = ''
    __log = None
    __imap = None
    __folders = list()
    __folder_name = ''
    __from_field = ''
    __array_messages = list()
    __messages_count = 0
    __message = None

    def __init__(self):
        self.__set_fields_from_config()
        self.__log = Log(__name__, 'log.txt')
        self.__imap = imaplib.IMAP4_SSL(self.__get_email_server())
        self.__array_messages = list()
        self.__message = None
        self.__messages_count = 0

    def __set_fields_from_config(self):
        self.__server = config_vars['email_server']
        self.__login = config_vars['email_login']
        self.__password = config_vars['email_password']
        self.__folder_name = config_vars['folder']
        self.__from_field = config_vars['from']

    def __get_email_server(self):
        return self.__server

    def __get_email_login(self):
        return self.__login

    def __get_email_password(self):
        return self.__password

    def __add_folder(self, folder):
        self.__folders.append(folder)

    def get_all_messages(self):
        return self.__array_messages

    def get_messages_count(self):
        return self.__messages_count

    def __connect(self):
        try:
            self.__log.add(Levels.info, 'Подключаемся к почте...')
            self.__set_fields_from_config()
            self.__imap.login(self.__get_email_login(), self.__get_email_password())
            self.__log.add(Levels.info, 'Подключение прошло успешно')
        except Exception as e:
            self.__log.add(Levels.critical, f'Подключение не удалось из-за ошибки:\n{e}')

    def __get_all_folders(self):
        self.__log.add(Levels.info, 'Получаем список папок...')
        res, resp = self.__imap.list()
        if res == 'OK':
            self.__log.add(Levels.info, 'Список папок успешно получен')
            for folder in resp:
                self.__add_folder(Folder(folder.decode('utf-8').split()))
            self.__log.add(Levels.info, 'Список доступных папок:')
            for f in self.__folders:
                self.__log.add(Levels.info, f)
        else:
            self.__log.add(Levels.error, f'Ошибка получения списка папок {res}:\n{resp.decode("utf-8")}')

    def __open_folder(self):
        self.__log.add(Levels.info, f'Подключаемся к папке {self.__folder_name}...')
        res, resp = self.__imap.select(self.__folder_name)
        if res == 'OK':
            self.__log.add(Levels.info, f'Подключение к папке {self.__folder_name} прошло успешно')
        else:
            self.__log.add(Levels.error, f'Не удалось подключиться к папке {self.__folder_name}. Проверьте имя в конфиге')

    def __get_unread_messages(self):
        self.__log.add(Levels.info, f'Ищем непрочитанные сообщения в папке {self.__folder_name}...')
        res, resp = self.__imap.uid('search', None, 'UNSEEN')
        self.__array_messages = resp[0].split()
        self.__messages_count = len(self.__array_messages)
        if res == 'OK':
            self.__log.add(Levels.info, f'Непрочитанных сообщений в папке {self.__folder_name} - {len(self.__array_messages)}')
        else:
            self.__log.add(Levels.error, f'Не удалось получить непрочитанные сообщения из папки {self.__folder_name}:\n{resp[0].decode("utf-8")}')

    def get_message_data(self, index):
        # while i > -len(self.__array_messages):
        mess_id = self.__array_messages[index]
        message = Message(mess_id, self.__imap)
        self.set_message(message)
        if message.check_from_field(self.__from_field):
            message.get_message_body()
            message.set_name_and_phone()

    def get_messages_from_bot(self):
        self.__connect()
        self.__get_all_folders()
        self.__open_folder()
        self.__get_unread_messages()

    def set_message(self, message):
        self.__message = message

    def get_message(self):
        return self.__message
