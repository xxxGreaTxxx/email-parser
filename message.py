from log import Log, Levels
import email


class Message:
    __id = b''
    __name = ''
    __phone = ''
    __body = ''
    __message = ''
    __imap = None
    __log = Log(__name__)

    def __init__(self, mess_id, imap):
        self.__id = mess_id
        self.__name = ''
        self.__phone = ''
        self.__body = ''
        self.__message = ''
        self.__imap = imap
        self.__get_message_data()

    def __get_message_data(self):
        self.__log.add(Levels.info, f'Получаем данные письма с UID={self.__id.decode("utf-8")}...')
        res, data = self.__imap.uid('fetch', self.__id, '(RFC822)')
        if res == 'OK':
            self.__log.add(Levels.info, f'Данные письма с UID={self.__id.decode("utf-8")} получены')
            raw_email = data[0][1]
            self.__message = email.message_from_bytes(raw_email)
        else:
            self.__log.add(Levels.warn, f'Ошибка получения данных письма с UID={self.__id.decode("utf-8")}:\n{data[0].decode("utf-8")}')

    def check_from_field(self, from_address):
        self.__log.add(Levels.info, 'Проверяем отправителя...')
        from_name, from_addr = email.utils.parseaddr(self.__message['From'])
        if from_addr == from_address:
            self.__log.add(Levels.info, f'Письмо от нужного отправителя {from_address}')
            return True
        else:
            self.__log.add(Levels.info, f'Отправитель письма {from_addr} - нам не нужен, пропускаем')
            return False

    def get_message_body(self):
        self.__log.add(Levels.info, 'Получаем текст письма...')
        if self.__message.is_multipart():
            for part in self.__message.walk():
                if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
                    self.__body = part.get_payload(decode=True).decode('utf-8')
        else:
            self.__body = self.__message.get_payload().decode('utf-8')
        self.__log.add(Levels.info, 'Текст письма получен:\n{0}'.format(str.replace(self.__body, '\r\n', ' ')))

    def set_name_and_phone(self):
        self.__log.add(Levels.info, 'Вычленяем имя и телефон...')
        str_array = self.__body.split('\r\n')
        for el in str_array:
            if el.startswith('Имя'):
                arr = el.split(': ')
                self.__name = arr[1]
            if el.startswith('Телефон'):
                arr = el.split(': ')
                self.__phone = arr[1]
        self.__log.add(Levels.info, f'Получены Имя: {self.__name}. Телефон: {self.__phone}')

    def get_name(self):
        return self.__name

    def get_phone(self):
        return self.__phone
