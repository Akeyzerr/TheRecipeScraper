# coding: utf-8
from __future__ import print_function

from collections import OrderedDict
from modules.argparser import ArgParser
from modules.settings import GeneralSettings


class SetupRequest(object):
    def __init__(self, user_inquiry_args, settings):
        # type: (ArgParser, GeneralSettings) -> None
        self.args = user_inquiry_args
        self._settings = settings

    @property
    def setup_get_recipe_link(self):
        rv = OrderedDict()
        rv["settings"] = self._settings
        if self.args.is_requested_last_cooked:
            rv["last_cooked"] = "cook"
            return rv

        if self.args.dish_name or self.args.products:
            rv["sq"] = self._settings.search_query

        if self.args.dish_name:
            rv["dish_name"] = self._settings.space + self.args.dish_name

        if self.args.products:
            rv["products"] = self._settings.space + self.args.products
        return rv
