import re

BASE_URL = 'https://pogoda.mail.ru'
CITY_URL_COMP = re.compile(r'href="[a-z\-_/]+"')
CITY_NAME_COMP = re.compile(r'/">[а-яА-Я\-\s]+<')

DATA_FOR_PARSING = {
    'cities_list_url': BASE_URL + '/country/russia/',
    'city_class_for_html_tag': 'city-list__simple',
    'url_re': CITY_URL_COMP,
    'name_re': CITY_NAME_COMP,
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
