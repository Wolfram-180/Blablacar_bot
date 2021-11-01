from aiogram.dispatcher.filters.state import State, StatesGroup
import dbwork


class CarStates(StatesGroup):
    mark  = State()  # Will be represented in storage as 'CarStates:mark'
    model = State()  # Will be represented in storage as 'CarStates:model'
    plate = State()  # Will be represented in storage as 'CarStates:plate'
    seats = State()  # Will be represented in storage as 'CarStates:seats'


class Car:
    id_tel : str  # telegram_id водителя
    mark : str  # марка
    model : str  # модель
    plate : str  # госномер
    seats : int # мак колво мест
    text : str
    no_car_text_str : str
    car_cmnd = 'mycar'
    car_add_cmnd = 'caradd'
    car_del_cmnd = 'cardel'
    exist_in_db = False

    def __init__(self, id_tel):
        self.id_tel = id_tel
        self.mark = ''
        self.model = ''
        self.plate = ''
        self.seats = ''
        self.text = ''
        self.no_car_text_str = ''

    def get_car(self):
        car_row = dbwork.get_car_from_db(self.id_tel)
        if car_row['id_tel'] != '':
            self.plate = car_row['plate']
            self.mark  = car_row['mark']
            self.model = car_row['model']
            self.seats = car_row['seats']
            self.text = self.get_car_text()
            self.exist_in_db = True
            return self
        else:
            self.exist_in_db = False
            #self.no_car_text_str = 'Информации по авто нет в БД, добавить? /{} Или идем в начало? {}'.format(self.car_add_cmnd, '/start')
            self.no_car_text_str = 'No car info, add? /{} Or back to start? {}'.format(
                self.car_add_cmnd, '/start')
            return self

    def set_car(self, data, id_tel):
        dbwork.set_car_in_db(data, id_tel)

    def get_car_text(self):
        #text = 'Марка: {}; модель: {}; гос. номер: {}; мест: {}; удалить: /{}, в начало: /{}'.format(self.mark, self.model, self.plate, self.seats, self.car_del_cmnd, 'start')
        text = 'Manufacturer: {}; model: {}; plate: {}; places: {}; delete: /{}, go to start: /{}'.format(self.mark,
                                                                                                     self.model,
                                                                                                     self.plate,
                                                                                                     self.seats,
                                                                                                     self.car_del_cmnd,
                                                                                                     'start')
        return text

    def del_car(self):
        dbwork.del_car_in_db(self.id_tel)

    def no_car_text(self) -> str:
        text = self.no_car_text_str
        return text



