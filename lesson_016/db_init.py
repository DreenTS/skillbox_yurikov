import peewee
import settings

DATABASE_PROXY = peewee.DatabaseProxy()


class DatabaseUpdater:
    """
    Класс для работы с базой данных.
    Функционал: добавление или получение прогнозов с БД.

    """

    def __init__(self):
        self.db_name = settings.DB_NAME
        self.proxy = DATABASE_PROXY

    def run(self, mode, data):
        """
        Запуск работы с БД.

        Инициализирует БД и подключается к ней.
        В зависимости от значение аргумента mode вызывает метод добавления или получения прогнозов.
        После отработки методов, закрывает подключение к БД.

        :param mode: str, режим работы
        :param data: list, данные для добавления или получения прогнозов
        :return: None or list, список полученных из БД прогнозов
        """

        database = peewee.SqliteDatabase(self.db_name)
        self.proxy.initialize(database)
        self.proxy.connect()
        database.create_tables([Location, Forecast])

        if mode == 'add':
            self._add_forecasts(data=data)
        elif mode == 'get':
            return self._get_forecasts(data=data)

        self.proxy.close()
        database.close()

    def _add_forecasts(self, data):
        """
        Добавление прогнозов в БД.

        Выполняет запросы к БД:
        1) Пытается получить запись из таблицы Location по названию населённого пункта
        2) Если запись отсутствует, добавляет запись в таблицу
        3) Если запись прогноза отсутствует в БД - добавляет прогноз в таблицу Forecast

        :param data: list, данные для добавления прогнозов
        :return: None
        """

        try:
            location_to_save = Location.get(Location.name == data[0][settings.FIELDNAMES_FOR_DB[0]])
        except peewee.DoesNotExist:
            location_to_save = Location(name=data[0][settings.FIELDNAMES_FOR_DB[0]])
            location_to_save.save()
        for forecast in data:
            forecast[settings.FIELDNAMES_FOR_DB[0]] = location_to_save
            try:
                _ = Forecast.get(Forecast.forecast_date == forecast[settings.FIELDNAMES_FOR_DB[1]],
                                 Forecast.location == location_to_save)
            except peewee.DoesNotExist:
                Forecast.insert_many(forecast).execute()
                print('\nПрогноз сохранён в БД!')

    def _get_forecasts(self, data):
        """
        Получение прогнозов из БД.

        Выполняет запросы к БД:
        1) Пытается получить запись из таблицы Location по названию населённого пункта
        2) Если запись отсутствует, вызывает иключение, которое ловится в weather_forecaster.py
        3) ытается получить запись из таблицы Forecast по названию населённого пункта и датам
        4) см. шаг 3

        :param data: list, данные для добавления прогнозов
        :return: list, список полученных из БД прогнозов
        """

        location = Location.get(Location.name == data[0])
        result = []
        for date in data[1]:
            forecast = Forecast.get(Forecast.location == location, Forecast.forecast_date == date)
            result.append(forecast)
        return result


class BaseTable(peewee.Model):
    class Meta:
        database = DATABASE_PROXY


class Location(BaseTable):
    """
    Таблица "Населённый пункт".
    Поля:
    - name: CharField, название населённого пункта

    """

    name = peewee.CharField()


class Forecast(BaseTable):
    """
    Таблица "Прогноз".
    Поля:
    - location: ForeignKeyField, внешний ключ на населённый пункт
    - forecast_date: DateTimeField, дата прогноза
    - temperature: CharField, температура
    - description: CharField, "описание" погода (ясно, дождь, облачно...)
    - pressure: CharField, давление
    - humidity: CharField, влажность
    - wind: CharField, скорость ветра
    - precipitation: CharField, вероятность осадков

    """

    location = peewee.ForeignKeyField(Location)
    forecast_date = peewee.DateTimeField()
    temperature = peewee.CharField()
    description = peewee.CharField()
    pressure = peewee.CharField()
    humidity = peewee.CharField()
    wind = peewee.CharField()
    precipitation = peewee.CharField()
