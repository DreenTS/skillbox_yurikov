# -*- coding: utf-8 -*-


# Заполнить все поля в билете на самолет.
# Создать функцию, принимающую параметры: ФИО, откуда, куда, дата вылета,
# и заполняющую ими шаблон билета Skillbox Airline.
# Шаблон взять в файле lesson_013/images/ticket_template.png
# Пример заполнения lesson_013/images/ticket_sample.png
# Подходящий шрифт искать на сайте ofont.ru
from PIL import Image, ImageDraw, ImageFont, ImageColor
import argparse as argp


class TicketMaker:

    def __init__(self, template='images/ticket_template.png', font_path='ofont.ru_Schula.ttf'):
        # TODO Имена файлов надо присваивать константам и использовать в основном коде только их.
        #  Имена констант пишутся большими буквами. Располагают константы в начале модуля, сразу после
        #  импортов сторонних модулей.
        self.template = template
        self.font_path = font_path
        self.positions_dict = {  # TODO Есть смыл добавить ключи и для самих текстовых данных, чтобы не делать две
                                 #  структуры данных - одну для координат, другую для текста
            0: {
                'line': [(45, 140), (250, 140)],
                'text': (45, 131)
            },
            1: {
                'line': [(45, 210), (150, 210)],
                'text': (45, 201)
            },
            2: {
                'line': [(45, 275), (150, 275)],
                'text': (45, 266)
            },
            3: {
                'line': [(287, 275), (320, 275)],
                'text': (287, 266)
            },
        }

    def make_ticket(self, fio='Иванов И.И.', from_='ЗЕМЛЯ', to='ЛУНА', date='09.12', save_to=None):
        img = Image.open(self.template)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(self.font_path, size=15)
        list_of_content = [fio, from_, to, date]
        for ind, content in enumerate(list_of_content):
            draw.line(xy=self.positions_dict[ind]['line'], fill=ImageColor.colormap['white'], width=3)
            draw.text(xy=self.positions_dict[ind]['text'], text=content, font=font, fill=ImageColor.colormap['black'])
        if save_to is None:
            img.save(f'{date} {fio}.png')
            print(f'Ticket saved as "{date} {fio}.png"')
        else:
            img.save(f'{save_to}')
            print(f'Ticket saved as "{save_to}"')


def from_parser(maker):

    """
    example for terminal:
        cd C:\...\python_base\lesson_013
        python 01_ticket.py --fio "Иванов И.И." --from Москва --to Саратов --date 01.02 --save_to "01.02 Иванов И.И..png"
    """

    parser = argp.ArgumentParser(description='Ticket Maker')
    parser.add_argument('--fio', action='store', dest='fio')
    parser.add_argument('--from', action='store', dest='from_')
    parser.add_argument('--to', action='store', dest='to')
    parser.add_argument('--date', action='store', dest='date')
    parser.add_argument('--save_to', action='store', dest='save_to')
    args = vars(parser.parse_args())
    maker.make_ticket(fio=args['fio'], from_=args['from_'], to=args['to'], date=args['date'], save_to=args['save_to'])


if __name__ == '__main__':
    maker = TicketMaker()

    # EZ mode

    # maker.make_ticket(fio='Пупкин В.К.', from_='Новосибирск', to='Москва', date='25.11')
    # maker.make_ticket(fio='Зайцева А.А.', from_='Кемерово', to='Екатеринбург', date='27.11')
    # maker.make_ticket(fio='Кничевский Р.Д.', from_='Хабаровск', to='Омск', date='26.11')

    # HARD mode

    from_parser(maker=maker)

# Усложненное задание (делать по желанию).
# Написать консольный скрипт c помощью встроенного python-модуля argparse.
# Скрипт должен принимать параметры:
#   --fio - обязательный, фамилия.
#   --from - обязательный, откуда летим.
#   --to - обязательный, куда летим.
#   --date - обязательный, когда летим.
#   --save_to - необязательный, путь для сохранения заполненнего билета.
# и заполнять билет.
