"""
Файл функций-обработчиков для шагов сценариев.

"""

import datetime
import settings
import re

CITY_PATTERN = re.compile(r'^((калининград)|(краснодар)|(новосибирск)|(владивосток)|(лондон)'
                          r'|(париж)|(вашингтон)|(берлин))[аеу]*|(токио)$')

PHONE_NUMBER_PATTERN = re.compile(r'^\+7[0-9]{10}$')


def city_handler(text, context, step):
    """
    Обработчик городов отправления и прибытия.

    Производит матч по паттерну.
    Если не находит соответствие, возвращается False.
    Если находит соответствие, получает название города из конфига
    и начинает обработку города отправления/прибытия и добавляет его в контекст пользователя
    (в зависимости от номера шага).

    Было решено не разделять обработку двух городов на два отдельных хендлера,
    а просто добавить дополнительный аргумент - step, номер шага.
    Шаги идут последовательно друг за другом, поэтому не возникнет KeyError
    при получении названия города отправления из контекста пользователя.

    :param text: str, текст сообщения пользователя
    :param context: dict, контекст текущего пользователя
    :param step: str, номер шага для обработки города отправления или города прибытия
    :return: bool, прошёл ли текст сообщения пользователя валидацию
    """

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
    """
    Обработчик даты рейса от пользователя.

    Если не получается преобразовать дату в datetime.datetime объект,
    вызывается исключение ValueError, возвращается False.
    В ином случае, если дата представлена в валидном формате,
    она добавляется в контекст пользователя, возвращается True.

    :param text: str, текст сообщения пользователя
    :param context: dict, контекст текущего пользователя
    :return: bool, прошёл ли текст сообщения пользователя валидацию
    """

    try:
        datetime.datetime.strptime(text, '%d-%m-%Y')
        context['date'] = text
        return True
    except ValueError:
        return False


def flight_handler(text, context):
    """
    Обработчик выбора рейса из списка представленных.

    Формируется список подходящих рейсов из конфига.
    Если текст - цифра, входящая в диапазон длины списка рейсов,
    выбранный рейс по индексу добавляется в контекст пользователя.

    :param text: str, текст сообщения пользователя
    :param context: dict, контекст текущего пользователя
    :return: bool, прошёл ли текст сообщения пользователя валидацию
    """

    flights_list = settings.FLIGHTS[context['departure_city']][context['arrival_city']]
    if text.isdigit():
        if int(text) - 1 in range(len(flights_list)):
            context['flight'] = flights_list[int(text) - 1]
            return True
    return False


def number_of_seats_handler(text, context):
    """
    Обработчик количества мест.

    Проверяет, является ли текст числом, входящим в диапазон количества мест.
    При успешной валидаци, количество мест добавляется в контекст пользователя.

    :param text: str, текст сообщения пользователя
    :param context: dict, контекст текущего пользователя
    :return: bool, прошёл ли текст сообщения пользователя валидацию
    """

    if text.isdigit():
        if int(text) in range(1, 6):
            context['number_of_seats'] = int(text)
            return True
    return False


def comment_handler(text, context):
    """
    Обработчик комментария.

    Добавляет комментарий пользователя в контекст.
    Всегде возвращает True.

    :param text: str, текст сообщения пользователя
    :param context: dict, контекст текущего пользователя
    :return: bool
    """

    context['comment'] = text
    return True


def data_checking_handler(text, context):
    """
    Обработчик подтверждения введённых данных.

    При любом ответе, кроме положительного ('да'), сценарий завершится.

    :param text: str, текст сообщения пользователя
    :param context: dict, контекст текущего пользователя
    :return: bool
    """

    if text == 'да':
        return True
    else:
        return False


def phone_number_handler(text, context):
    """
    Обработчик номера телефона.

    Производит матч по паттерну.
    Если не находит соответствие, возвращается False.
    Если находит соответствие, добавляет номер в контекст пользователя.

    :param text: str, текст сообщения пользователя
    :param context: dict, контекст текущего пользователя
    :return: bool, прошёл ли текст сообщения пользователя валидацию
    """

    match = re.match(PHONE_NUMBER_PATTERN, text)
    if match:
        context['phone_number'] = text
        return True
    else:
        return False
