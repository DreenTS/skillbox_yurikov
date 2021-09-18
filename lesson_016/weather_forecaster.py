import datetime
import os
import re
import time

import requests
from bs4 import BeautifulSoup

import settings


class WrongCityNameError(Exception):

    def __str__(self):
        return '\nWrongCityNameError: имя введённого населённого пункта не найдено в базе.'


class WrongDateRangeError(Exception):

    def __str__(self):
        return '\nWrongDateRangeError: введён неправильный диапазон дат: ' \
               'нижняя граница должна быть строго меньше верхней границы.'


class WeatherForecaster:

    def __init__(self, date_for_forecast=None):
        self.data_for_parsing = settings.DATA_FOR_PARSING
        self.date_for_forecast = date_for_forecast or []
        self.city_for_forecast = None

    def forecast(self):
        self._user_location_choice()
        if not self.date_for_forecast:
            self._date_input()
        else:
            self.date_for_forecast = self.date_for_forecast.split('-')
            try:
                self._date_check(dates=self.date_for_forecast)
            except (ValueError, WrongDateRangeError) as exc:
                self.date_for_forecast.clear()
                print(f'{exc}\nДата должна быть в формате ДД.ММ или ДД.ММ-ДД.ММ , Давайте попробуем ещё раз', end='')
                self._dots()
                self._date_input()

    def _user_location_choice(self):
        is_ok_choice = False
        while not is_ok_choice:
            user_input = input('\nВведите название населённого пункта: ')
            formatted_user_input = user_input.lower().replace('ё', 'е')
            try:
                if formatted_user_input[0].isdigit():
                    raise WrongCityNameError
                self.city_for_forecast = self._get_city_from_network(formatted_user_input)
                is_ok_choice = True
            except WrongCityNameError as exc:
                print(f'{exc}\nДавайте попробуем ещё раз', end='')
                self._dots()

    def _get_city_from_network(self, user_choice):
        city = {}
        eng_letter = settings.LETTERS_IN_TRANSCRIPTION[user_choice[0].upper()]

        response = requests.get(self.data_for_parsing['cities_list_url'] + eng_letter)
        if response.status_code == 200:
            html_doc = BeautifulSoup(response.text, features='html.parser')
            tag_list = html_doc.find_all('div', {'class': self.data_for_parsing['city_class_for_html_tag']})
            for tags in tag_list:
                city_name = re.search(self.data_for_parsing['name_re'], str(tags)).group()[3:-1]
                if user_choice == city_name.lower():
                    city_url = re.search(self.data_for_parsing['url_re'], str(tags)).group()[6:-1]
                    city['city'] = city_name
                    city['url'] = settings.BASE_URL + city_url
                    break
            else:
                raise WrongCityNameError
        return city

    def _date_input(self):
        while not self.date_for_forecast:
            print('\nДата прогноза.')
            user_dates = input('Введите дату в формате ДД.ММ,\n'
                               'или диапазон дат в формате ДД.ММ-ДД.ММ (текущий год): ').split('-')
            try:
                self._date_check(dates=user_dates)
            except (ValueError, WrongDateRangeError) as exc:
                self.date_for_forecast.clear()
                print(f'{exc}\nДата должна быть в формате ДД.ММ или ДД.ММ-ДД.ММ , Давайте попробуем ещё раз', end='')
                self._dots()

    def _date_check(self, dates):
        for date in dates:
            date += '.2021'
            self.date_for_forecast.append(datetime.datetime.strptime(date, '%d.%m.%Y').date())

        if len(self.date_for_forecast) > 2:
            raise ValueError
        elif len(self.date_for_forecast) == 2:
            if self.date_for_forecast[1] - self.date_for_forecast[0] <= datetime.timedelta(days=0):
                raise WrongDateRangeError

        today = datetime.date.today()
        for date in self.date_for_forecast:
            if date - today > datetime.timedelta(days=13):
                raise ValueError(f'Максимальная дата прогноза - сегодняшняя дата '
                                 f'({datetime.date.strftime(today, "%d.%m.%Y")}) + 2 недели.\nНапоминание:')

    def _dots(self):
        """
        Вспомогательный метод.
        Выводит на экран точки с задержкой и очищает экран.

        :return: None
        """
        for _ in range(3):
            print('.', end='')
            time.sleep(1.5)
        os.system('cls')


if __name__ == '__main__':
    forecaster = WeatherForecaster(date_for_forecast='')
    forecaster.forecast()
    print(forecaster.city_for_forecast)
    print(forecaster.date_for_forecast)