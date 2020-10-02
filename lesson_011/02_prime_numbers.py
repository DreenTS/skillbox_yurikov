# -*- coding: utf-8 -*-


# Есть функция генерации списка простых чисел

# def get_prime_numbers(n):
#     prime_numbers = []
#     for number in range(2, n + 1):
#         for prime in prime_numbers:
#             if number % prime == 0:
#                 break
#         else:
#             prime_numbers.append(number)
#     return prime_numbers

# Часть 1
# На основе алгоритма get_prime_numbers создать класс итерируемых обьектов,
# который выдает последовательность простых чисел до n
#
# Распечатать все простые числа до 10000 в столбик


# class PrimeNumbers:
#
#     def __init__(self, n):
#         self.number_list = []
#         self.n = n
#         self.curr = 2
#         self.i = 0
#
#     def __iter__(self):
#         self.i = 0
#         return self
#
#     def __next__(self):
#         self.i += 1
#         self.number_list.append(self.get_prime_numbers())
#         return self.number_list[self.i - 1]
#
#     def get_prime_numbers(self):
#         for number in range(self.curr, self.n + 1):
#             for prime in self.number_list:
#                 if number % prime == 0:
#                     break
#             else:
#                 self.curr = number + 1
#                 return number
#         else:
#             self.i = 0
#             self.number_list.clear()
#             self.curr = 2
#             raise StopIteration
#
#
# prime_number_iterator = PrimeNumbers(n=10000)
# for number in prime_number_iterator:
#     print(number)


# Часть 2
# Теперь нужно создать генератор, который выдает последовательность простых чисел до n
# Распечатать все простые числа до 10000 в столбик


def prime_numbers_generator(n):
    prime_numbers = []
    for numb in range(2, n + 1):
        for prime in prime_numbers:
            if numb % prime == 0:
                break
        else:
            """
                Выводим только палиндромные простые числа.
            """
            if is_palindromic_number(numb):
                prime_numbers.append(numb)
                yield numb


def is_lucky_number(n):
    if n < 10:
        return False
    str_n = str(n)
    half = len(str_n) // 2
    return sum([int(i) for i in str_n[:half]]) == sum([int(i) for i in str_n[-half:]])


def is_palindromic_number(n):
    return str(n) == str(n)[::-1]


def is_hilbert_number(n):
    """
        число Гильберта
        n = 4 * i + 1
        где i - натуральное число
    """
    return (n - 1) % 4 == 0


print('Палиндромные числа:')
for number in prime_numbers_generator(n=10000):
    print(number)
print(f'Счастливое число 17562: {is_lucky_number(17562)}')
print(f'Палиндромное число 1223221: {is_palindromic_number(1223221)}')
print(f'Число Гильберта 9: {is_hilbert_number(9)}')

# Часть 3
# Написать несколько функций-фильтров, которые выдает True, если число:
# 1) "счастливое" в обыденном пониманиии - сумма первых цифр равна сумме последних
#       Если число имеет нечетное число цифр (например 727 или 92083),
#       то для вычисления "счастливости" брать равное количество цифр с начала и конца:
#           727 -> 7(2)7 -> 7 == 7 -> True
#           92083 -> 92(0)83 -> 9+2 == 8+3 -> True
# 2) "палиндромное" - одинаково читающееся в обоих направлениях. Например 723327 и 101
# 3) придумать свою (https://clck.ru/GB5Fc в помощь)
#
# Подумать, как можно применить функции-фильтры к полученной последовательности простых чисел
# для получения, к примеру: простых счастливых чисел, простых палиндромных чисел,
# простых счастливых палиндромных чисел и так далее. Придумать не менее 2х способов.
#
# Подсказка: возможно, нужно будет добавить параметр в итератор/генератор.


# зачет! 