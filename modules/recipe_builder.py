# coding: utf-8
from __future__ import print_function

from modules.handlers import string_handler_unicode_to_byte
from modules.models.recipe import Recipe


class RecipeBuilder(object):
    """
    Builds a Recipe with given Chef from target URL
    """

    def __init__(self, parsed_url_data, chef, ingredients):
        # type: (string, Chef, Ingredients) -> None
        """
        :param parsed_url_data: string:
            This is the data that is returned from the urlparse function
        :param chef: Chef:
            The chef object instance that is used to make the recipe
        """
        self.chef = chef
        self.ingredients = ingredients
        self._parsed_data = parsed_url_data

    def _get_title(self):
        """
        Private parser for the recipe title.
        :return: string: The title of the article.
        """
        try:
            rv = self._parsed_data.find("h1").text.replace("\n", " ")
            return rv
        except AttributeError:
            raise AttributeError

    def _get_rating(self):
        """
        Private parser for the recipe rating.
        :return: string
        """
        try:
            rv = self._parsed_data.find(
                "div", {"class": "lsi"}
            ).find("div").text
            return rv
        except AttributeError:
            rv = "0"
            return rv

    def _get_times_cooked(self):
        """
        Private parser for the recipe times cooked.
        :return: int
        """
        rv = 0
        try:
            find_stats = self._parsed_data.find(
                "div", {"class": "stats soc"}
            ).find("ul").findAll("li", href=False)[-1]
            find_cooked_span = string_handler_unicode_to_byte(find_stats.findAll("span")[-2].get_text())
            is_cooked = find_cooked_span == "Сготвена"
            rv = find_stats.findAll("span")[-1].get_text() if is_cooked else rv
            return rv
        except AttributeError:
            return rv

    def make_recipe(self):
        """
        Instantiation method that creates a new
        recipe object with the parsed date.
          :return: Recipe
        """
        rv = Recipe(
            title=self._get_title(),
            rating=self._get_rating(),
            times_cooked=self._get_times_cooked(),
            chef=self.chef,
            ingredients=self.ingredients,
        )
        return rv
