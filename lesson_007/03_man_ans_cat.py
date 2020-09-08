# -*- coding: utf-8 -*-

from random import randint
from termcolor import cprint
# Доработать практическую часть урока lesson_007/python_snippets/08_practice.py

# Необходимо создать класс кота. У кота есть аттрибуты - сытость и дом (в котором он живет).
# Кот живет с человеком в доме.
# Для кота дом характеризируется - миской для еды и грязью.
# Изначально в доме нет еды для кота и нет грязи.

# Доработать класс человека, добавив методы
#   подобрать кота - у кота появляется дом.
#   купить коту еды - кошачья еда в доме увеличивается на 50, деньги уменьшаются на 50.
#   убраться в доме - степень грязи в доме уменьшается на 100, сытость у человека уменьшается на 20.
# Увеличить кол-во зарабатываемых человеком денег до 150 (он выучил пайтон и устроился на хорошую работу :)

# Кот может есть, спать и драть обои - необходимо реализовать соответствующие методы.
# Когда кот спит - сытость уменьшается на 10
# Когда кот ест - сытость увеличивается на 20, кошачья еда в доме уменьшается на 10.
# Когда кот дерет обои - сытость уменьшается на 10, степень грязи в доме увеличивается на 5
# Если степень сытости < 0, кот умирает.
# Так же надо реализовать метод "действуй" для кота, в котором он принимает решение
# что будет делать сегодня

# Человеку и коту надо вместе прожить 365 дней.


class Man:

    def __init__(self, name):
        self.name = name
        self.fullness = 50
        self.house = None

    def __str__(self):
        return f'Сытость {self.name} равна {self.fullness}'

    def eat(self):
        if self.house.food >= 10:
            cprint(f'{self.name} только что поел.', color='yellow')
            self.fullness += 10
            self.house.food -= 10
        else:
            cprint('В доме нет еды.', color='red')

    def work(self):
        cprint(f'{self.name} сходил на работу.', color='blue')
        self.house.money += 150
        self.fullness -= 10

    def watch_tv(self):
        cprint(f'{self.name} смотрел TV целый день.', color='yellow')
        self.fullness -= 10

    def shopping(self):
        if self.house.money >= 50:
            cprint(f'{self.name} сходил в магазин за едой.', color='blue')
            self.house.money -= 50
            self.house.food += 50
        else:
            cprint('Деньги кончились!', color='red')

    def shopping_for_cat(self):
        if self.house.money >= 50:
            cprint(f'{self.name} сходил в зоомагазин за кошачей едой.', color='blue')
            self.house.money -= 50
            self.house.cat_food += 50
        else:
            cprint('Деньги кончились!', color='red')

    def go_to_the_house(self, house):
        self.house = house
        self.fullness -= 10
        cprint(f'{self.name} только что въехал в дом! С новосельем!', color='cyan')

    def clean_house(self):
        self.house.dirt -= 100
        self.fullness -= 20
        cprint(f'{self.name} убрался дома.', color='blue')

    def pet(self, cat, house):
        cat.house = house

    def act(self):
        if self.fullness <= 0:
            cprint(f'{self.name} умер...', color='red')
            return
        dice = randint(1, 6)
        if self.fullness < 30:
            self.eat()
        elif self.house.money < 100:
            self.work()
        elif self.house.food < 20:
            self.shopping()
        elif self.house.cat_food < 20:
            self.shopping_for_cat()
        elif self.house.dirt >= 100:
            self.clean_house()
        elif dice == 1:
            self.work()
        elif dice == 2:
            self.eat()
        else:
            self.watch_tv()


class House:

    def __init__(self):
        self.food = 50
        self.cat_food = 0
        self.dirt = 0
        self.money = 0

    def __str__(self):
        return f'В доме осталось {self.food} еды, {self.money} денег, {self.cat_food} кошачей еды. ' \
               f'Загрязнённость дома {self.dirt}.'


class Cat:

    def __init__(self, name):
        self.name = name
        self.fullness = 50
        self.house = None

    def __str__(self):
        return f'Сытость {self.name} равна {self.fullness}'

    def eat(self):
        if self.house.cat_food >= 10:
            cprint(f'{self.name} только что поел.', color='yellow')
            self.fullness += 20
            self.house.cat_food -= 10
        else:
            cprint('В доме нет кошачей еды.', color='red')

    def destroy(self):
        self.house.dirt += 5
        self.fullness -= 10
        cprint(f'{self.name} коварно дерёт обои!', color='green')

    def sleep(self):
        self.fullness -= 10
        cprint(f'{self.name} сладко спит.', color='yellow')

    def act(self):
        if self.fullness <= 0:
            cprint(f'{self.name} умер...', color='red')
            return
        dice = randint(1, 10)
        if self.fullness < 60:
            self.eat()
        elif dice in [1, 2, 3]:
            self.destroy()
        elif dice == 4:
            self.eat()
        else:
            self.sleep()


my_sweet_home = House()
dude = Man('Dude')
dude.go_to_the_house(my_sweet_home)
cat = Cat('Max')
dude.pet(cat, my_sweet_home)
for day in range(1, 366):
    print(f'================ день {day} ==================')
    dude.act()
    cat.act()
    print('--- в конце дня ---')
    print(dude)
    print(cat)
    print(my_sweet_home)

# Усложненное задание (делать по желанию)
# Создать несколько (2-3) котов и подселить их в дом к человеку.
# Им всем вместе так же надо прожить 365 дней.

# (Можно определить критическое количество котов, которое может прокормить человек...)
