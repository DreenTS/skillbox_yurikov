import os
import time

import settings


class WrongCityNameError(Exception):

    def __str__(self):
        return '\nWrongCityNameError: имя введённого населённого пункта не найдено в базе.'


class WeatherForecaster:

    def __init__(self, date_for_forecast):
        self.data_for_parsing = settings.DATA_FOR_PARSING
        self.date_for_forecast = date_for_forecast
        self.city_for_forecast = None

    def forecast(self):
        self._user_location_choice()

    def _user_location_choice(self):
        is_ok_choice = False
        while not is_ok_choice:
            user_input = input('\nВведите название населённого пункта: ')
            formatted_user_input = user_input.lower().replace('ё', 'е')
            try:
                self.city_for_forecast = self._get_city_from_network(formatted_user_input)
                is_ok_choice = True
            except WrongCityNameError as exc:
                print(f'{exc}\nДавайте попробуем ещё раз', end='')
                self._dots()

    def _get_city_from_network(self, user_choice):
        return 'city'

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