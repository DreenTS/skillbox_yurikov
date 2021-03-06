from random import choice

secret_number = ''


def make_secret_number():
    global secret_number
    secret_number = ''
    temp_list_of_number = [str(number) for number in range(0, 10)]
    for _ in range(3):
        temp_number = choice(temp_list_of_number)
        temp_list_of_number.remove(temp_number)
        secret_number += temp_number
    if '0' in temp_list_of_number:
        temp_list_of_number.remove('0')
    secret_number = choice(temp_list_of_number) + secret_number
    return secret_number


def check_the_number(guess_number):
    bulls_and_cows = {'bulls': 0, 'cows': 0}
    for index, digit in enumerate(guess_number):
        temp_find = secret_number.find(digit)
        if temp_find > -1 and temp_find == index:
            bulls_and_cows['bulls'] += 1
        elif temp_find > -1:
            bulls_and_cows['cows'] += 1
    return bulls_and_cows

