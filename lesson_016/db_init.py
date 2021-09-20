import peewee
import settings

DATABASE_PROXY = peewee.DatabaseProxy()


class DatabaseUpdater:

    def __init__(self):
        self.db_name = settings.DB_NAME
        self.proxy = DATABASE_PROXY

    def _add_forecasts(self, forecasts):
        database = peewee.SqliteDatabase(self.db_name)
        self.proxy.initialize(database)
        self.proxy.connect()

        database.create_tables([Locality, Forecast])
        try:
            locality_to_save = Locality.get(Locality.name == forecasts[0][settings.FIELDNAMES_FOR_DB[0]])
        except peewee.DoesNotExist:
            locality_to_save = Locality(name=forecasts[0][settings.FIELDNAMES_FOR_DB[0]])
            locality_to_save.save()
        for frcst in forecasts:
            frcst[settings.FIELDNAMES_FOR_DB[0]] = locality_to_save
        _forecasts_to_save = Forecast.insert_many(forecasts).execute()
        print('Прогноз сохранён в БД!')

        self.proxy.close()
        database.close()


class BaseTable(peewee.Model):
    class Meta:
        database = DATABASE_PROXY


class Locality(BaseTable):
    name = peewee.CharField()


class Forecast(BaseTable):
    locality = peewee.ForeignKeyField(Locality)
    forecast_date = peewee.DateTimeField()
    temperature = peewee.CharField()
    description = peewee.CharField()
    pressure = peewee.CharField()
    humidity = peewee.CharField()
    wind = peewee.CharField()
    precipitation = peewee.CharField()
