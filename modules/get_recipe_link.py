# coding: utf-8
from __future__ import print_function

try:
    from urlparse import urljoin  # case py2
except ImportError:
    # noinspection PyUnresolvedReferences
    from urllib.parse import urljoin  # case py3

import requests
from collections import deque
from bs4 import BeautifulSoup
from time import sleep


class GetRecipeLink(object):
    """
    GetRecipeLink class yields a single recipe link and
    handles pagination with initial url kwargs
    """

    def __init__(self, settings, url=None, **kwargs):
        """
        :param settings: GeneralSettings: a settings object that contains the target url, the user agent, and the proxy
        :param url: string: The URL of the page to be scraped (optional)
        """
        self._init_args = kwargs
        self._settings = settings
        self._url = self._settings.target_url if url is None else url
        self._init_uri = self._construct_rq_uri(url=self.url, **self._init_args)
        self._homepage = self._get_page_data()
        self._homepage_parsed = self._parse_page_data()

    @property
    def url(self):
        """
        The `@property` decorator turns the url() method into a "getter" for a read-only attribute with
        the same name, url

        :return: string
        """
        return self._url

    @staticmethod
    def _construct_rq_uri(url, page="", **kwargs):
        """
        Takes an url, a current page number, and target-specific
        keyword arguments and returns a correct url

        :param url: the base url of the website
        :param page: The page to be requested
        :return: A string.
        """
        rv = "".join([v for v in kwargs.values() if v is not None])
        url = urljoin(url, page + rv)
        return url

    def _get_page_data(self):
        """
        The private function waits for a preset "long"
        time for safety against DDoS protections,
        then it makes a request to the website.
        :return: request
        """
        sleep(self._settings.timeout_long)
        return requests.get(self._init_uri, headers=self._settings.headers, timeout=2)

    def _parse_page_data(self):
        """
        The private function takes the content of the homepage, and parses it using BeautifulSoup
        :return: BeautifulSoup4 ResultSet
        """
        return BeautifulSoup(self._homepage.content, "html.parser")

    def _set_links_deque(self):
        """
        The private function  takes the homepage of the website,
        parses it, finds the links to the next pages, and returns
        them in a deque
        :return: deque: A deque of links to the next page of results.
        """
        rv = deque([link["href"] + "?s=1" for link in self._homepage_parsed
                   .find("div", class_="rprev")
                   .find_all("a", class_="title", href=True)])
        return rv

    def _refill_links_deque(self):
        """
        Takes the next page link from the current page,
        constructs a new request URI, gets the new page
        data, parses the new page data, and sets the new
        links deque
        """
        try:
            page_path = self._homepage_parsed.find("div", class_="pagination") \
                .span.findAllNext("a", class_="next", href=True)[0]["href"]
            self._init_uri = self._construct_rq_uri(url=self.url, page=page_path, **self._init_args)
            self._homepage = self._get_page_data()
            self._homepage_parsed = self._parse_page_data()
            self._links = self._set_links_deque()
        except AttributeError:
            raise StopIteration

    def __iter__(self):
        self._links = self._set_links_deque()
        return self

    def __intercompatible_next__(self):
        """
        If there are no more links in the deque,
        refill it and then pop the first link
        :return: string: url for the next recipe
        """
        try:
            rv = self._links.popleft()
        except IndexError:
            try:
                self._refill_links_deque()
                rv = self._links.popleft()
            except IndexError:
                raise StopIteration
        return rv

    def __next__(self):  # Python3 syntax for generator class
        return self.__intercompatible_next__()

    def next(self):  # Handling generator in Python2.7 syntax
        return self.__intercompatible_next__()
