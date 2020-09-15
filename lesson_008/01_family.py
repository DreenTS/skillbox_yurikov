# -*- coding: utf-8 -*-

from termcolor import cprint
from random import randint


######################################################## Часть первая
#
# Создать модель жизни небольшой семьи.
#
# Каждый день участники жизни могут делать только одно действие.
# Все вместе они должны прожить год и не умереть.
#
# Муж может:
#   есть,
#   играть в WoT,
#   ходить на работу,
# Жена может:
#   есть,
#   покупать продукты,
#   покупать шубу,
#   убираться в доме,

# Все они живут в одном доме, дом характеризуется:
#   кол-во денег в тумбочке (в начале - 100)
#   кол-во еды в холодильнике (в начале - 50)
#   кол-во грязи (в начале - 0)
#
# У людей есть имя, степень сытости (в начале - 30) и степень счастья (в начале - 100).
#
# Любое действие, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Кушают взрослые максимум по 30 единиц еды, степень сытости растет на 1 пункт за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе чел умрет от голода.
#
# Деньги в тумбочку добавляет муж, после работы - 150 единиц за раз.
# Еда стоит 10 денег 10 единиц еды. Шуба стоит 350 единиц.
#
# Грязь добавляется каждый день по 5 пунктов, за одну уборку жена может убирать до 100 единиц грязи.
# Если в доме грязи больше 90 - у людей падает степень счастья каждый день на 10 пунктов,
# Степень счастья растет: у мужа от игры в WoT (на 20), у жены от покупки шубы (на 60, но шуба дорогая)
# Степень счастья не должна падать ниже 10, иначе чел умирает от депрессии.
#
# Подвести итоги жизни за год: сколько было заработано денег, сколько сьедено еды, сколько куплено шуб.


class House:
    total_money_earned = 0
    total_food_eaten = 0
    total_fur_coat_purchased = 0

    def __init__(self):
        self.money = 100
        self.food = 50
        self.dirt = 0
        self.cat_food = 30

    def __str__(self):
        return f'Состояние дома: {self.money} денег, {self.food} еды, {self.cat_food} кошачей еды, {self.dirt} грязи.'


class Man:

    def __init__(self, name, house):
        self.name = name
        self.fullness = 30
        self.happiness = 100
        self.house = house

    def __str__(self):
        return f'Состояние {self.name}: {self.fullness} сытости, {self.happiness} счастья.'

    def eat(self):
        if self.house.food < 30:
            cprint('В доме закончилась еда!', color='red')
            return True
        else:
            self.house.food -= 30
            self.fullness += 30
            cprint(f'{self.name} только что поел(-ла).', color='cyan')
            self.house.total_food_eaten += 30
            return False

    def act(self):
        self.house.dirt += 5
        if self.house.dirt > 90:
            self.happiness -= 10
        if self.fullness <= 0 or self.happiness < 10:
            cprint(f'{self.name} умер :(', color='red')
            return False
        elif self.fullness <= 50:
            cprint(f'{self.name} голоден.', color='yellow')
            return self.eat()
        return True

    def play_with_cat(self):
        cprint(f'{self.name} гладит котика. Весь день.', color='cyan')
        self.fullness -= 10
        if self.happiness <= 90:
            self.happiness += 5


class Husband(Man):

    def act(self):
        if super().act():
            dice = randint(1, 8)
            if self.house.money < 140:
                cprint('В доме осталось не так много денег...', color='red')
                self.work()
            elif dice in range(1, 3):
                cprint(f'{self.name} хочет поиграть в танчики.', color='yellow')
                self.gaming()
            elif dice in range(3, 8):
                cprint(f'{self.name}, можно и на работу сходить.', color='yellow')
                self.work()
            else:
                cprint(f'{self.name} хочет погладить котика.', color='yellow')
                self.play_with_cat()

    def work(self):
        cprint(f'{self.name} сходил на работу и принёс денег в дом.', color='cyan')
        self.house.money += 150
        self.fullness -= 10
        self.house.total_money_earned += 150

    def gaming(self):
        cprint(f'{self.name} весь день играет в WoT. И хорошо ему.', color='cyan')
        self.fullness -= 10
        if self.happiness <= 80:
            self.happiness += 20


class Wife(Man):

    def act(self):
        if super().act():
            dice = randint(1, 10)
            if self.house.food < 70:
                cprint('В доме почти не осталось еды...', color='yellow')
                self.shopping()
            elif self.house.dirt > 80 or dice in range(1, 5):
                cprint(f'{self.name} решила прибраться.', color='yellow')
                self.clean_house()
            elif dice in range(5, 8):
                cprint(f'{self.name} захотела шубу.', color='yellow')
                self.buy_fur_coat()
            elif dice in range(8, 10):
                cprint(f'{self.name} решила прикупить чего-нибудь вкусного.', color='yellow')
                self.shopping()
            else:
                cprint(f'{self.name} хочет погладить котика.', color='yellow')
                self.play_with_cat()

    def shopping(self):
        if self.house.money >= 100:
            cprint(f'{self.name} купила домой покушать. И коту тоже.', color='cyan')
            self.house.money -= 84
            self.house.food += 70
            self.house.cat_food += 14
            self.fullness -= 10
        else:
            cprint('В доме осталось не так много денег...', color='red')

    def buy_fur_coat(self):
        if self.house.money >= 350:
            cprint(f'{self.name} купила шубу.', color='cyan')
            if self.happiness <= 70:
                self.happiness += 60
            self.house.money -= 350
            self.fullness -= 10
            self.house.total_fur_coat_purchased += 1
        else:
            cprint('В доме осталось не так много денег...', color='red')

    def clean_house(self):
        if self.house.dirt >= 45:
            cprint(f'{self.name} убралась дома.', color='cyan')
            self.fullness -= 10
            self.house.dirt -= 35
        else:
            cprint('В доме не так уж и много грязи, жить можно :)', color='cyan')


