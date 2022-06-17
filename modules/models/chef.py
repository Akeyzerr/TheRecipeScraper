# -*- coding: utf-8 -*-
from modules.handlers import string_handler_unicode_to_byte


class Chef:
    def __init__(self, name, hats, hearts, plates):
        self.name = name
        self.hats = self._calc_thousands(literal=hats)
        self.hearts = self._calc_thousands(literal=hearts)
        self.plates = self._calc_thousands(literal=plates)
        self.popularity = self._calculate_popularity()

    @staticmethod
    def _calc_thousands(literal):
        """
        Parses a string to int and translates 'k'
        in the string to thousands

        :param literal:
        :return: int
        """
        is_thousands = False if u"k" not in literal else True
        rv = int("".join(n for n in literal if n.isdigit()))
        if is_thousands:
            return rv * 1000
        else:
            return rv

    def _calculate_popularity(self):
        """
        Calculates chef's popularity by the
        formula as per assignment.

        :return: int
        """
        rv = (self.hats + self.hearts + self.plates) // 3
        return rv

    def __repr__(self):
        rv = string_handler_unicode_to_byte(self.name)
        return "Chef Name: {}".format(rv)

    def __le__(self, other):
        return self.popularity <= other.popularity

    def __eq__(self, other):
        return self.popularity == other.popularity
