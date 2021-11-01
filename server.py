"""Сервер Telegram бота, запускаемый непосредственно"""
import logging
from aiogram import executor
import cars
from cars import CarStates
import users
from users import UserStates
import routes
from routes import RouteStates
from middlewares import AccessMiddleware
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode
import datetime
import re
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)

API_TOKEN = ''  # os.getenv("TELEGRAM_API_TOKEN")

PROXY_URL = '' # os.getenv("TELEGRAM_PROXY_URL")
PROXY_AUTH = ''
#    = aiohttp.BasicAuth(
#    login=os.getenv("TELEGRAM_PROXY_LOGIN"),
#    password=os.getenv("TELEGRAM_PROXY_PASSWORD")
#)

storage = MemoryStorage()

bot = Bot(token=API_TOKEN, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
dp = Dispatcher(bot, storage=storage)

restrict_access = False

if restrict_access:
    ACCESS_ID = '' # os.getenv("TELEGRAM_ACCESS_ID")
    dp.middleware.setup(AccessMiddleware(ACCESS_ID))

cmnd_user = users.User.user_cmnd
cmnd_user_add = users.User.user_add_cmnd
cmnd_user_del = users.User.user_del_cmnd
cmnd_mycar = cars.Car.car_cmnd
cmnd_car_add = cars.Car.car_add_cmnd
cmnd_actroutes = routes.Route.routes_view_cmnd
cmnd_addroutes = routes.Route.routes_add_cmnd
cmnd_takeplace = routes.Route.take_place_cmnd
cmnd_tknplaces = routes.Route.user_taken_places
cmnd_active_tknplaces = routes.Route.user_active_taken_places
cmnd_active_created_places = routes.Route.active_driver_created_places
cmnd_created_places = routes.Route.driver_created_places
cmnd_user_leave_place = routes.Route.user_leave_place
cmnd_driver_del_place = routes.Route.driver_del_place
cmnd_cancel = 'cancel'
cmnd_empty = 'empty'
cmnd_faq = 'faq'

# RU
#mess_enter_date = 'Введите дату поездки (сегодня или в будущем) в формате дд.мм, например 01.02 для 01 февраля (можно дд.мм.гггг если надо)'
#mess_enter_time = 'Введите время отправки от точки сбора в формате чч:мм, например 07:30'
#mess_enter_cost = "Введите желаемую стоимость 1 места в рублях (целое число от 0 до 9999)"
#mess_tostart = '/start для возврата в начало'
#mess_exit = ' (/' + cmnd_cancel + ' для выхода из процесса ввода)'

mess_enter_date = 'Enter ride date in format dd.mm, i.e. 01.02 for February, 1st (or dd.mm.yyyy if you prefer)'
mess_enter_time = 'Enter ride time in format hh:mm, i.e. 07:30'
mess_enter_cost = 'Enter cost of 1 place (integer only please)'
mess_tostart = '/start for main menu'
mess_exit = ' (/' + cmnd_cancel + ' for process reset)'

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    now = datetime.datetime.now()

    await message.reply('Hi there!', reply_markup=types.ReplyKeyboardRemove())

    await message.answer(
        #"Бот Vidnovoz - помощник для водителей и пассажиров.\n\n"
        #"Водители: создают поездки, везут.\n\n"
        #"Пассажиры: занимают места, едут.\n\n"
        #"Узнать подробнее как это работает: /" + cmnd_faq + " \n\n"
        #"Активные поездки (свободные места): /" + cmnd_actroutes + " \n\n"
        #"Создать поездку: /" + cmnd_addroutes + " \n\n"
        #"Моя контактная информация: /" + cmnd_user + " \n\n"
        #"Мой автомобиль: /" + cmnd_mycar + " \n\n"
        #"Занятые мной места (активные): /" + cmnd_active_tknplaces + " \n\n"
        #"Занятые мной места (все): /" + cmnd_tknplaces + " \n\n"
        #"Созданные мной поездки (активные): /" + cmnd_active_created_places + " \n\n"
        #"Созданные мной поездки (все): /" + cmnd_created_places + " \n\n"
        #"Мой TelegramID: " + str(message.from_user.id) + "\n"
        #"Сейчас: {}".format(now.strftime("%d %B %Y %H:%M")) + "\n"

        "Blabla bot - assistant for drivers & passengers for rides creating and taking.\n\n"
        "How it works: /" + cmnd_faq + " \n\n"
        "Active rides (free places): /" + cmnd_actroutes + " \n\n"
        "Create ride: /" + cmnd_addroutes + " \n\n"                                                 
        "My contact info: /" + cmnd_user + " \n\n"
        "My car: /" + cmnd_mycar + " \n\n"
        "Passenger: my taken places (active): /" + cmnd_active_tknplaces + " \n\n"
        "Passenger: my taken places (all): /" + cmnd_tknplaces + " \n\n"
        "Driver: my created places (active): /" + cmnd_active_created_places + " \n\n"
        "Driver: my created places (all): /" + cmnd_created_places + " \n\n"
        "My TelegramID: " + str(message.from_user.id) + "\n"
        "Now: {}".format(now.strftime("%d %B %Y %H:%M")) + "\n"
        #"instagram.com/ulvissa_com/"
        "\n"
    )
    # %d-%m-%Y %H:%M


@dp.message_handler(commands=[cmnd_faq, 'help'])
async def faq(message: types.Message):
    """ Информация о проекте """
#    await message.answer(
#        "Многие водители регулярно ездят по маршрутам типа Видное-метро, Березовая-Расторгуево и обратно, "
#        "имея свободные места в авто и возможность захватить попутчика. \n\n"
#        "Цель работы бота Vidnovoz - дать простой способ водителям сообщить о возможной "
#        "поездке и свои контакты, а потенциальным попутчикам - узнать о них и занять место.\n\n"
#        "Как это работает: \n "
#        "\n"
#        "любой пользователь командой /" + cmnd_user + " указывает свой ник и контактный телефон, \n"
#        "\n"
#        "если вы водитель - командой /" + cmnd_mycar + " указываете информацию об авто (номер, марка, модель, кол-во мест для пассажиров), \n"
#        "\n"
#        "командой /" + cmnd_addroutes + " водитель создает планируемую поездку (дата, время, откуда, куда, стоимость, комментарий); \n"
#        "\n"
#        "пассажир командой /" + cmnd_actroutes + " может увидеть активные поездки, занять место и узнать контакт водителя, \n"
#        "далее в указанные в поездке дату/время/место отъезда - созвон, встреча, поездка.\n"
#        "\n"
#        "Командой /" + cmnd_active_tknplaces + " - пассажир видит занятые собой места; \n"
#        "\n"
#        "командой /" + cmnd_created_places + " - водитель видит созданные собой поездки. \n"
#        "\n"
#        "При вводе любых данных можно прервать процесс командой /" + cmnd_cancel + " \n"
#        "\n"
#        "instagram.com/probkovidnoe/ - вопросы и предложения по работе бота\n"
#        "\n"
#        "В начало: /start\n"
#    )
    await message.answer(
        "Drivers can create rides with places, providing info by route, place cost, and contact info, "
        "passengers can view rides, take places and get driver`s contact.\n\n"
        "All users by command /" + cmnd_user + " can provide nick and contact phone, \n\n"
        "drivers by commands \n"
        "/" + cmnd_mycar + " - provide car info (plate, mark-model, places count), \n"
        "/" + cmnd_addroutes + " - create route providing info date, time, from, to, place cost, comment); \n\n"
        "passenger by command /" + cmnd_actroutes + " can see active rides, take place & get driver info, \n\n"
        "then they are meeting in ride`s start place/time - and move on!\n\n"
        "Also passenger can see places taken: /" + cmnd_active_tknplaces + "; \n\n"
        "and driver can see rides created: /" + cmnd_created_places + ". \n\n"
        "Any process can be reset by command /" + cmnd_cancel + " \n\n"
        "{}".format(mess_tostart) + "\n\n"
    )


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        await message.reply(mess_tostart)
        return
    #logging.info('Отмена состояния %r', current_state)
    logging.info('Cancel state: %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    #await message.reply('Ввод данных сброшен. ' + mess_tostart, reply_markup=types.ReplyKeyboardRemove())
    await message.reply('Process reset. ' + mess_tostart, reply_markup=types.ReplyKeyboardRemove())


##################################################### ROUTES VVVVVVVVVVVVVVVVVVVVVV
@dp.message_handler(lambda message: message.text.startswith('/'+cmnd_takeplace))
async def take_place(message: types.Message):
    # проверяем контакт пассажира
    _user = users.User(message.from_user.id)
    _user.get_user()
    if not _user.exist_in_db:
        answer_message = _user.no_user_text()
        await message.answer(answer_message)
        return

    place_id = int(message.text[len(cmnd_takeplace)+1:])
    routes_ = routes.Route(0)
    placestatus, driver_chat_id = routes_.take_place(place_id, message.from_user.id)
    if driver_chat_id > 0: # место успешно занято пассажиром
        #mess = placestatus + "Занятые мной места (активные): /" + cmnd_active_tknplaces + " \n"
        mess = placestatus + "My taken places (active): /" + cmnd_active_tknplaces + " \n"

        markup = types.ReplyKeyboardRemove()
        # сообщить водителю
        await bot.send_message(
            #message.chat.id,
            driver_chat_id,
            md.text(
                #md.text('Пассажир занял место № {} из /{} \n'.format(str(place_id), cmnd_active_created_places)),
                md.text('Passenger took place № {} of /{} \n'.format(str(place_id), cmnd_active_created_places)),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )
        await message.answer(mess)
    else:
        #mess = placestatus + "Свободные места (активные): /" + cmnd_actroutes + " \n"
        mess = placestatus + "Free places (active): /" + cmnd_actroutes + " \n"
        await message.answer(mess)


@dp.message_handler(lambda message: message.text.startswith('/'+cmnd_user_leave_place))
async def user_leave_place(message: types.Message):
    place_id = int(message.text[len(cmnd_user_leave_place)+1:])
    routes_ = routes.Route(0)
    placestatus, driver_chat_id = routes_.user_leave_place_func(place_id, message.from_user.id)

    if driver_chat_id > 0: # место успешно освобождено пассажиром
        #mess = placestatus + "Занятые мной места (активные): /" + cmnd_active_tknplaces + " \n"
        mess = placestatus + "My taken places (active): /" + cmnd_active_tknplaces + " \n"

        markup = types.ReplyKeyboardRemove()
        # сообщить водителю
        await bot.send_message(
            driver_chat_id,
            md.text(
                #md.text('Пассажир освободил место № {} из /{} \n'.format(str(place_id), cmnd_active_created_places)),
                md.text('Passenger left place № {} of /{} \n'.format(str(place_id), cmnd_active_created_places)),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )
        #await message.answer(mess)

        mess += '\n'+mess_tostart
        await message.answer(mess)


@dp.message_handler(lambda message: message.text.startswith('/'+cmnd_driver_del_place))
async def driver_del_place(message: types.Message):
    place_id = int(message.text[len(cmnd_driver_del_place)+1:])
    routes_ = routes.Route(0)
    mess = routes_.driver_del_place_func(place_id, message.from_user.id)
    mess += '\n'+mess_tostart
    await message.answer(mess)


@dp.message_handler(commands=[cmnd_actroutes])
async def active_routes(message: types.Message):
    """ Маршруты - активные """
    routes_ = routes.Route(message.from_user.id)
    answer_message = routes_.get_active_routes()

    if len(answer_message) > 4096:
        for x in range(0, len(answer_message), 4096):
            await message.answer(answer_message[x:x + 4096])
    else:
        await message.answer(answer_message)

    #await message.answer(answer_message)


@dp.message_handler(lambda message: message.text.startswith('/'+cmnd_active_tknplaces))
async def active_taken_places(message: types.Message):
    routes_ = routes.Route(message.from_user.id)
    answer_message = routes_.get_active_taken_places()
    #await message.answer(answer_message)
    if len(answer_message) > 4096:
        for x in range(0, len(answer_message), 4096):
            await message.answer(answer_message[x:x + 4096])
    else:
        await message.answer(answer_message)


@dp.message_handler(lambda message: message.text.startswith('/'+cmnd_active_created_places))
async def active_created_places(message: types.Message):
    routes_ = routes.Route(message.from_user.id)
    answer_message = routes_.get_active_created_places()
    #await message.answer(answer_message)
    if len(answer_message) > 4096:
        for x in range(0, len(answer_message), 4096):
            await message.answer(answer_message[x:x + 4096])
    else:
        await message.answer(answer_message)


@dp.message_handler(lambda message: message.text.startswith('/'+cmnd_tknplaces))
async def taken_places(message: types.Message):
    routes_ = routes.Route(message.from_user.id)
    answer_message = routes_.get_taken_places()
    #await message.answer(answer_message)
    if len(answer_message) > 4096:
        for x in range(0, len(answer_message), 4096):
            await message.answer(answer_message[x:x + 4096])
    else:
        await message.answer(answer_message)


@dp.message_handler(lambda message: message.text.startswith('/'+cmnd_created_places))
async def created_places(message: types.Message):
    routes_ = routes.Route(message.from_user.id)
    answer_message = routes_.get_created_places()
    #await message.answer(answer_message)
    if len(answer_message) > 4096:
        for x in range(0, len(answer_message), 4096):
            await message.answer(answer_message[x:x + 4096])
    else:
        await message.answer(answer_message)


@dp.message_handler(commands=[cmnd_addroutes])
async def route_add(message: types.Message):
    # проверяем авто и контакт водителя
    _car = cars.Car(message.from_user.id)
    _car.get_car()
    if not _car.exist_in_db:
        await message.reply(_car.no_car_text())
        return

    _user = users.User(message.from_user.id)
    _user.get_user()
    if not _user.exist_in_db:
        answer_message = _user.no_user_text()
        await message.answer(answer_message)
        return

    # прошли проверки
    await RouteStates.rdate.set()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    tmrtext0 = (datetime.date.today() + datetime.timedelta(days=0)).strftime('%d.%m')
    tmrtext1 = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%d.%m')
    tmrtext2 = (datetime.date.today() + datetime.timedelta(days=2)).strftime('%d.%m')
    tmrtext3 = (datetime.date.today() + datetime.timedelta(days=3)).strftime('%d.%m')
    btn_tmrtext0 = KeyboardButton(tmrtext0)
    btn_tmrtext1 = KeyboardButton(tmrtext1)
    btn_tmrtext2 = KeyboardButton(tmrtext2)
    btn_tmrtext3 = KeyboardButton(tmrtext3)
    markup.insert(btn_tmrtext0)
    markup.insert(btn_tmrtext1)
    markup.insert(btn_tmrtext2)
    markup.insert(btn_tmrtext3)

    await bot.send_message(
        message.chat.id,
        md.text(
            md.text(mess_enter_date),
            #md.bold("{}".format(tmrtext1)) + " для завтра",
            md.bold("{}".format(tmrtext1)) + " for tomorrow",
            md.text(mess_exit),
            sep='\n',
        ),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )


@dp.message_handler(state=RouteStates.rdate)
async def process_rdate(message: types.Message, state: FSMContext):
    date_entered = message.text

    match = re.search("^([1-9] |1[0-9]| 2[0-9]|3[0-1])(.|-)([1-9] |1[0-2])(.|-|)20[0-9][0-9]$", date_entered)
    if match is not None: # есть год в дате
        pass
    else:
        date_entered += ".2021"

    try:
        dt = datetime.datetime.strptime(date_entered, '%d.%m.%Y')
    except:
        #mess = 'Дата {} не распознана.\n{}\n{}\n'.format(dt, mess_enter_date, mess_exit)
        mess = 'Date {} not recognized.\n{}\n{}\n'.format(dt, mess_enter_date, mess_exit)
        await message.reply(mess)
        return

    try:    # timestring.Date(dtstring.text)
        if dt.date() < datetime.datetime.now().date():
            #mess = 'Введена дата в прошлом\n' + mess_enter_date + mess_exit
            mess = 'Date entered is in past\n' + mess_enter_date + mess_exit
            await message.reply(mess)
            return
    except:
        #mess = 'Не получилось определить - дата в прошлом или в будущем\n' + mess_enter_date + mess_exit
        mess = 'Can`t recognize - is date entered in past or future.\n' + mess_enter_date + mess_exit
        await message.reply(mess)
        return

    async with state.proxy() as data:
        data['rdate'] = datetime.datetime.strftime(dt, '%d.%m.%Y')

    await RouteStates.next()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    tmrtext1 = '07:15'
    tmrtext2 = '07:30'
    tmrtext3 = '07:45'
    tmrtext4 = '08:00'
    tmrtext5 = '08:15'
    tmrtext6 = '08:30'
    btn_tmrtext1 = KeyboardButton(tmrtext1)
    btn_tmrtext2 = KeyboardButton(tmrtext2)
    btn_tmrtext3 = KeyboardButton(tmrtext3)
    btn_tmrtext4 = KeyboardButton(tmrtext4)
    btn_tmrtext5 = KeyboardButton(tmrtext5)
    btn_tmrtext6 = KeyboardButton(tmrtext6)
    markup.insert(btn_tmrtext1)
    markup.insert(btn_tmrtext2)
    markup.insert(btn_tmrtext3)
    markup.insert(btn_tmrtext4)
    markup.insert(btn_tmrtext5)
    markup.insert(btn_tmrtext6)

    await bot.send_message(
        message.chat.id,
        md.text(
            md.text(mess_enter_time),
            md.text(mess_exit),
            sep='\n',
        ),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )


@dp.message_handler(state=RouteStates.rtime)
async def process_rtime(message: types.Message, state: FSMContext):
    try:
        tm = datetime.datetime.strptime(message.text, '%H:%M')
    except:
        #mess = 'Время не распознано.\n' + mess_enter_time + mess_exit
        mess = 'Time entered is not recognized.\n' + mess_enter_time + mess_exit
        await message.reply(mess)
        return

    try:  # timestring.Date(dtstring.text)
        async with state.proxy() as data:
            dttxt = data['rdate'] + ' ' + message.text
            dt = datetime.datetime.strptime(dttxt, '%d.%m.%Y %H:%M')
            data['rdt'] = dttxt   # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< route datetime

        if dt < datetime.datetime.now() + datetime.timedelta(minutes = 10):   # <<<<<<<<<<<<< добавил 10 минут в будущее
            #mess = 'Введена дата\время в прошлом, нужно хотя бы +10 минут позже чем сейчас \n' + mess_enter_time + mess_exit
            mess = 'Date/time entered is in past, need to be at least +10 minutes from now \n' + mess_enter_time + mess_exit
            await message.reply(mess)
            return
    except:
        #mess = 'Дата\время не распознано.\n' + mess_enter_time + mess_exit
        mess = 'Date/time entered is not recognized.\n' + mess_enter_time + mess_exit
        await message.reply(mess)
        return

    async with state.proxy() as data:
        data['rtime'] = message.text

    await RouteStates.next()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    tmrtext1 = 'Philadelphia'
    tmrtext2 = 'New York'
    btn_tmrtext1 = KeyboardButton(tmrtext1)
    btn_tmrtext2 = KeyboardButton(tmrtext2)
    markup.insert(btn_tmrtext1)
    markup.insert(btn_tmrtext2)

    await bot.send_message(
        message.chat.id,
        md.text(
            #md.text("Введите город отправления"),
            md.text("Enter 'From' city"),
            md.text(mess_exit),
            sep='\n',
        ),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )


@dp.message_handler(state=RouteStates.fcity)
async def process_fcity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fcity'] = message.text

    await RouteStates.next()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    tmrtext1 = 'N 16th St'
    tmrtext2 = 'Green St'
    tmrtext3 = 'Monterey St'
    tmrtext4 = 'Brandywine St'
    tmrtext5 = 'Wallace St'
    tmrtext6 = 'Nectarine St'
    tmrtext7 = 'Ogden St'
    tmrtext8 = 'Parrish St'
    btn_tmrtext1 = KeyboardButton(tmrtext1)
    btn_tmrtext2 = KeyboardButton(tmrtext2)
    btn_tmrtext3 = KeyboardButton(tmrtext3)
    btn_tmrtext4 = KeyboardButton(tmrtext4)
    btn_tmrtext5 = KeyboardButton(tmrtext5)
    btn_tmrtext6 = KeyboardButton(tmrtext6)
    btn_tmrtext7 = KeyboardButton(tmrtext7)
    btn_tmrtext8 = KeyboardButton(tmrtext8)
    markup.insert(btn_tmrtext1)
    markup.insert(btn_tmrtext2)
    markup.insert(btn_tmrtext3)
    markup.insert(btn_tmrtext4)
    markup.insert(btn_tmrtext5)
    markup.insert(btn_tmrtext6)
    markup.insert(btn_tmrtext7)
    markup.insert(btn_tmrtext8)

    await bot.send_message(
        message.chat.id,
        md.text(
            md.text("Enter 'From' street (or any other remarkable point)"),
            md.text(mess_exit),
            sep='\n',
        ),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )

    #await message.reply("Введите улицу отправления (или метро)" + mess_exit)


@dp.message_handler(state=RouteStates.fstreet)
async def process_fstreet(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fstreet'] = message.text
    await RouteStates.next()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    tmrtext1 = '1'
    tmrtext2 = '3'
    tmrtext3 = '5'
    tmrtext4 = '7'
    tmrtext5 = '9'
    tmrtext6 = '11'
    tmrtext7 = '13'
    tmrtext8 = '15'
    btn_tmrtext1 = KeyboardButton(tmrtext1)
    btn_tmrtext2 = KeyboardButton(tmrtext2)
    btn_tmrtext3 = KeyboardButton(tmrtext3)
    btn_tmrtext4 = KeyboardButton(tmrtext4)
    btn_tmrtext5 = KeyboardButton(tmrtext5)
    btn_tmrtext6 = KeyboardButton(tmrtext6)
    btn_tmrtext7 = KeyboardButton(tmrtext7)
    btn_tmrtext8 = KeyboardButton(tmrtext8)
    markup.insert(btn_tmrtext1)
    markup.insert(btn_tmrtext2)
    markup.insert(btn_tmrtext3)
    markup.insert(btn_tmrtext4)
    markup.insert(btn_tmrtext5)
    markup.insert(btn_tmrtext6)
    markup.insert(btn_tmrtext7)
    markup.insert(btn_tmrtext8)

    await bot.send_message(
        message.chat.id,
        md.text(
            #md.text("Введите № дома отправления (при необходимости, или ", md.bold("/"+cmnd_empty), " если не нужно)", mess_exit),
            md.text("Enter 'From' building number (if needed, or ", md.bold("/" + cmnd_empty), " if not needed)",
                    mess_exit),
            sep='\n',
        ),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )


@dp.message_handler(state=RouteStates.fhouse)
async def process_fhouse(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fhouse'] = message.text
    await RouteStates.next()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    #tmrtext1 = 'Видное'
    #tmrtext2 = 'Москва'
    tmrtext1 = 'Philadelphia'
    tmrtext2 = 'New York'
    btn_tmrtext1 = KeyboardButton(tmrtext1)
    btn_tmrtext2 = KeyboardButton(tmrtext2)
    markup.insert(btn_tmrtext1)
    markup.insert(btn_tmrtext2)

    await bot.send_message(
        message.chat.id,
        md.text(
            #md.text("Введите город прибытия"),
            md.text("Enter 'To' city"),
            md.text(mess_exit),
            sep='\n',
        ),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )

    #await message.reply("Введите город прибытия" + mess_exit)


@dp.message_handler(state=RouteStates.tcity)
async def process_tcity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tcity'] = message.text
    await RouteStates.next()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    #tmrtext1 = 'Ермолинская'
    #tmrtext2 = 'Березовая'
    #tmrtext3 = 'ПЛК'
    #tmrtext4 = 'Аннино'
    #tmrtext5 = 'Домодедовская'
    #tmrtext6 = 'Теплый Стан'
    #tmrtext7 = 'Парковка нижняя Расторгуево'
    #tmrtext8 = 'Школьная'
    tmrtext1 = '17th St'
    tmrtext2 = '18th St'
    tmrtext3 = '19th St'
    tmrtext4 = '25th St'
    tmrtext5 = '26th St'
    tmrtext6 = 'Crescent St'
    tmrtext7 = 'Skillman Ave'
    tmrtext8 = 'Woodside Ave'
    btn_tmrtext1 = KeyboardButton(tmrtext1)
    btn_tmrtext2 = KeyboardButton(tmrtext2)
    btn_tmrtext3 = KeyboardButton(tmrtext3)
    btn_tmrtext4 = KeyboardButton(tmrtext4)
    btn_tmrtext5 = KeyboardButton(tmrtext5)
    btn_tmrtext6 = KeyboardButton(tmrtext6)
    btn_tmrtext7 = KeyboardButton(tmrtext7)
    btn_tmrtext8 = KeyboardButton(tmrtext8)
    markup.insert(btn_tmrtext1)
    markup.insert(btn_tmrtext2)
    markup.insert(btn_tmrtext3)
    markup.insert(btn_tmrtext4)
    markup.insert(btn_tmrtext5)
    markup.insert(btn_tmrtext6)
    markup.insert(btn_tmrtext7)
    markup.insert(btn_tmrtext8)

    await bot.send_message(
        message.chat.id,
        md.text(
            #md.text("Введите улицу прибытия (или метро)"),
            md.text("Enter 'To' street (or any remarkable point)"),
            md.text(mess_exit),
            sep='\n',
        ),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )
    #await message.reply("Введите улицу прибытия (или метро)" + mess_exit)


@dp.message_handler(state=RouteStates.tstreet)
async def process_tstreet(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tstreet'] = message.text
    await RouteStates.next()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    tmrtext1 = '1'
    tmrtext2 = '3'
    tmrtext3 = '5'
    tmrtext4 = '7'
    tmrtext5 = '9'
    tmrtext6 = '11'
    tmrtext7 = '13'
    tmrtext8 = '15'
    btn_tmrtext1 = KeyboardButton(tmrtext1)
    btn_tmrtext2 = KeyboardButton(tmrtext2)
    btn_tmrtext3 = KeyboardButton(tmrtext3)
    btn_tmrtext4 = KeyboardButton(tmrtext4)
    btn_tmrtext5 = KeyboardButton(tmrtext5)
    btn_tmrtext6 = KeyboardButton(tmrtext6)
    btn_tmrtext7 = KeyboardButton(tmrtext7)
    btn_tmrtext8 = KeyboardButton(tmrtext8)
    markup.insert(btn_tmrtext1)
    markup.insert(btn_tmrtext2)
    markup.insert(btn_tmrtext3)
    markup.insert(btn_tmrtext4)
    markup.insert(btn_tmrtext5)
    markup.insert(btn_tmrtext6)
    markup.insert(btn_tmrtext7)
    markup.insert(btn_tmrtext8)

    await bot.send_message(
        message.chat.id,
        md.text(
            #md.text("Введите № дома прибытия (при необходимости, или ", md.bold("/"+cmnd_empty), " если не нужно)", mess_exit),
            md.text("Enter 'To' building number (if needed, or ", md.bold("/" + cmnd_empty), " if not needed)",
                    mess_exit),
            sep='',
        ),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )


@dp.message_handler(state=RouteStates.thouse)
async def process_thouse(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['thouse'] = message.text
    await RouteStates.next()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    tmrtext1 = '0'
    tmrtext2 = '10'
    tmrtext3 = '15'
    tmrtext4 = '20'
    tmrtext5 = '25'
    tmrtext6 = '30'
    tmrtext7 = '35'
    tmrtext8 = '50'
    btn_tmrtext1 = KeyboardButton(tmrtext1)
    btn_tmrtext2 = KeyboardButton(tmrtext2)
    btn_tmrtext3 = KeyboardButton(tmrtext3)
    btn_tmrtext4 = KeyboardButton(tmrtext4)
    btn_tmrtext5 = KeyboardButton(tmrtext5)
    btn_tmrtext6 = KeyboardButton(tmrtext6)
    btn_tmrtext7 = KeyboardButton(tmrtext7)
    btn_tmrtext8 = KeyboardButton(tmrtext8)
    markup.insert(btn_tmrtext1)
    markup.insert(btn_tmrtext2)
    markup.insert(btn_tmrtext3)
    markup.insert(btn_tmrtext4)
    markup.insert(btn_tmrtext5)
    markup.insert(btn_tmrtext6)
    markup.insert(btn_tmrtext7)
    markup.insert(btn_tmrtext8)

    await bot.send_message(
        message.chat.id,
        md.text(
            md.text(mess_enter_cost),
            md.text(mess_exit),
            sep='\n',
        ),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )


@dp.message_handler(state=RouteStates.costr)
async def process_costr(message: types.Message, state: FSMContext):
    try:
        cost = int(message.text)
    except:
        mess = 'Cost not recognized, please enter integer number.\n' + mess_enter_cost + mess_exit
        await message.reply(mess)
        return

    async with state.proxy() as data:
        data['costr'] = message.text
    await RouteStates.next()

    markup = types.ReplyKeyboardRemove()
    await bot.send_message(
        message.chat.id,
        md.text(
            #md.text("Введите комментарий (при желании, или ", md.bold("/"+cmnd_empty), " если не нужно)"),
            md.text("Enter comment (if needed, or ", md.bold("/" + cmnd_empty), " if not needed)"),
            sep='',
        ),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )


@dp.message_handler(state=RouteStates.drcmnt)
async def process_drcmnt(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "/" + cmnd_empty:
            data['drcmnt'] = ''
        else:
            data['drcmnt'] = message.text

        data_check = data._data

        # меняем /empty на ---
        #for key, value in data_check.items():
        #    if value == "/"+cmnd_empty:
        #        data[key] = '---'

        # корректирую формат rdate и rdt
        data['rdate'] = (datetime.datetime.strptime(data['rdate'], '%d.%m.%Y')).strftime('%Y-%m-%d')
        data['rdt'] = data['rdate'] + ' ' + data['rtime'] # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< route datetime
        data['driver_chat_id'] = message.chat.id

        markup = types.ReplyKeyboardRemove()

        _car = cars.Car(message.from_user.id)
        _car.get_car()
        _seats = _car.seats

        _route = routes.Route(message.from_user.id)

        for r in range(0, _seats):
            _route.set_route(data)

        await bot.send_message(
            message.chat.id,
            md.text(
                #md.text("Ок, добавили поездку ->"),
                #md.text("Дата отправки : ", md.code(data["rdate"])),
                #md.text("Время отправки : ", md.code(data["rtime"])),
                #md.text("От - город : ", md.code(data["fcity"])),
                #md.text("От - улица (метро) : ", md.code(data["fstreet"])),
                #md.text("От - дом : ", md.code(data["fhouse"])),
                #md.text("В - город : ", md.code(data["tcity"])),
                #md.text("В - улица (метро) : ", md.code(data["tstreet"])),
                #md.text("В - дом : ", md.code(data["thouse"])),
                #md.text("Стоимость за место, руб : ", md.code(data["costr"])),
                #md.text("Комментарий водителя : ", md.code(data["drcmnt"])),
                #md.text("Создано мест на поездку в БД : ", str(_seats)),
                #md.text('Вернуться в начало: /start'),
                md.text("OK, ride added ->"),
                md.text("Date start : ", md.code(data["rdate"])),
                md.text("Time start : ", md.code(data["rtime"])),
                md.text("From - city : ", md.code(data["fcity"])),
                md.text("From - street (point) : ", md.code(data["fstreet"])),
                md.text("From - building : ", md.code(data["fhouse"])),
                md.text("To - city : ", md.code(data["tcity"])),
                md.text("To - street (point) : ", md.code(data["tstreet"])),
                md.text("To - building : ", md.code(data["thouse"])),
                md.text("Place cost : ", md.code(data["costr"])),
                #md.text("Driver`s comment : {}".format(data["drcmnt"])),
                md.text("Ride places created in DB : ", str(_seats)),
                md.text('{}'.format(mess_tostart)),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )
    # Finish conversation
    await state.finish()


##################################################### ROUTES AAAAAAAAAAAAAAAAAAAAA


##################################################### CAR VVVVVVVVVVVVVVVVVVVVVV
@dp.message_handler(commands=[cmnd_mycar])
async def my_car(message: types.Message):
    """Информация про автомобиль - показ """
    my_car = cars.Car(message.from_user.id)
    my_car.get_car()
    if my_car.exist_in_db:
        answer_message = my_car.get_car_text()
    else:
        answer_message = my_car.no_car_text()
    await message.answer(answer_message)


@dp.message_handler(commands=[cmnd_car_add])
async def car_add(message: types.Message):
    """
    Conversation's entry point
    """
    # Remove keyboard
    markup = types.ReplyKeyboardRemove()

    # Set state
    await CarStates.mark.set()
    #await message.reply("Марка автомобиля (необязательно) ?")
    await message.reply("Car manufacturer ?")


@dp.message_handler(state=CarStates.mark)
async def process_mark(message: types.Message, state: FSMContext):
    """
    Process car mark
    """
    async with state.proxy() as data:
        data['mark'] = message.text

    await CarStates.next()
    #await message.reply("Модель автомобиля (необязательно) ?")
    await message.reply("Car model ?")


@dp.message_handler(state=CarStates.model)
async def process_model(message: types.Message, state: FSMContext):
    """
    Process car model
    """
    async with state.proxy() as data:
        data['model'] = message.text

    await CarStates.next()
    #await message.reply("Гос. номер автомобиля (необязательно) ?")
    await message.reply("Car plate (at least numbers) ?")


@dp.message_handler(state=CarStates.plate)
async def process_plate(message: types.Message, state: FSMContext):
    """
    Process car plate
    """
    async with state.proxy() as data:
        data['plate'] = message.text

    #seats_q = "Максимальное кол-во пассажиров?"
    seats_q = "Car passengers maximum count?"

    await CarStates.next()   # -> seats
    # await message.reply(seats_q)

    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("1", "2", "3", "4")

    await message.reply(seats_q, reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["1", "2", "3", "4"], state=CarStates.seats)
async def process_seats_invalid(message: types.Message):
    """
    In this example seats has to be one of: 1, 2, 3, 4
    """
    #return await message.reply("Пожалуйста укажите число от 1 до 4")
    return await message.reply("Please enter integer in range 1 to 4")


@dp.message_handler(state=CarStates.seats)
async def process_seats(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['seats'] = message.text

        # Remove keyboard
        markup = types.ReplyKeyboardRemove()

        my_car = cars.Car(message.from_user.id)
        my_car.set_car(data, message.from_user.id)

        # And send message
        await bot.send_message(
            message.chat.id,
            md.text(
                #md.text('Ок, добавили авто, марка: ', md.bold(data['mark'])),
                #md.text('модель: ', md.code(data['model'])),
                #md.text('гос. номер: ', data['plate']),
                #md.text('мест: ', data['seats']),
                #md.text('Вернуться в начало: ', '/start'),
                md.text('OK, car added, manufacturer: ', md.bold(data['mark'])),
                md.text('model: ', md.code(data['model'])),
                md.text('plate: ', data['plate']),
                md.text('places: ', data['seats']),
                md.text(mess_tostart),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )

    # Finish conversation
    await state.finish()


@dp.message_handler(lambda message: message.text.startswith('/'+cars.Car.car_del_cmnd))
async def del_car(message: types.Message):
    """Удаляет авто"""
    my_car = cars.Car(message.from_user.id)
    my_car.del_car()

    #answer_message = "Авто удалено, в начало /start"
    answer_message = "Car deleted, {}".format(mess_tostart)
    await message.answer(answer_message)
##################################################### CAR AAAAAAAAAAAAAAAAAAAAA


##################################################### USER VVVVVVVVVVVVVVVVVVVVVV
@dp.message_handler(commands=[cmnd_user])
async def user(message: types.Message):
    """Информация про юзера - показ """
    _user = users.User(message.from_user.id)
    _user.get_user()
    if _user.exist_in_db:
        answer_message = _user.get_user_text()
    else:
        answer_message = _user.no_user_text()
    await message.answer(answer_message)


@dp.message_handler(commands=[cmnd_user_add])
async def user_add(message: types.Message):
    """
    Conversation's entry point
    """
    # Remove keyboard
    markup = types.ReplyKeyboardRemove()

    # Set state
    await UserStates.nick.set()
    #await message.reply("Ваш ник ?")
    await message.reply("Your nick?")


@dp.message_handler(state=UserStates.nick)
async def process_nick(message: types.Message, state: FSMContext):
    """
    Process phone
    """
    async with state.proxy() as data:
        data['nick'] = message.text

    await UserStates.next()
    #await message.reply("Номер телефона (необязательно, но очень желательно) ?")
    await message.reply("Contact phone number ?")


@dp.message_handler(state=UserStates.phone)
async def process_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text

        # Remove keyboard
        markup = types.ReplyKeyboardRemove()

        _user = users.User(message.from_user.id)
        _user.set_user(data, message.from_user.id)

        # And send message
        await bot.send_message(
            message.chat.id,
            md.text(
                #md.text('Добавлена инфа по пользователю, ник: ', md.bold(data['nick'])),
                #md.text('телефон: ', md.code(data['phone'])),
                #md.text('Вернуться в начало: /start'),
                md.text('User info added, nick: ', md.bold(data['nick'])),
                md.text('phone: ', md.code(data['phone'])),
                md.text(mess_tostart),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )

    # Finish conversation
    await state.finish()


@dp.message_handler(commands=[cmnd_user_del])
async def del_user(message: types.Message):
    """Удаляет user"""
    _user = users.User(message.from_user.id)
    _user.del_user()

    #answer_message = "Контактная информация пользователя удалена, в начало /start"
    answer_message = "Contact info deleted, {}".format(mess_tostart)
    await message.answer(answer_message)
##################################################### USER AAAAAAAAAAAAAAAAAAAAA


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)