import datetime
import settings
import re

CITY_PATTERN = re.compile(r'^((калининград)|(краснодар)|(новосибирск)|(владивосток)|(лондон)'
                          r'|(париж)|(вашингтон)|(берлин))[аеу]*|(токио)$')
PHONE_NUMBER_PATTERN = re.compile(r'^\+7[0-9]{10}$')


def city_handler(text, context, step):
    match = re.match(CITY_PATTERN, text)
    if match:
        city = [c for c in settings.FLIGHTS.keys() if c in text][0]
        if step == '1':
            context['departure_city'] = city
        elif step == '2':
            if city in settings.FLIGHTS[context['departure_city']].keys():
                context['arrival_city'] = city
            else:
                return False
        return True
    else:
        return False


def date_handler(text, context):
    try:
        datetime.datetime.strptime(text, '%d-%m-%Y')
        context['date'] = text
        return True
    except ValueError:
        return False


def flight_handler(text, context):
    flights_list = settings.FLIGHTS[context['departure_city']][context['arrival_city']]
    if text.isdigit():
        if int(text) - 1 in range(len(flights_list)):
            context['flight'] = flights_list[int(text) - 1]
            return True
    return False


def number_of_seats_handler(text, context):
    if text.isdigit():
        if int(text) in range(1, 6):
            context['number_of_seats'] = int(text)
            return True
    return False


def comment_handler(text, context):
    context['comment'] = text
    return True


def data_checking_handler(text, context):
    if text == 'да':
        return True
    else:
        return False


def phone_number_handler(text, context):
    match = re.match(PHONE_NUMBER_PATTERN, text)
    if match:
        context['phone_number'] = text
        return True
    else:
        return False
