import re

BASE_URL = 'https://pogoda.mail.ru'
LOCATION_URL_COMP = re.compile(r'href="[a-z\-_/]+"')
LOCATION_NAME_COMP = re.compile(r'/">[а-яА-Я\-\s,.]+<')
TEMPERATURE_COMP = re.compile(r'ure">[0-9°+-]+<')
DESCRIPTION_COMP = re.compile(r'title="[а-яА-Я\s\-,]+"')
PRESSURE_COMP = re.compile(r'Давление: [0-9]+ мм рт\. ст\.')
HUMIDITY_COMP = re.compile(r'Влажность: [0-9]+%')
WIND_COMP = re.compile(r'Ветер: [0-9]+ м/c')
PRECIPITATION_COMP = re.compile(r'Вероятность осадков: [0-9]+%')

DB_NAME = 'forecast.db'
FIELDNAMES_FOR_DB = ['location', 'forecast_date', 'temperature', 'description', 'pressure',
                     'humidity', 'wind', 'precipitation']

DATA_FOR_PARSING = {
    'locations_list_url': BASE_URL + '/country/russia/',
    'classes_for_html_tag': [
        'city-list__simple',
        'cols__column__item cols__column__item_2-1 cols__column__item_2-1_ie8',
        'day day_period',
    ],
    'location_url_re': LOCATION_URL_COMP,
    'location_name_re': LOCATION_NAME_COMP,
    'forecast_re': [
        TEMPERATURE_COMP,
        DESCRIPTION_COMP,
        PRESSURE_COMP,
        HUMIDITY_COMP,
        WIND_COMP,
        PRECIPITATION_COMP,
    ]
}

LETTERS_IN_TRANSCRIPTION = {
    'А': 'a',
    'Б': 'b',
    'В': 'v',
    'Г': 'g',
    'Д': 'd',
    'Е': 'e',
    'Ж': 'zh',
    'З': 'z',
    'И': 'i',
    'Й': 'j',
    'К': 'k',
    'Л': 'l',
    'М': 'm',
    'Н': 'n',
    'О': 'o',
    'П': 'p',
    'Р': 'r',
    'С': 's',
    'Т': 't',
    'У': 'u',
    'Ф': 'f',
    'Х': 'h',
    'Ц': 'c',
    'Ч': 'ch',
    'Ш': 'sh',
    'Щ': 'sch',
    'Ы': 'y',
    'Э': 'eh',
    'Ю': 'yu',
    'Я': 'ya',
}
