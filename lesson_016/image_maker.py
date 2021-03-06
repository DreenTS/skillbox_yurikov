import datetime

import settings
import cv2


class ImageMaker:
    """
    Класс для создания изображений с прогнозами ("открыток"),
    используя заготовки изображений.

    """

    def __init__(self, forecasts):
        self.templates = settings.IMAGE_TEMPLATES
        self.themes_patterns = settings.THEMES_PATTERNS
        self.forecasts = forecasts

    def draw(self):
        """
        Запуск отрисовки.

        Проходится циклом по списку переданных прогнозов:
        1) Определяет тему оформления изображения
        2) Красит в градиент заготовку заднего фона и добавляет на него лого (цвет и лого зависят от темы)
        3) Печатает текст на изображении
        4) Сохраняет изображение

        :return: None
        """

        for forecast in self.forecasts:
            theme = self._get_themes(forecast=forecast)
            background_and_logo = self._gradient_and_logo(theme=theme)
            finished_image = self._print_text(forecast=forecast, src=background_and_logo)
            loc_name = self._get_loc_en_name(loc=forecast["location"])
            cv2.imwrite(f'{loc_name} {forecast["forecast_date"]}.jpg', finished_image)

    def _get_themes(self, forecast):
        """
        Определение темы изображения.

        Было решено отказаться от регулярных выражений,
        т.к. пул описаний погоды на сайте довольно небольшой, так получается чуть быстрее (и реализация проще).
        (см. THEMES_PATTERNS в settings.py)

        :param forecast: dict, словарь отдельного прогноза
        :return: str, тема оформления изображения
        """

        for theme, patterns in self.themes_patterns.items():
            for pattern in patterns:
                if pattern in forecast['description'].lower():
                    return theme

    def _gradient_and_logo(self, theme):
        """
        Отрисовка градиента и лого.

        Двигается вдоль оси x, рисуя линию. Цвет линии постепенно меняется от цвета, определённого темой, до белого
        (см. IMAGE_TEMPLATES['background'][1] в settings.py).
        После чего попиксельно отрисовываетлого на полуившемся фоне.

        :param theme: str, тема оформления изображения
        :return: ndarray, массив изображения
        """

        logo = cv2.imread(self.templates[theme][0], cv2.IMREAD_UNCHANGED)
        res = cv2.imread(self.templates['background'][0])

        b_curr, g_curr, r_curr = self.templates[theme][1]
        b_end, g_end, r_end = self.templates['background'][1]
        modif = 0.75

        for x in range(res.shape[1], -1, -1):
            cv2.line(res, (x, 0), (x, res.shape[0]), (b_curr, g_curr, r_curr), 1)
            b_curr += (b_end - b_curr) / res.shape[1] * modif
            g_curr += (g_end - g_curr) / res.shape[1] * modif
            r_curr += (r_end - r_curr) / res.shape[1] * modif

        for y, x_line in enumerate(logo):
            for x, color in enumerate(x_line):
                dx = res.shape[1] - logo.shape[1] + x - round(res.shape[1] * .05)
                dy = y + round(res.shape[0] * .1)
                if color[3] != 0:
                    res[dy][dx] = color[:3]
        return res

    def _print_text(self, forecast, src):
        """
        Печать текста на изображении.

        :param forecast: dict, словарь отдельного прогноза
        :param src: ndarray, массив изображения
        :return: ndarray, массив готового изображения
        """

        res = src
        forecast['forecast_date'] = datetime.date.strftime(forecast['forecast_date'], '%d.%m.%Y')
        x = round(src.shape[1] * .05)
        y = round(src.shape[0] * .1)
        step = round(src.shape[0] * .8) // 8
        for k, v in forecast.items():
            cv2.putText(src, v, (x, y), cv2.FONT_HERSHEY_COMPLEX, .45, (0, 0, 0))
            y += step
        return res

    def _get_loc_en_name(self, loc):
        """
        Получение транслита названия населённого пункта
        для формирования имени сохраняемого файла.

        :param loc: str, название населённого пункта на русском языке
        :return: str, название населённого пункта  транслитом
        """

        res = ''
        for symb in loc.upper():
            if symb not in 'ЁЪЬ':
                if symb in '-,. ':
                    res += symb
                else:
                    res += settings.LETTERS_IN_TRANSCRIPTION[symb]
        return res


if __name__ == '__main__':
    forecast = [{
        'location': 'Москва',
        'forecast_date': datetime.datetime(year=2021, month=9, day=22),
        'temperature': 'Температура: +9 град. С',
        'description': 'дожд',
        'pressure': 'Давление: 744 мм рт.ст.',
        'humidity': 'Влажность: 90 %',
        'wind': 'Ветер: 2 м/c',
        'precipitation': 'Вероятность осадков: 100 %'
    }]
    image_maker = ImageMaker(forecasts=forecast)
    image_maker.draw()
