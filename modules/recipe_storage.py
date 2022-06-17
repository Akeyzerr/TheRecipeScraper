# coding: utf-8
from modules.models.recipe import Recipe
from collections import OrderedDict
import pandas as pd


class RecipeStorage(object):
    def __init__(self):
        self.recipe_container = []

    def __len__(self):
        return len(self.recipe_container)

    def __contains__(self, item):
        return item in self.recipe_container

    def __iter__(self):
        self.index = 0
        return self

    def __intercompatible_next__(self):
        if self.index < len(self.recipe_container):
            rv = self.recipe_container[self.index]
            self.index += 1
            return rv
        else:
            raise StopIteration

    def __next__(self):
        return self.__intercompatible_next__()

    def next(self):
        return self.__intercompatible_next__()

    def __str__(self):
        return "Recipe Container"

    def append(self, other):
        if isinstance(other, Recipe):
            self.recipe_container.append(other)

    def sort_by_title(self, reversed_flag=False):
        self.recipe_container = sorted(self.recipe_container,
                                       key=lambda k: k.title,
                                       reverse=reversed_flag)

    def sort_by_unique_ingredients_count(self, reversed_flag=False):
        self.recipe_container = sorted(self.recipe_container,
                                       key=lambda k: k.ingredients.get_unique_count(),
                                       reverse=reversed_flag)

    def sort_by_total_ingredients_count(self, reversed_flag=False):
        self.recipe_container = sorted(self.recipe_container,
                                       key=lambda k: k.ingredients,
                                       reverse=reversed_flag)

    def sort_by_times_cooked(self, reversed_flag=False):
        self.recipe_container = sorted(self.recipe_container,
                                       key=lambda k: k.times_cooked,
                                       reverse=reversed_flag)

    def sort_by_recipe_rating(self, reversed_flag=False):
        self.recipe_container = sorted(self.recipe_container,
                                       key=lambda k: k.rating,
                                       reverse=reversed_flag)

    def sort_by_chef_popularity(self, reversed_flag=False):
        self.recipe_container = sorted(self.recipe_container,
                                       key=lambda k: k.chef.popularity,
                                       reverse=reversed_flag)

    def _make_report_odict(self):
        rv = OrderedDict({
            "recipe_title": [],
            "recipe_rating": [],
            "recipe_times_cooked": [],
            "chef_name": [],
            "chef_popularity": [],
            "recipe_unique_products": [],
            "recipe_allergens": [],
            "recipe_products": [],
        })
        for r in self.recipe_container:
            rv["recipe_title"].append(r.title)
            rv["recipe_rating"].append(r.rating)
            rv["recipe_times_cooked"].append(r.times_cooked)
            rv["recipe_products"].append([p for _, p in r.ingredients])
            rv["recipe_unique_products"].append(r.ingredients.get_unique_count())
            rv["recipe_allergens"].append(r.allergens)
            rv["chef_name"].append(r.chef.name)
            rv["chef_popularity"].append(r.chef.popularity)
        return rv

    @property
    def get_csv(self):
        rv = self.get_dataframe().to_csv(encoding="utf-8")
        return rv

    def export_json(self):
        self.get_dataframe().to_json(
            "inquiry_report.json",
            orient="index", force_ascii=False)

    def get_dataframe(self):
        rv = pd.DataFrame(self._make_report_odict(), columns=[
            "recipe_title",
            "recipe_rating",
            "recipe_times_cooked",
            "recipe_products",
            "recipe_unique_products",
            "recipe_allergens",
            "chef_name",
            "chef_popularity",
        ])
        return rv

