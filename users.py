from aiogram.dispatcher.filters.state import State, StatesGroup
import dbwork


class UserStates(StatesGroup):
    nick  = State()
    phone = State()


class User:
    id_tel = ''
    nick = ''
    phone = ''
    text = ''
    no_user_text_str = ''
    user_cmnd = 'user'
    user_add_cmnd = 'useradd'
    user_del_cmnd = 'userdel'
    exist_in_db = False

    def __init__(self, id_tel):
        self.id_tel = id_tel

    def get_user(self):
        user_row = dbwork.get_user_from_db(self.id_tel)
        if user_row['id_tel'] != '':
            self.nick  = user_row['nick']
            self.phone = user_row['phone']
            self.text  = self.get_user_text()
            self.exist_in_db = True
            return self
        else:
            self.exist_in_db = False
            #self.no_user_text_str = 'Ваша контактная информация не указана, добавить? /{} Или идем в начало? /{}'.format(self.user_add_cmnd, 'start')
            self.no_user_text_str = 'No contact info, add? /{} Or to start? /{}'.format(
                self.user_add_cmnd, 'start')
            return self

    def set_user(self, data, id_tel):
        dbwork.set_user_in_db(data, id_tel)

    def get_user_text(self):
        #text = 'Ник: {}; телефон: {}; удалить: /{}, в начало: /{}'.format(self.nick, self.phone, self.user_del_cmnd, 'start')
        text = 'Nick: {}; phone: {}; delete: /{}, to start: /{}'.format(self.nick, self.phone, self.user_del_cmnd,
                                                                          'start')
        return text

    def del_user(self):
        dbwork.del_user_in_db(self.id_tel)

    def no_user_text(self) -> str:
        return self.no_user_text_str