class Cat:

    def __init__(self, name, house):
        self.name = name
        self.fullness = 30
        self.house = house

    def __str__(self):
        return f'Состояние {self.name}: {self.fullness} сытости, 100 кошачности.'

    def act(self):
        dice = randint(1, 10)
        if self.fullness <= 0:
            cprint(f'{self.name} умер :( Бедный котик...', color='red')
        elif self.fullness <= 60:
            cprint(f'{self.name} очень голоден.', color='yellow')
            self.eat()
        elif dice in range(1, 6):
            cprint(f'{self.name} хочет спать весь день.', color='yellow')
            self.sleep()
        elif dice in range(6, 9):
            cprint(f'{self.name} проголодался.', color='yellow')
            self.eat()
        else:
            cprint(f'{self.name} решил похулиганить.', color='yellow')
            self.soil()

    def eat(self):
        if self.house.cat_food < 10:
            cprint('В доме закончилась еда для кота!', color='red')
        else:
            self.house.cat_food -= 6
            self.fullness += 12
            cprint(f'{self.name} только что поел как кот.', color='cyan')

    def sleep(self):
        cprint(f'{self.name} сладко спит.', color='cyan')
        self.fullness -= 10

    def soil(self):
        cprint(f'{self.name} коварно портит обои. Вот зачем?...', color='cyan')
        self.fullness -= 10
        self.house.dirt += 5


home = House()
dad = Husband(name='Василий', house=home)
mom = Wife(name='Мария', house=home)
cat = Cat(name='Борис', house=home)


for day in range(365):
    cprint(f'================== День {day + 1} ==================', color='green')
    dad.act()
    mom.act()
    cat.act()
    cprint('В конце дня:', color='magenta')
    cprint(dad, color='blue')
    cprint(mom, color='blue')
    cprint(cat, color='blue')
    cprint(home, color='blue')
cprint(f'\nОбщая сводка за год.', color='green')
cprint(f'Заработано денег: {home.total_money_earned}.\nСъедено еды: {home.total_food_eaten}.\n'
       f'Куплено шуб: {home.total_fur_coat_purchased}.', color='blue')


######################################################## Часть вторая
#
# После подтверждения учителем первой части надо
# отщепить ветку develop и в ней начать добавлять котов в модель семьи
#
# Кот может:
#   есть,
#   спать,
#   драть обои
#
# Люди могут:
#   гладить кота (растет степень счастья на 5 пунктов)
#
# В доме добавляется:
#   еда для кота (в начале - 30)
#
# У кота есть имя и степень сытости (в начале - 30)
# Любое действие кота, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Еда для кота покупается за деньги: за 10 денег 10 еды.
# Кушает кот максимум по 10 единиц еды, степень сытости растет на 2 пункта за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе кот умрет от голода.
#
# Если кот дерет обои, то грязи становится больше на 5 пунктов


######################################################## Часть вторая бис
#
# После реализации первой части надо в ветке мастер продолжить работу над семьей - добавить ребенка
#
# Ребенок может:
#   есть,
#   спать,
#
# отличия от взрослых - кушает максимум 10 единиц еды,
# степень счастья  - не меняется, всегда ==100 ;)

class Child:

    def __init__(self):
        pass

    def __str__(self):
        return super().__str__()

    def act(self):
        pass

    def eat(self):
        pass

    def sleep(self):
        pass


######################################################## Часть третья
#
# после подтверждения учителем второй части (обоих веток)
# влить в мастер все коммиты из ветки develop и разрешить все конфликты
# отправить на проверку учителем.


# Усложненное задание (делать по желанию)
#
# Сделать из семьи любителей котов - пусть котов будет 3, или даже 5-10.
# Коты должны выжить вместе с семьей!
#
# Определить максимальное число котов, которое может прокормить эта семья при значениях зарплаты от 50 до 400.
# Для сглаживание случайностей моделирование за год делать 3 раза, если 2 из 3х выжили - считаем что выжили.
#
# Дополнительно вносить некий хаос в жизнь семьи
# - N раз в год вдруг пропадает половина еды из холодильника (коты?)
# - K раз в год пропадает половина денег из тумбочки (муж? жена? коты?!?!)
# Промоделировать - как часто могут случаться фейлы что бы это не повлияло на жизнь героев?
#   (N от 1 до 5, K от 1 до 5 - нужно вычислит максимумы N и K при котором семья гарантированно выживает)
#
# в итоге должен получится приблизительно такой код экспериментов
# for food_incidents in range(6):
#   for money_incidents in range(6):
#       life = Simulation(money_incidents, food_incidents)
#       for salary in range(50, 401, 50):
#           max_cats = life.experiment(salary)
#           print(f'При зарплате {salary} максимально можно прокормить {max_cats} котов')
