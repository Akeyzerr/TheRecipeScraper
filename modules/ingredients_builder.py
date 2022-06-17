# coding: utf-8
from modules.models.ingredient_entry import IngredientEntry
from modules.models.recipe_ingredients import Ingredients


class IngredientsBuilder(object):
    def __init__(self, parsed_url_data):
        """
        Accepts parsed recipe page data and returns a
        Recipe Ingredients object via the .make_ingredients()
        method.
        :param parsed_url_data: RecipeRequestParser
        """
        self._parsed_data = parsed_url_data

    def make_ingredients(self):
        rv = Ingredients()
        try:  # extracts recipe products
            products_data = self._parsed_data.find(
                "section", {"class": "products new"}
            ).find("ul").findAll("li", href=False)
            for li in products_data:
                valid_li = li if not li.span else None
                if valid_li:
                    ingredient = IngredientEntry(ingredient_entry=valid_li.get_text())
                    rv.append(ingredient)
                else:
                    continue
            return rv
        except AttributeError:
            return rv
