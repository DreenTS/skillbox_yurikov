import peewee
import settings

DATABASE_PROXY = peewee.DatabaseProxy()


class DatabaseUpdater:

    def __init__(self):
        self.db_name = settings.DB_NAME
        self.proxy = DATABASE_PROXY

    def run(self, mode, **kwargs):
        database = peewee.SqliteDatabase(self.db_name)
        self.proxy.initialize(database)
        self.proxy.connect()
        database.create_tables([Location, Forecast])

        if mode == 'add':
            return self._add_forecasts(data=kwargs)
        elif mode == 'get':
            return self._get_forecasts(data=kwargs)

        self.proxy.close()
        database.close()

    def _add_forecasts(self, data):
        loc_data = data['data']
        try:
            location_to_save = Location.get(Location.name == loc_data[0][settings.FIELDNAMES_FOR_DB[0]])
        except peewee.DoesNotExist:
            location_to_save = Location(name=loc_data[0][settings.FIELDNAMES_FOR_DB[0]])
            location_to_save.save()
        for forecast in loc_data:
            forecast[settings.FIELDNAMES_FOR_DB[0]] = location_to_save
            try:
                _ = Forecast.get(Forecast.forecast_date == forecast[settings.FIELDNAMES_FOR_DB[1]],
                                 Forecast.location == location_to_save)
            except peewee.DoesNotExist:
                Forecast.insert_many(forecast).execute()
        print('\nПрогноз сохранён в БД!')

    def _get_forecasts(self, data):
        loc_data = data['data']
        location = Location.get(Location.name == loc_data[0])
        result = []
        for date in loc_data[1]:
            forecast = Forecast.get(Forecast.location == location, Forecast.forecast_date == date)
            result.append(forecast)
        return result


class BaseTable(peewee.Model):
    class Meta:
        database = DATABASE_PROXY


class Location(BaseTable):
    name = peewee.CharField()


class Forecast(BaseTable):
    location = peewee.ForeignKeyField(Location)
    forecast_date = peewee.DateTimeField()
    temperature = peewee.CharField()
    description = peewee.CharField()
    pressure = peewee.CharField()
    humidity = peewee.CharField()
    wind = peewee.CharField()
    precipitation = peewee.CharField()
