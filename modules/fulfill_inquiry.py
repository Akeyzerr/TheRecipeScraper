# coding: utf-8
from __future__ import print_function

from modules.argparser import ArgParser
from modules.ingredients_builder import IngredientsBuilder
from modules.settings import GeneralSettings
from modules.setup_request import SetupRequest
from modules.get_recipe_link import GetRecipeLink
from modules.recipe_request_parser import RecipeRequestParser
from modules.chef_builder import ChefBuilder
from modules.recipe_builder import RecipeBuilder
from modules.recipe_storage import RecipeStorage
from project_exceptions.fulfillRequest_exceptions import UnfulfillableInquiry


class FulfillInquiry(object):
    settings = GeneralSettings()

    def __init__(self, mock_argv=None, strict=True):
        """
        The command class object that instantiates ArgParser object, which parses the user inquiry.
        Creates an instance of the SetupRequest the general settings of the program.
        Creates an instance of the GetRecipeLink class, with the parsed arguments and the settings.
        It then creates an instance of the RecipeStorage class.
        It then calls the _produce method and governs the user inquiry fulfillment.
        :param: list
        :param: bool: If True, the program will exit if the recipe is not found, defaults to True
        (optional)
        """
        self.strict = strict
        self._args = ArgParser(mock_args=mock_argv)
        self._setup_links_params = SetupRequest(user_inquiry_args=self._args, settings=self.settings)
        self._links = GetRecipeLink(**self._setup_links_params.setup_get_recipe_link)
        self._storage = RecipeStorage()
        self._produce()

    @property
    def result_storage(self):
        """
        AP for the stored objects of class Recipe.
        :return: list:
        """
        return self._storage

    def _produce(self):
        """
        Master executive producer method. Iterates over a generator of
        links, creates a Recipe object and adds it to the instance's
        storage.
        """
        no_more_recipes = False
        while len(self._storage) < self._args.count:
            for link in self._links:
                if len(self._storage) > self._args.count - 1:
                    break
                parsed_data = RecipeRequestParser(settings=self.settings, target_url=link).parsed_data
                new_chef = ChefBuilder(parsed_url_data=parsed_data).make_chef()
                ingredients = IngredientsBuilder(parsed_url_data=parsed_data).make_ingredients()
                recipe = RecipeBuilder(parsed_url_data=parsed_data,
                                       chef=new_chef,
                                       ingredients=ingredients).make_recipe()
                self._progress_bar(len(self._storage)+1, self._args.count, recipe)
                if recipe not in self._storage:
                    if self._args.allergens:
                        if self._filter_allergens(recipe):
                            self._storage.append(recipe)
                    else:
                        self._storage.append(recipe)
                else:
                    no_more_recipes = True
                    break
            if no_more_recipes:
                count = self._args.count
                found = len(self._storage)
                if self.strict:
                    raise UnfulfillableInquiry(requested=count, found=found)
                else:
                    from warnings import warn
                    warn(
                        "\nNot enough recipes with given arguments found:\nRequested count: {}\nFound only: {}".format(
                            count, found))
                    break

    def _filter_allergens(self, recipe):
        """
        Returns True if the given Recipe has one of
        the allergens from the initial user inquiry.
        :param recipe: Recipe
        :return: bool
        """
        for allergen in self._args.allergens:
            if not recipe.has_allergen(allergen.title()):
                return True
        return False

    @staticmethod
    def _progress_bar(progress, total, msg):
        """
        A tongue-in-cheek command line progress bar giving
        approx. fulfillment info.
        :param progress: int: the current progress
        :param total: int: the total number of items to be processed
        :param msg: string: The message to be displayed
        """
        percent = int((100 * (progress / float(total)))/2)
        bar = "#" * percent + "-" * (50 - percent)
        print("\r[{}] {}%, processing: {}".format(bar, percent*2, msg), end="")
