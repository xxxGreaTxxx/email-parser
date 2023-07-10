from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from log import Log, Levels
from mail import Mail
from config import config_vars


class Sites:
    __driver = None
    __offices = {}
    __current_office = []
    __mail = Mail()
    __log = Log(__name__)

    def __init__(self):
        self.__set_offices_from_config()

    def __set_offices_from_config(self):
        self.__offices = config_vars['offices']

    def __set_current_office(self):
        self.__log.add(Levels.info, 'Выбираем офис...')
        isOffice = False
        for key, value in self.__offices.items():
            if value[2] and value[1] > value[3]:
                isOffice = True
                self.__current_office = value
                value[2] = False
                self.__log.add(Levels.info, f'Выбран офис {key}. Разрешено заявок {value[1]}, передано заявок {value[3]}')
                break
        if not isOffice:
            self.__log.add(Levels.info, 'Все офисы получили заявки, идем по новому кругу...')
            for value in self.__offices.values():
                if value[1] > value[3]:
                    value[2] = True
                    isOffice = True
            if isOffice:
                self.__set_current_office()
            else:
                self.__log.add(Levels.warn, 'Все офисы получили максимальное количество заявок, сбрасываем количество и начинаем заново')
                for value in self.__offices.values():
                    value[3] = 0
                    value[2] = True
                self.__set_current_office()

    def send(self):
        i = -1
        self.__mail.get_messages_from_bot()
        o = Options()
        o.add_experimental_option('detach', False)
        while i >= -self.__mail.get_messages_count():
            self.__mail.get_message_data(i)
            message = self.__mail.get_message()
            if message.get_name():
                self.__set_current_office()
                self.__log.add(Levels.info, f'Начинаем отправку лида в выбранный офис...')
                self.__driver = webdriver.Chrome(options=o)
                self.__driver.get(self.__current_office[0])
                form_selectors = self.__current_office[4]
                name = message.get_name()
                phone = message.get_phone()
                self.__log.add(Levels.info, f'Данные заявки: Имя: {name}, Телефон: {phone}')
                try:
                    form = self.__driver.find_element(By.CLASS_NAME, form_selectors['form'])
                    form.find_element(By.CSS_SELECTOR, form_selectors['name']).send_keys(name)
                    form.find_element(By.CSS_SELECTOR, form_selectors['phone']).send_keys(phone)
                    form.find_element(By.CSS_SELECTOR, '[type="submit"]').click()
                    sleep(2)
                    self.__log.add(Levels.info, 'Заявка отправлена')
                    self.__current_office[3] += 1
                except Exception as e:
                    self.__log.add(Levels.error, f'Заявка не отправлена! Ошибка:\n{e}')
                self.__driver.close()
            i -= 1
