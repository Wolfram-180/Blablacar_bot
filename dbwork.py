import pymysql
import pytz
import routes

# MySQL DB
_host = ''
_user = ''
_password = ''
_db = ''
_charset = 'utf32'

debug = False

local_tz = pytz.timezone('Europe/Moscow')

def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt) # .normalize might be unnecessary


def aslocaltimestr(utc_dt):
    return utc_to_local(utc_dt).strftime('%Y-%m-%d %H:%M:%S.%f')
#   return utc_to_local(utc_dt).strftime('%Y-%m-%d %H:%M:%S.%f %Z%z')

def getconnect():
    connect = pymysql.connect(host = _host,
                              user = _user,
                              password = _password,
                              db = _db,
                              port = 3306)
                              #charset = _charset,
                              #cursorclass = pymysql.cursors.DictCursor)
    return connect


def disconnect(connection):
    connection.close()


def get_car_from_db(id_tel):
    my_car = {'id_tel': '', 'plate': '', 'mark': '', 'model': '', 'seats': '', }
    connection_ = getconnect()
    with connection_.cursor() as cur:
        sql = 'select id_tel, plate, mark, model, seats from vidnovoz_cars where ' \
              'id_tel={}'.format(id_tel)
        cur.execute(sql)
        cur.fetchall
        if cur.rowcount > 0:
            for row in cur:
                my_car['id_tel'] = row[0]
                my_car['plate']  = row[1]
                my_car['mark']   = row[2]
                my_car['model']  = row[3]
                my_car['seats']  = row[4]
    disconnect(connection_)
    return my_car


def set_car_in_db(data, id_tel):
    connection_ = getconnect()
    with connection_.cursor() as cur:
        sql = 'insert into vidnovoz_cars (id_tel, plate, mark, model, seats) values ' \
              '({}, "{}", "{}", "{}", {})'.format(id_tel, data['plate'][:40], data['mark'][:40], data['model'][:40], data['seats'])
        cur.execute(sql)
    disconnect(connection_)


def del_car_in_db(id_tel):
    connection_ = getconnect()
    with connection_.cursor() as cur:
        sql = 'delete from vidnovoz_cars where id_tel= {}'.format(id_tel)
        cur.execute(sql)
    disconnect(connection_)


def get_user_from_db(id_tel):
    _user = {'id_tel': '', 'nick': '', 'phone': '', }
    connection_ = getconnect()
    with connection_.cursor() as cur:
        sql = 'select id_tel, nick, phone from vidnovoz_user where id_tel={}'.format(id_tel)
        cur.execute(sql)
        cur.fetchall
        if cur.rowcount > 0:
            for row in cur:
                _user['id_tel'] = row[0]
                _user['nick']   = row[1]
                _user['phone']  = row[2]
    disconnect(connection_)
    return _user


def set_user_in_db(data, id_tel):
    connection_ = getconnect()
    with connection_.cursor() as cur:
        sql = 'insert into vidnovoz_user (id_tel, nick, phone) values ({}, "{}",' \
              ' "{}")'.format(id_tel, data['nick'][:40], data['phone'][:40])
        cur.execute(sql)
    disconnect(connection_)


def del_user_in_db(id_tel):
    connection_ = getconnect()
    with connection_.cursor() as cur:
        sql = 'delete from vidnovoz_user where id_tel= {}'.format(id_tel)
        cur.execute(sql)
    disconnect(connection_)


