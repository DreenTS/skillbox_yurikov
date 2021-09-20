import datetime
import os
import re
import time

import requests
from bs4 import BeautifulSoup

from db_init import *


class WrongCityNameError(Exception):

    def __str__(self):
        return '\nWrongCityNameError: имя введённого населённого пункта не найдено в базе.'


class WrongDateRangeError(Exception):

    def __str__(self):
        return '\nWrongDateRangeError: введён неправильный диапазон дат: ' \
               'нижняя граница должна быть строго меньше верхней границы.'


class WeatherForecaster:

    def __init__(self, location_for_forecast=None, date_for_forecast=None):
        self.data_for_parsing = settings.DATA_FOR_PARSING
        self.date_for_forecast = date_for_forecast or []
        self.location_for_forecast = location_for_forecast
        self.url_for_forecast = None
        self.forecast_data = []
        self.database = DatabaseUpdater()

    def forecast_to_db(self):
        self._user_location_choice()
        self._user_date_choice()
        self._get_forecast_by_date()
        self.database._add_forecasts(forecasts=self.forecast_data)
        self.forecast_data.clear()

    def forecast_from_db(self):
        pass

    def print_forecast(self):
        print(f'Населённый пункт: {self.location_for_forecast["name"]}')
        for content in self.forecast_data:
            for k, v in content.items():
                if k == 'location':
                    continue
                elif k == 'forecast_date':
                    print(f'\n{datetime.date.strftime(content["forecast_date"], "%d.%m")}:')
                else:
                    print(f'\t{v}')

    def _get_forecast_by_date(self):
        if len(self.date_for_forecast) == 1:
            self._get_forecast_from_network()
        else:
            first_date, second_date = self.date_for_forecast
            self.date_for_forecast.clear()
            while first_date <= second_date:
                self.date_for_forecast.append(first_date)
                first_date += datetime.timedelta(days=1)
            self._get_forecast_from_network()

    def _get_forecast_from_network(self):
        fieldnames = settings.FIELDNAMES_FOR_DB
        for date in self.date_for_forecast:
            date_url = datetime.date.strftime(date, '%d-%B').lower()
            response = requests.get(self.url_for_forecast + date_url)
            if response.status_code == 200:
                html_doc = BeautifulSoup(response.text, features='html.parser')
                tag_list = html_doc.find_all('div', {'class': self.data_for_parsing['classes_for_html_tag'][1]})
                for tags in tag_list:
                    day_tags = tags.find_all('div', {'class': self.data_for_parsing['classes_for_html_tag'][2]})
                    for tag in day_tags:
                        if 'Днем' in str(tag):
                            temperature = re.search(self.data_for_parsing['forecast_re'][0], str(tag)).group()[5:-1]
                            description = re.search(self.data_for_parsing['forecast_re'][1], str(tag)).group()[7:-1]
                            pressure = re.search(self.data_for_parsing['forecast_re'][2], str(tag)).group()
                            humidity = re.search(self.data_for_parsing['forecast_re'][3], str(tag)).group()
                            wind = re.search(self.data_for_parsing['forecast_re'][4], str(tag)).group()
                            precipitation = re.search(self.data_for_parsing['forecast_re'][5], str(tag)).group()
                            self.forecast_data.append(
                                {
                                    fieldnames[0]: self.location_for_forecast,
                                    fieldnames[1]: date,
                                    fieldnames[2]: f'Температура: {temperature}',
                                    fieldnames[3]: description[0].upper() + description[1:],
                                    fieldnames[4]: pressure,
                                    fieldnames[5]: humidity,
                                    fieldnames[6]: wind,
                                    fieldnames[7]: precipitation,
                                }
                            )
                            break
                    break

    def _user_location_choice(self):
        if self.location_for_forecast is not None:
            formatted_user_input = self.location_for_forecast.lower().replace('ё', 'е')
            try:
                if formatted_user_input[0].isdigit():
                    raise WrongCityNameError
                self.location_for_forecast, self.url_for_forecast = self._get_city_from_network(formatted_user_input)
            except WrongCityNameError as exc:
                print(exc)
        else:
            is_ok_choice = False
            while not is_ok_choice:
                user_input = input('\nВведите название населённого пункта: ')
                formatted_user_input = user_input.lower().replace('ё', 'е')
                try:
                    if formatted_user_input[0].isdigit():
                        raise WrongCityNameError
                    self.location_for_forecast, self.url_for_forecast = self._get_city_from_network(formatted_user_input)
                    is_ok_choice = True
                except WrongCityNameError as exc:
                    print(f'{exc}\nДавайте попробуем ещё раз', end='')
                    self._dots()

    def _get_city_from_network(self, user_choice):
        res = []
        eng_letter = settings.LETTERS_IN_TRANSCRIPTION[user_choice[0].upper()]

        response = requests.get(self.data_for_parsing['locations_list_url'] + eng_letter)
        if response.status_code == 200:
            html_doc = BeautifulSoup(response.text, features='html.parser')
            tag_list = html_doc.find_all('div', {'class': self.data_for_parsing['classes_for_html_tag'][0]})
            for tags in tag_list:
                location_name = re.search(self.data_for_parsing['location_name_re'],
                                          str(tags).replace('ё', 'е')).group()[3:-1]
                if user_choice == location_name.lower():
                    location_url = re.search(self.data_for_parsing['location_url_re'], str(tags)).group()[6:-1]
                    res.append(location_name)
                    res.append(settings.BASE_URL + location_url)
                    break
            else:
                raise WrongCityNameError
        return res

    def _user_date_choice(self):
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
    forecaster = WeatherForecaster()
    forecaster.forecast_to_db()
    forecaster.forecast_from_db()
