from aiogram.dispatcher.filters.state import State, StatesGroup
import dbwork
import datetime


class RouteStates(StatesGroup):
    rdate = State()
    rtime = State()
    fcity = State()
    fstreet = State()
    fhouse = State()
    tcity = State()
    tstreet = State()
    thouse = State()
    costr  = State()
    drcmnt = State()
    rdt = State()

class Route:
    id = 0
    date = ''
    time = ''
    from_city = ''
    from_street = ''
    from_house = ''
    to_city = ''
    to_street = ''
    to_house = ''
    id_tel_driver = ''
    id_tel_user = ''
    driver_comment = ''
    user_comment = ''
    route_created = ''
    routes_view_cmnd = 'routesview'
    routes_add_cmnd = 'routesadd'
    take_place_cmnd = 'takeplace'
    #drvr_added_routes = 'addedroutes'
    user_taken_places = 'takenplaces'
    user_active_taken_places = 'acttknplcs'
    active_driver_created_places = 'actdrvcrtd'
    driver_created_places = 'drvcrtd'
    user_leave_place = 'usrleave'
    driver_del_place = 'drvdel'
    exist_in_db = False

    def __init__(self, id_tel):
        self.id_tel_user = id_tel

    def set_route(self, data):
        dbwork.set_route_in_db(data, self.id_tel_user)

    def take_place(self, id_place, id_tel_user):
        driver_chat_id = dbwork.take_place(id_place, id_tel_user) # id_tel_driver = -1 если не нашли
        if driver_chat_id > 0:
            #placestatus = 'Место успешно занято\n'
            placestatus = 'Place taken\n'
        else:
            #placestatus = 'Извините, кто-то уже занял это место\n'
            placestatus = 'Sorry, that place is taken by somebody else\n'
        return placestatus, driver_chat_id

    def user_leave_place_func(self, id_place, id_tel_user):
        placestatus, driver_chat_id = dbwork.leave_place(id_place, id_tel_user)
        placestatus += '\n'
        return placestatus, driver_chat_id

    def driver_del_place_func(self, id_place, id_tel_user):
        placestatus = dbwork.delete_place(id_place, id_tel_user)
        placestatus += '\n'
        return placestatus

    def get_routes(self, is_active=False, me_driver=False, me_user=False):
        _all_routes = {}
        dttimenow = datetime.datetime.now()

        all_routes = dbwork.get_routes(str(self.id_tel_user), dttimenow, is_active, me_driver, me_user)

        mess = []

        if is_active is True and me_user is False and me_driver is False:
            #mess.append('Информация по местам (поездкам) активным на дату-время: \n{}'.format(dttimenow.strftime("%d.%m.%y %H:%M:%S")))
            mess.append('Info by rides active at date-time: \n{}'.format(
                dttimenow.strftime("%d.%m.%y %H:%M:%S")))

        if is_active is True and me_user is True:
            #mess.append('Информация по занятым мной местам активным на дату-время: \n{}'.format(dttimenow.strftime("%d.%m.%y %H:%M")))
            mess.append('Info by place taken by me for date-time: \n{}'.format(
                dttimenow.strftime("%d.%m.%y %H:%M")))

        if is_active is True and me_driver is True:
            #mess.append('Информация по созданным мной местам активным на дату-время: \n{}'.format(dttimenow.strftime("%d.%m.%y %H:%M")))
            mess.append('Info by place created by me active for date-time: \n{}'.format(
                dttimenow.strftime("%d.%m.%y %H:%M")))

        if is_active is False and me_user is True:
            #mess.append('Информация по занятым мной местам за все время: ')
            mess.append('Info by place taken by me for all time: ')

        if is_active is False and me_driver is True:
            #mess.append('Информация по созданным мной местам за все время:')
            mess.append('Info by place created by me for all time:')

        mess.append('\n')
        mess.append('*'*15)
        mess.append('\n')

        if is_active is True and me_user is False and me_driver is False:
            for row in all_routes.items():
                #mess.append('{}: Отъезд -> дата: {} время: {} \nгород: {} ; улица(метро): {} ; дом: {} |\n'
                #            'Приезд -> город: {} ; улица(метро): {} ; дом: {} \n'
                #            'Стоимость за место в руб.: {} \n Комментарий водителя: {} \n'
                #            'Занять место /{}{} \n'.format(row[1]['id'], row[1]['route_date'], row[1]['route_time'], row[1]['from_city'], row[1]['from_street'], row[1]['from_house'],
                #                              row[1]['to_city'], row[1]['to_street'], row[1]['to_house'],
                #                              row[1]['cost_rub'], row[1]['driver_comment'],
                #                              self.take_place_cmnd, row[1]['id'])
                #            )
                mess.append('{}: Ride start -> date: {} time: {}\n city: {} ; street (point): {} ; building: {} |\n'
                            'Ride finish -> city: {} ; street (point): {} ; building: {} \n'
                            'Place cost: {} \n Driver`s comment: {} \n'
                            'Take place /{}{} \n'.format(row[1]['id'], row[1]['route_date'], row[1]['route_time'], row[1]['from_city'], row[1]['from_street'], row[1]['from_house'],
                                              row[1]['to_city'], row[1]['to_street'], row[1]['to_house'],
                                              row[1]['cost_rub'], row[1]['driver_comment'],
                                              self.take_place_cmnd, row[1]['id'])
                            )
                mess.append('*' * 15)
                mess.append('\n')

        if me_user is True:
            for row in all_routes.items():
                #mess.append('{}: Отъезд -> дата: {} время: {} \nгород: {} ; улица(метро): {} ; дом: {} |\n'
                #            'Приезд -> город: {} ; улица(метро): {} ; дом: {} \n'
                #            'Стоимость за место в руб.: {} \n Комментарий водителя: {} \n'
                #            'Ник водителя: {} ; тел. водителя: {} ; \nНомер авто: {} ; марка: {} ; модель: {}'
                #            '\n'.format(row[1]['id'], row[1]['route_date'], row[1]['route_time'], row[1]['from_city'], row[1]['from_street'], row[1]['from_house'],
                #                        row[1]['to_city'], row[1]['to_street'], row[1]['to_house'],
                #                        row[1]['cost_rub'], row[1]['driver_comment'],
                #                        row[1]['driver_nick'], row[1]['driver_phone'], row[1]['plate'], row[1]['mark'], row[1]['model']
                #                        )
                #            )
                mess.append('{}: Ride start -> date: {} time: {}\n city: {} ; street (point): {} ; building: {} |\n'
                            'Ride finish -> city: {} ; street (point): {} ; building: {} \n'
                            'Place cost: {} \n Driver`s comment: {} \n'
                            'Driver`s nick: {} ; driver`s phone: {} ;\n Car plate: {} ; manufacturer: {} ; model: {}'
                            '\n'.format(row[1]['id'], row[1]['route_date'], row[1]['route_time'], row[1]['from_city'], row[1]['from_street'], row[1]['from_house'],
                                        row[1]['to_city'], row[1]['to_street'], row[1]['to_house'],
                                        row[1]['cost_rub'], row[1]['driver_comment'],
                                        row[1]['driver_nick'], row[1]['driver_phone'], row[1]['plate'], row[1]['mark'], row[1]['model']
                                        )
                            )
                if is_active is True:
                    #mess.append('Освободить место /{}{}\n'.format(self.user_leave_place, row[1]['id']))
                    mess.append('Leave he place /{}{}\n'.format(self.user_leave_place, row[1]['id']))
                mess.append('*' * 15)
                mess.append('\n')

        if me_driver is True:
            for row in all_routes.items():
                mess.append('{}: Ride start -> date: {} time: {}\n city: {} ; street (point): {} ; building: {} |\n'
                            'Ride finish -> city: {} ; street (point): {} ; building: {} \n'
                            'Place cost: {} \n Driver`s comment: {} \n'
                            'Passenger`s nick: {} ; passenger`s phone: {} ; '
                            '\n'.format(row[1]['id'], row[1]['route_date'], row[1]['route_time'], row[1]['from_city'], row[1]['from_street'], row[1]['from_house'],
                                        row[1]['to_city'], row[1]['to_street'], row[1]['to_house'],
                                        row[1]['cost_rub'], row[1]['driver_comment'],
                                        row[1]['user_nick'], row[1]['user_phone']
                                        )
                            )
                #mess.append('{}: Отъезд -> дата: {} время: {} \nгород: {} ; улица(метро): {} ; дом: {} |\n'
                #            'Приезд -> город: {} ; улица(метро): {} ; дом: {} \n'
                #            'Стоимость за место в руб.: {} \n Комментарий водителя: {} \n'
                #            'Ник пассажира: {} ; тел. пассажира: {} ; '
                #            '\n'.format(row[1]['id'], row[1]['route_date'], row[1]['route_time'], row[1]['from_city'], row[1]['from_street'], row[1]['from_house'],
                #                        row[1]['to_city'], row[1]['to_street'], row[1]['to_house'],
                #                        row[1]['cost_rub'], row[1]['driver_comment'],
                #                        row[1]['user_nick'], row[1]['user_phone']
                #                        )
                #            )
                if is_active is True:
                    #mess.append('Удалить место /{}{}\n'.format(self.driver_del_place, row[1]['id']))
                    mess.append('Delete place /{}{}\n'.format(self.driver_del_place, row[1]['id']))
                mess.append('*' * 15)
                mess.append('\n')

        #mess.append('В начало: /start')
        mess.append('/start for main menu')
        text = ''.join(mess)
        return text

    def get_active_routes(self):
        return self.get_routes(is_active=True, me_user=False, me_driver=False)

    def get_active_taken_places(self):
        return self.get_routes(is_active=True, me_user=True)

    def get_active_created_places(self):
        return self.get_routes(is_active=True, me_driver=True)

    def get_taken_places(self):
        return self.get_routes(me_user=True)

    def get_created_places(self):
        return self.get_routes(me_driver=True)





