# coding: utf-8
from __future__ import print_function
from sys import argv

from project_exceptions.argParser_exceptions import *
from modules.settings import ArgParserSettings
from modules.handlers import string_handler_byte_to_unicode


class ArgParser(object):
    _instance = None
    __slots__ = "settings", "mock_args", \
                "__settings", "args", "_count", \
                "_products", "_allergens", "_dish_name"

    def __init__(self, settings=None, mock_args=None):
        """
        Custom parser for sys.argv array.
        Takes optional settings object, which contains the settings for the parsing.
        And optional mock_args list of strings that can be used as mock arguments
        instead of actual command line arguments for testing

        :param settings: ArgParserSettings
        :param mock_args: list
        """
        self.__settings = ArgParserSettings() if settings is None else settings
        self.args = [a for a in argv] if mock_args is None else [a for a in mock_args]
        self._count = self._set_recipes_count
        self._dish_name = self._set_dish_name
        self._products = self._set_products
        self._allergens = self._set_allergens

    def __new__(cls, *args, **kwargs):
        """
        Implementation of the Singleton design pattern.
        :return: ArgParser instance
        """
        if cls._instance is None:
            cls._instance = super(ArgParser, cls).__new__(cls)
            return cls._instance
        else:
            return cls._instance

    @property
    def _set_recipes_count(self):
        """
        Private check method to assert the required argument is present
        in the command line array and the following argument is a number.
        Also, checks if the requested count is within the allowed range.
        If checks fail raises an exceptions.

        :return: int
        """
        try:
            if self.__settings.required_arg_number_of_dishes in self.args:
                result = int(self.args[self.args.index(self.__settings.required_arg_number_of_dishes) + 1])
                return self.__settings.max_request if abs(result) > self.__settings.max_request else abs(result)
            else:
                raise RequiredArgException(
                    req_arg=self.__settings.required_arg_number_of_dishes,
                    message="{} argument is required.".format(
                        self.__settings.required_arg_number_of_dishes
                    ),
                )
        except IndexError:
            raise RequiredArgParamException("No number of dishes provided")

    @property
    def _set_allergens(self):
        """
        Parses command line space or comma separated string of allergens.
        :return: list
        """
        rv = []
        try:
            if self.__settings.opt_arg_allergens in self.args:
                # res_obj holds the string data that has to be
                # handled differently in python 2.7 and 3.x
                res_obj = self.args[self.args.index(self.__settings.opt_arg_allergens) + 1]
                rv = string_handler_byte_to_unicode(res_obj).split()
                return rv
            else:
                return rv
        except IndexError:
            raise RequiredArgParamException()

    @property
    def _set_products(self):
        """
        Parses command line space or comma separated string of products.
        :return: list
        """
        try:
            if self.__settings.opt_arg_products in self.args:
                res_obj = self.args[self.args.index(self.__settings.opt_arg_products) + 1]
                return string_handler_byte_to_unicode(res_obj)
            else:
                return None
        except IndexError:
            err_msg = "List of the products must be provided in quotes or in csv-nospaces format"
            raise RequiredArgParamException(message=err_msg)

    @property
    def _set_dish_name(self):
        """
        Parses command line space or comma separated string for dish name.
        :return: list
        """
        try:
            if self.__settings.opt_dish_name in self.args:
                res_obj = self.args[self.args.index(self.__settings.opt_dish_name) + 1]
                return string_handler_byte_to_unicode(res_obj)
            else:
                return None
        except IndexError:
            err_msg = "Name of the dish must be provided in quotes or in cvs-nospaces format"
            raise RequiredArgParamException(message=err_msg)

    @property
    def is_requested_last_cooked(self):
        """
        Parses command line argument into bool flag.
        :return: bool
        """
        return self.__settings.opt_last_cooked in self.args

    @property
    def count(self):
        """
        Private method returning the value for the requested number of recipes.
        :return: int
        """
        return self._count

    @property
    def dish_name(self):
        """
        Private method returning the value for the requested dish name.
        :return: string
        """
        return self._dish_name

    @property
    def products(self):
        """
        Private method returning the value for the requested products.
        :return: list
        """
        return self._products

    @property
    def allergens(self):
        """
        Private method returning the value for the requested allergens.
        :return: list
        """
        return self._allergens
