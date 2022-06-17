# coding: utf-8
from data.allergens import allergens
from modules.handlers import string_handler_unicode_to_byte
from modules.models.chef import Chef
from modules.models.recipe_ingredients import Ingredients


class Recipe(object):
    __slots__ = "_title", "_chef", "_raw_products", "_times_cooked", \
                "_rating", "__products", "__allergens", \
                "_unique_products", "ingredients"

    def __init__(
            self,
            title,
            times_cooked,
            rating,
            chef=None,
            ingredients=None,):
        self._title = string_handler_unicode_to_byte(title)
        self._chef = self._set_chef(chef)
        self.ingredients = self._set_ingredients(ingredients)
        self._times_cooked = int(times_cooked)
        self._rating = float(rating)
        self.__allergens = set()
        self._set_allergens()

    @property
    def title(self):
        return self._title

    @property
    def rating(self):
        return self._rating

    @property
    def times_cooked(self):
        return self._times_cooked

    @property
    def chef(self):
        return self._chef

    @property
    def allergens_as_string(self):
        rv = ", ".join(self.__allergens) if self.__allergens else "No allergens found!"
        return rv

    @property
    def allergens(self):
        return self.__allergens

    def __lt__(self, other):
        return self.unique_products < other.unique_products

    def __repr__(self):
        rv = string_handler_unicode_to_byte(self.title)
        return "Recipe: {}".format(rv)

    def __eq__(self, other):
        return self.title == other

    def _set_allergens(self):
        # TODO: rewrite using IngredientEntry objs
        for product, _ in self.ingredients:
            for al in allergens.keys():
                try:
                    comp = product.lower().decode("utf-8")
                except NameError:
                    comp = product.lower()
                if comp in allergens[al]:
                    self.__allergens.add(al)

    @staticmethod
    def _set_chef(chef):
        if isinstance(chef, Chef):
            return chef
        else:
            anon_chef = Chef(
                name="Anonymous",
                hats=0,
                hearts=0,
                plates=0
            )
            return anon_chef

    @staticmethod
    def _set_ingredients(ingredients):
        if isinstance(ingredients, Ingredients):
            return ingredients
        else:
            null_ingredients = Ingredients()
            return null_ingredients

    def has_allergen(self, inquiry):
        return inquiry in self.allergens