def get_routes(id_tel, dttimenow, is_active=False, me_driver=False, me_user=False):
    connection_ = getconnect()
    routeslist = {}

    with connection_.cursor() as cur:
        sql = "select id, route_date, route_time, route_datetime, route_created, from_city, from_street, from_house, to_city, to_street, to_house, " \
              "id_tel_driver, id_tel_user, cost_rub, driver_comment, user_comment, vud.nick as driver_nick, vud.phone as driver_phone, vc.plate, vc.mark, vc.model, vuu.nick as user_nick, vuu.phone as user_phone " \
              "from vidnovoz_routes vr left join vidnovoz_user vud on vr.id_tel_driver = vud.id_tel left join vidnovoz_user vuu on vr.id_tel_user = vuu.id_tel left join vidnovoz_cars vc on vr.id_tel_driver = vc.id_tel "

        if is_active is True and me_user is False and me_driver is False:
            sql += " where route_datetime >= '{}'".format(dttimenow)
            sql += " and id_tel_user = 0"

        if is_active is True and me_user is True:
            sql += " where route_datetime >= '{}'".format(dttimenow)
            sql += " and id_tel_user = {}".format(id_tel)

        if is_active is True and me_driver is True:
            sql += " where route_datetime >= '{}'".format(dttimenow)
            sql += " and id_tel_driver = {}".format(id_tel)

        if is_active is False and me_user is True:
            sql += " where id_tel_user = {}".format(id_tel)

        if is_active is False and me_driver is True:
            sql += " where id_tel_driver = {}".format(id_tel)

        sql += " order by {}".format('route_datetime asc')

        cur.execute(sql)
        cur.fetchall

        for row in cur:
            route = {}
            route['id'] = row[0]
            route['route_date'] = row[1].strftime('%d.%m.%Y')
            route['route_time'] = row[2]
            route['route_datetime'] = row[3]
            route['route_created'] = row[4]
            route['from_city'] = row[5]
            route['from_street'] = row[6]
            route['from_house'] = row[7]
            route['to_city'] = row[8]
            route['to_street'] = row[9]
            route['to_house'] = row[10]
            route['id_tel_driver'] = row[11]
            route['id_tel_user'] = row[12]
            route['cost_rub'] = row[13]
            route['driver_comment'] = row[14]
            route['user_comment'] = row[15]
            route['driver_nick'] = row[16]
            route['driver_phone'] = row[17]
            route['plate'] = row[18]
            route['mark'] = row[19]
            route['model'] = row[20]
            route['user_nick'] = row[21]
            route['user_phone'] = row[22]
            routeslist[route['id']] = route

    disconnect(connection_)
    return routeslist


def set_route_in_db(data, id_tel):
    connection_ = getconnect()
    with connection_.cursor() as cur:
        sql = 'insert into vidnovoz_routes (route_date, route_time, route_datetime, ' \
              'from_city, from_street, from_house, ' \
              'to_city, to_street, to_house, ' \
              'id_tel_driver, cost_rub, driver_comment, driver_chat_id) values ' \
              '("{}", "{}", "{}", ' \
              '"{}", "{}", "{}", ' \
              '"{}", "{}", "{}", ' \
              '{}, {}, "{}", {}' \
              ')'.format(data["rdate"], data["rtime"], data["rdt"],
                         data["fcity"][:40], data["fstreet"][:40], data["fhouse"][:40],
                         data["tcity"][:40], data["tstreet"][:40], data["thouse"][:40],
                         id_tel, data["costr"], data["drcmnt"][:140], data["driver_chat_id"], )
        cur.execute(sql)
    disconnect(connection_)


def take_place(id_place, id_tel_user):
    connection_ = getconnect()
    driver_chat_id = -1
    with connection_.cursor() as cur:
        sql = 'select driver_chat_id from vidnovoz_routes where id_tel_user = {} and id = {}'.format(str(0), str(id_place))
        cur.execute(sql)
    if cur.rowcount > 0:
        for row in cur:
            driver_chat_id = row[0]
        with connection_.cursor() as cur:
            sql = 'update vidnovoz_routes set id_tel_user = {} where id = {}'.format(str(id_tel_user), str(id_place))
            cur.execute(sql)
    disconnect(connection_)
    return driver_chat_id


def leave_place(id_place, id_tel):
    connection_ = getconnect()
    driver_chat_id = -1
    with connection_.cursor() as cur:
        sql = 'select driver_chat_id from vidnovoz_routes where id_tel_user = {} and id = {}'.format(str(id_tel), str(id_place))
        cur.execute(sql)
    if cur.rowcount > 0:
        for row in cur:
            driver_chat_id = row[0]
        with connection_.cursor() as cur:
            sql = 'update vidnovoz_routes set id_tel_user = 0 where id = {} and id_tel_user = {}'.format(str(id_place), str(id_tel))
            cur.execute(sql)
    disconnect(connection_)
    #return 'Место {} успешно освобождено'.format(str(id_place)), driver_chat_id
    return 'Place {} is free now'.format(str(id_place)), driver_chat_id


def delete_place(id_place, id_tel):
    connection_ = getconnect()

    with connection_.cursor() as cur:
        sql = 'select count(*) from vidnovoz_routes where id={} and id_tel_user > 0 and id_tel_driver = {}'.format(str(id_place), str(id_tel))
        cur.execute(sql)

    for row in cur:
        if row[0] > 0:
            # кто-то занял место
            #mess = 'Место {} занято, нельзя удалить. Список созданных вами мест: /{}'.format(str(id_place), routes.Route.driver_created_places)
            mess = 'Place {} taken, can`t delete. List of places created: /{}'.format(str(id_place),
                                                                                             routes.Route.driver_created_places)
            disconnect(connection_)
            return mess
    else:
        with connection_.cursor() as cur:
            sql = 'delete from vidnovoz_routes where id = {} and id_tel_driver = {}'.format(str(id_place), str(id_tel))
            cur.execute(sql)
        mess = 'Place deleted'
        disconnect(connection_)
        return mess