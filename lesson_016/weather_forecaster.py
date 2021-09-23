import datetime
import os
import re

import requests
from bs4 import BeautifulSoup

from db_init import *
import settings
import image_maker


class WrongLocationError(Exception):

    def __str__(self):
        return '\nWrongLocationError: имя введённого населённого пункта введено неверно или не найдено в базе.'


class DateFormatError(Exception):

    def __str__(self):
        return '\nDateFormatError: Дата должна быть в формате ДД.ММ или ДД.ММ-ДД.ММ'


class DateRangeError(Exception):

    def __str__(self):
        return '\nDateRangeError: введён неправильный диапазон дат: ' \
               'нижняя граница должна быть строго меньше верхней границы.'


class MaxDateError(Exception):

    def __init__(self):
        self.today = datetime.date.today()

    def __str__(self):
        return f'\nMaxDateError: Максимальная дата прогноза - сегодняшняя дата ' \
               f'({datetime.date.strftime(self.today, "%d.%m.%Y")}) + 2 недели.'


class WeatherForecaster:

    def __init__(self):
        self.data_for_parsing = settings.DATA_FOR_PARSING
        self.date_for_forecast = []
        self.location_for_forecast = None
        self.url_for_forecast = None
        self.forecast_data = []
        self.database = DatabaseUpdater()
        self._need_date_check = True

    def add_forecast(self, date, location):
        user_date = date.split('-')
        try:
            if self._need_date_check:
                self._date_check(dates=user_date)
            self._need_date_check = True
            self.location_for_forecast, self.url_for_forecast = self._get_loc_data_from_network(location)
            self._get_forecast_by_date()
            self._add_to_db()
            self._clear()
        except (DateFormatError, DateRangeError, MaxDateError, WrongLocationError) as exc:
            print(exc)
            os.system('exit')

    def get_forecast(self, date, location, mode):
        if mode not in ['console', 'image']:
            print('\nЗначение аргумента mode должно быть "console" или "image".')
            os.system('exit')
        fieldnames = settings.FIELDNAMES_FOR_DB
        user_date = date.split('-')
        try:
            self._date_check(dates=user_date)
            self._need_date_check = False
            self.location_for_forecast = location
            forecast = self._get_from_db()
            for f in forecast:
                self.forecast_data.append({
                                    fieldnames[0]: f.location.name,
                                    fieldnames[1]: f.forecast_date,
                                    fieldnames[2]: f.temperature,
                                    fieldnames[3]: f.description,
                                    fieldnames[4]: f.pressure,
                                    fieldnames[5]: f.humidity,
                                    fieldnames[6]: f.wind,
                                    fieldnames[7]: f.precipitation,
                                })
        except peewee.DoesNotExist:
            self.add_forecast(date=date, location=location)
        except (DateFormatError, DateRangeError, MaxDateError) as exc:
            print(exc)
            os.system('exit')

        if mode == 'console':
            self._print_forecast()
        elif mode == 'image':
            self._draw_forecast()
        self._clear()

    def _date_check(self, dates):
        if self._need_date_check:
            for date in dates:
                date += '.2021'
                self.date_for_forecast.append(datetime.datetime.strptime(date, '%d.%m.%Y').date())

            if len(self.date_for_forecast) > 2:
                raise DateFormatError
            elif len(self.date_for_forecast) == 2:
                if self.date_for_forecast[1] - self.date_for_forecast[0] <= datetime.timedelta(days=0):
                    raise DateRangeError

            today = datetime.date.today()
            for date in self.date_for_forecast:
                if date - today > datetime.timedelta(days=13):
                    raise MaxDateError

    def _get_from_db(self):
        mode = 'get'
        data = [self.location_for_forecast, self.date_for_forecast]
        return self.database.run(mode=mode, data=data)

    def _add_to_db(self):
        mode = 'add'
        data = self.forecast_data
        self.database.run(mode=mode, data=data)

    def _get_loc_data_from_network(self, user_choice):
        res = []
        formatted_user_choice = user_choice.lower().replace('ё', 'е')
        if formatted_user_choice[0].isdigit():
            raise WrongLocationError
        try:
            eng_letter = settings.LETTERS_IN_TRANSCRIPTION[formatted_user_choice[0].upper()]
        except KeyError:
            raise WrongLocationError

        response = requests.get(self.data_for_parsing['locations_list_url'] + eng_letter)
        if response.status_code == 200:
            html_doc = BeautifulSoup(response.text, features='html.parser')
            tag_list = html_doc.find_all('div', {'class': self.data_for_parsing['classes_for_html_tag'][0]})
            for tags in tag_list:
                location_name = re.search(self.data_for_parsing['location_name_re'],
                                          str(tags).replace('ё', 'е')).group()[3:-1]
                if formatted_user_choice == location_name.lower():
                    location_url = re.search(self.data_for_parsing['location_url_re'], str(tags)).group()[6:-1]
                    res.append(location_name)
                    res.append(settings.BASE_URL + location_url)
                    break
            else:
                raise WrongLocationError
        return res

    def _get_forecast_by_date(self):
        if len(self.date_for_forecast) == 1:
            self._from_network()
        else:
            first_date, second_date = self.date_for_forecast
            self.date_for_forecast.clear()
            while first_date <= second_date:
                self.date_for_forecast.append(first_date)
                first_date += datetime.timedelta(days=1)
            self._from_network()

    def _from_network(self):
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
                            temperature = re.search(self.data_for_parsing['forecast_re'][0], str(tag)).group()[5:-2]
                            description = re.search(self.data_for_parsing['forecast_re'][1], str(tag)).group()[7:-1]
                            pressure = re.search(self.data_for_parsing['forecast_re'][2], str(tag)).group()
                            humidity = re.search(self.data_for_parsing['forecast_re'][3], str(tag)).group()
                            wind = re.search(self.data_for_parsing['forecast_re'][4], str(tag)).group()
                            try:
                                precipitation = re.search(self.data_for_parsing['forecast_re'][5], str(tag)).group()
                            except AttributeError:
                                precipitation = 'Вероятность осадков - неизвестно'
                            self.forecast_data.append(
                                {
                                    fieldnames[0]: self.location_for_forecast,
                                    fieldnames[1]: date,
                                    fieldnames[2]: f'Температура: {temperature} град. С',
                                    fieldnames[3]: description[0].upper() + description[1:],
                                    fieldnames[4]: pressure,
                                    fieldnames[5]: humidity,
                                    fieldnames[6]: wind,
                                    fieldnames[7]: precipitation,
                                }
                            )
                            break
                    break

    def _print_forecast(self):
        print(f'Населённый пункт: {self.location_for_forecast}')
        for content in self.forecast_data:
            for k, v in content.items():
                if k == 'location':
                    continue
                elif k == 'forecast_date':
                    print(f'\n{datetime.date.strftime(content["forecast_date"], "%d.%m")}:')
                else:
                    print(f'\t{v}')

    def _draw_forecast(self):
        img_maker = image_maker.ImageMaker(forecasts=self.forecast_data)
        img_maker.draw()
        self._clear()

    def _clear(self):
        self.date_for_forecast.clear()
        self.location_for_forecast = None
        self.url_for_forecast = None
        self.forecast_data.clear()
        self._need_date_check = True


if __name__ == '__main__':
    forecaster = WeatherForecaster()
    forecaster.add_forecast(date='23.09-26.09', location='Москва')
    forecaster.get_forecast(date='24.09-25.09', location='Москва', mode='console')
    forecaster.add_forecast(date='12.07', location='Комсомольск-на-Амуре')
    forecaster.get_forecast(date='12.07', location='Комсомольск-на-Амуре', mode='image')
