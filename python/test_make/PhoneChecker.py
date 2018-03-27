import re


class PhoneChecker:
    def __init__(self, number=''):
        self.number = number

    def check(self):
        if re.match(r'^\d{3}-\d{4}$', self.number):
            print self.number, ' is a valid us local phone number'
        else:
            print self.number, ' rejected'
            raise ValueError('rejected')


# PhoneChecker("123-2445").check()