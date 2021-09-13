import unittest

from handlers import *


class HandlersTest(unittest.TestCase):

    def setUp(self):
        self.context = {}

    def test_city_handler_normal(self):
        city_from = 'калининграде'
        step = '1'
        result = city_handler(text=city_from, context=self.context, step=step)
        self.assertEqual(result, True)
        self.assertEqual(self.context['departure_city'], 'калининград')
        city_to = 'владивосток'
        step = '2'
        result = city_handler(text=city_to, context=self.context, step=step)
        self.assertEqual(result, True)
        self.assertEqual(self.context['arrival_city'], 'владивосток')

    def test_city_handler_failure(self):
        city_from = 'Калининград'
        step = '1'
        result = city_handler(text=city_from, context=self.context, step=step)
        self.assertEqual(result, False)
        self.assertEqual(len(self.context), 0)
        self.context['departure_city'] = 'калининград'
        city_to = 'токио'
        step = '2'
        result = city_handler(text=city_to, context=self.context, step=step)
        self.assertEqual(result, False)
        self.assertEqual(len(self.context), 1)

    def test_date_handler_normal(self):
        date = '01-01-2022'
        result = date_handler(text=date, context=self.context)
        self.assertEqual(result, True)
        self.assertEqual(self.context['date'], date)

    def test_date_handler_failure(self):
        date = '01.01.22'
        result = date_handler(text=date, context=self.context)
        self.assertEqual(result, False)
        self.assertEqual(len(self.context), 0)

    def test_flight_handler_normal(self):
        self.context['departure_city'] = 'калининград'
        self.context['arrival_city'] = 'лондон'
        settings.FLIGHTS['калининград']['лондон'] = [0, 1, 2, 3]
        flight = '2'
        result = flight_handler(text=flight, context=self.context)
        self.assertEqual(result, True)
        self.assertEqual(self.context['flight'], 1)

    def test_flight_handler_failure(self):
        self.context['departure_city'] = 'калининград'
        self.context['arrival_city'] = 'лондон'
        settings.FLIGHTS['калининград']['лондон'] = [0, 1, 2, 3]
        flight = 'A'
        result = flight_handler(text=flight, context=self.context)
        self.assertEqual(result, False)
        self.assertEqual(len(self.context), 2)
        flight = '5'
        result = flight_handler(text=flight, context=self.context)
        self.assertEqual(result, False)
        self.assertEqual(len(self.context), 2)

    def test_number_of_seats_handler_normal(self):
        seats = '2'
        result = number_of_seats_handler(text=seats, context=self.context)
        self.assertEqual(result, True)
        self.assertEqual(self.context['number_of_seats'], 2)

    def test_number_of_seats_handler_failure(self):
        seats = 'A'
        result = number_of_seats_handler(text=seats, context=self.context)
        self.assertEqual(result, False)
        self.assertEqual(len(self.context), 0)
        seats = '7'
        result = number_of_seats_handler(text=seats, context=self.context)
        self.assertEqual(result, False)
        self.assertEqual(len(self.context), 0)

    def test_data_checking_handler_normal(self):
        answer = 'да'
        result = data_checking_handler(text=answer, context=self.context)
        self.assertEqual(result, True)

    def test_data_checking_handler_failure(self):
        answer = 'нет'
        result = data_checking_handler(text=answer, context=self.context)
        self.assertEqual(result, False)

    def test_phone_number_handler_normal(self):
        phone = '+79991002030'
        result = phone_number_handler(text=phone, context=self.context)
        self.assertEqual(result, True)
        self.assertEqual(self.context['phone_number'], phone)

    def test_phone_number_handler_failure(self):
        phone = '+7999'
        result = phone_number_handler(text=phone, context=self.context)
        self.assertEqual(result, False)
        self.assertEqual(len(self.context), 0)


if __name__ == '__main__':
    unittest.main()
