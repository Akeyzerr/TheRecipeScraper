# coding: utf-8
from time import sleep

import requests
from bs4 import BeautifulSoup
try:
    from urlparse import urljoin  # case py2
except ImportError:
    # noinspection PyUnresolvedReferences
    from urllib.parse import urljoin  # case py3


class RecipeRequestParser(object):
    __slots__ = "_settings", "_parsed_data"

    def __init__(self, target_url, settings):
        # type: (string, GeneralSettings) -> None
        self._settings = settings
        self._parsed_data = self._get_parsed_recipe_data(target_url)

    @property
    def parsed_data(self):
        """
        AP for the parsed data.
        :return: BS4 ResultSet
        """
        return self._parsed_data

    def _get_parsed_recipe_data(self, target):
        """
        Receives a target URL, makes a request to that URL,
        and returns the parsed HTML of the page after
        a preset "long" wait time.

        :param target: string: the url of the recipe
        :return: BeautifulSoup4 ResultSet: The recipe data is being returned.
        """
        try:
            sleep(self._settings.timeout_long)
            rq = requests.get(target, headers=self._settings.headers).text
            rv = BeautifulSoup(rq, "html.parser")
            return rv
        except ValueError:
            # TODO: Raise custom ex
            return None
