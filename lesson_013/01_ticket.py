# -*- coding: utf-8 -*-


# Заполнить все поля в билете на самолет.
# Создать функцию, принимающую параметры: ФИО, откуда, куда, дата вылета,
# и заполняющую ими шаблон билета Skillbox Airline.
# Шаблон взять в файле lesson_013/images/ticket_template.png
# Пример заполнения lesson_013/images/ticket_sample.png
# Подходящий шрифт искать на сайте ofont.ru
from PIL import Image, ImageDraw, ImageFont, ImageColor
import argparse as argp

TEMPLATE_ORIGIN = 'images/ticket_template.png'
FONT_PATH_ORIGIN = 'ofont.ru_Schula.ttf'


class Ticket:

    def __init__(self, fio, from_, to, date):
        self.data_dict = {
            0: {
                'line': [(45, 140), (250, 140)],
                'text': (45, 131),
                'content': fio
            },
            1: {
                'line': [(45, 210), (150, 210)],
                'text': (45, 201),
                'content': from_
            },
            2: {
                'line': [(45, 275), (150, 275)],
                'text': (45, 266),
                'content': to
            },
            3: {
                'line': [(287, 275), (320, 275)],
                'text': (287, 266),
                'content': date
            },
        }


class TicketMaker:

    def __init__(self, ticket_list, template=TEMPLATE_ORIGIN, font_path=FONT_PATH_ORIGIN, save_to=None):
        self.template = template
        self.font_path = font_path
        self.save_to = save_to
        self.ticket_list = ticket_list

    def make_tickets(self):
        for ticket in self.ticket_list:
            img = Image.open(self.template)
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(self.font_path, size=15)
            for i in range(4):
                draw.line(xy=ticket.data_dict[i]['line'], fill=ImageColor.colormap['white'], width=3)
                draw.text(xy=ticket.data_dict[i]['text'], text=ticket.data_dict[i]['content'], font=font,
                          fill=ImageColor.colormap['black'])
            if self.save_to is None:
                img.save(f'{ticket.data_dict[3]["content"]} {ticket.data_dict[0]["content"]}.png')
                print(f'Ticket saved as "{ticket.data_dict[3]["content"]} {ticket.data_dict[0]["content"]}.png"')
            else:
                img.save(f'{self.save_to}')
                print(f'Ticket saved as "{self.save_to}"')


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
    maker.ticket_list.append(Ticket(args['fio'], args['from_'], args['to'], args['date']))
    maker.save_to = args['save_to']
    maker.make_tickets()


if __name__ == '__main__':
    # EZ mode
    tickets = [Ticket(fio='Пупкин В.К.', from_='Новосибирск', to='Москва', date='25.11'),
               Ticket(fio='Зайцева А.А.', from_='Кемерово', to='Екатеринбург', date='27.11'),
               Ticket(fio='Кничевский Р.Д.', from_='Хабаровск', to='Омск', date='26.11')]
    maker = TicketMaker(ticket_list=tickets)
    maker.make_tickets()

    # HARD mode
    # tickets = []
    # maker = TicketMaker(ticket_list=tickets)
    # from_parser(maker=maker)

# Усложненное задание (делать по желанию).
# Написать консольный скрипт c помощью встроенного python-модуля argparse.
# Скрипт должен принимать параметры:
#   --fio - обязательный, фамилия.
#   --from - обязательный, откуда летим.
#   --to - обязательный, куда летим.
#   --date - обязательный, когда летим.
#   --save_to - необязательный, путь для сохранения заполненнего билета.
# и заполнять билет.

# зачет!
