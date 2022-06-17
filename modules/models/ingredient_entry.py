# coding: utf-8
from __future__ import print_function

from data.measurements import measurements
from modules.handlers import string_handler_unicode_to_byte


class IngredientEntry(object):
    def __init__(self,
                 ingredient_entry=None,
                 ingredient=None,
                 qty=None,
                 unit=None,
                 ):
        # type: (str, str, float, str) -> None
        self.ingredient_raw = ingredient_entry
        self._ingredient = None if ingredient is None else ingredient
        self._quantity = None if qty is None else qty
        self._unit_of_measurement = None if unit is None else unit
        if self.ingredient_raw is not None and self._ingredient is None:
            self._set_values()
        # self.allergen = self._set_allergen() # TODO: should be implemented here, too

    def _set_values(self):
        splits = self.ingredient_raw.split(" - ", 1)
        self._ingredient = string_handler_unicode_to_byte(splits[0]) if splits[0] else None
        if len(splits) > 1:
            qty_raw = " ".join(s for s in splits[1:]).split()
            if qty_raw:
                try:
                    if qty_raw[0].isdigit():
                        self._quantity = abs(
                            int(qty_raw[0]) if "/" not in qty_raw[0] else float(
                                float(qty_raw[0][0]) / float(qty_raw[0][-1])))
                    else:
                        self._quantity = 0
                    ts = string_handler_unicode_to_byte(
                        " ".join([s for s in qty_raw[1:] if not s.isdigit() and s != "-"]))
                    self._unit_of_measurement = self._check_measurement(ts)
                except UnicodeEncodeError:
                    from warnings import warn
                    warn("Ingredient values not parsed correctly!")
        else:
            self._quantity = 0
            self._unit_of_measurement = string_handler_unicode_to_byte("на око/на вкус")

    @staticmethod
    def _check_measurement(literal):
        rv = "<" + literal + ">"
        for k, v in measurements.items():
            for o in v:
                if string_handler_unicode_to_byte(o) == literal:
                    rv = k
                    return string_handler_unicode_to_byte(rv)
        return rv

    def __repr__(self):
        return "{}: {} {}".format(
            string_handler_unicode_to_byte(self._ingredient),
            self._quantity,
            string_handler_unicode_to_byte(self._unit_of_measurement))

    def __lt__(self, other):
        if isinstance(other, IngredientEntry):
            return self._quantity < other.quantity \
                   and self._ingredient == other.ingredient \
                   and self._unit_of_measurement == other.unit
        else:
            return False

    def __eq__(self, other):
        if isinstance(other, IngredientEntry):
            return self._quantity == other.quantity \
                   and self._ingredient == other.ingredient \
                   and self._unit_of_measurement == other.unit
        else:
            return False

    def __add__(self, other):
        if isinstance(other, IngredientEntry):
            print(self, other)
            if self._unit_of_measurement == other.unit \
                    and self._ingredient == other.ingredient:
                rv = IngredientEntry(ingredient=self._ingredient,
                                     qty=self._quantity + other.quantity,
                                     unit=self._unit_of_measurement)
                return rv
            else:
                raise AttributeError("Ingredient cannot be added together")
        else:
            raise TypeError("Ingredient cannot be added with unsupported object")

    def __sub__(self, other):
        if isinstance(other, IngredientEntry):
            if self._unit_of_measurement == other.unit \
                    and self._ingredient == other.ingredient \
                    and self > other:
                rv = IngredientEntry(ingredient=self._ingredient,
                                     qty=self._quantity - other.quantity,
                                     unit=self._unit_of_measurement)
                return rv
            else:
                raise AttributeError("Result cannot be negative value")
        else:
            raise TypeError("Ingredient cannot be subtracted by unsupported object")

    @property
    def quantity(self):
        return self._quantity

    @property
    def ingredient(self):
        return self._ingredient

    @property
    def unit(self):
        return string_handler_unicode_to_byte(self._unit_of_measurement)
