# coding: utf-8
from modules.models.chef import Chef


class ChefBuilder(object):
    def __init__(self, parsed_url_data):
        """
        Accepts parsed recipe page data and returns
        a Chef object via .make_chef() method.
        :param parsed_url_data: RecipeRequestParser
        """
        self._parsed_data = parsed_url_data

    def _get_chef_name(self):
        """
        Extracts chef's name from the parsed data.
        :return: string or None
        """
        try:
            rv = self._parsed_data.find("div", {"class": "aub"}).select_one('a', href=False).text
            return rv
        except ValueError:
            return None

    def _get_chef_hats(self):
        """
        Extracts chef's hats from the parsed data.
        :return: string or None
        """
        try:
            rv = self._parsed_data.find("div", {"class": "aub"}).select_one('span.icb-hat').text
            return rv
        except ValueError:
            return None

    def _get_chef_hearts(self):
        """
        Extracts chef's hearts from the parsed data.
        :return: string or None
        """
        try:
            rv = self._parsed_data.find("div", {"class": "aub"}).select_one('span.icb-hrt').text
            return rv
        except ValueError:
            return None

    def _get_plates(self):
        """
        Extracts chef's plates from the parsed data.
        :return: string or None
        """
        try:
            rv = self._parsed_data.find("div", {"class": "aub"}).select_one('span.icb-plt').text
            return rv
        except ValueError:
            return None

    def make_chef(self):
        """
        Creates a Chef object with a name, hats, hearts, and plates
        :return: Chef
        """
        rv = Chef(
            name=self._get_chef_name(),
            hats=self._get_chef_hats(),
            hearts=self._get_chef_hearts(),
            plates=self._get_plates()
        )
        return rv
