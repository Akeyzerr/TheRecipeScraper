class ArgParserSettings(object):
    _instance = None  # Singleton

    def __init__(self):
        self.required_arg_number_of_dishes = "-n"
        self.opt_arg_allergens = "-a"
        self.opt_arg_products = "-p"
        self.opt_last_cooked = "-l"
        self.opt_dish_name = "-d"
        self.max_request = 100

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ArgParserSettings, cls).__new__(cls, *args, **kwargs)
            return cls._instance


class GeneralSettings:
    def __init__(self, long_time=None, short_time=None, *args, **kwargs):
        self._timeout_long = .5 if long_time is None else long_time
        self._timeout_short = 0.75 if short_time is None else short_time
        self._misc_args = args
        self._misc_kwargs = kwargs
        self._BASE_URL = "https://recepti.gotvach.bg/"
        self._rq_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) "
                                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                                          "Chrome/71.0.3578.98 Safari/537.36",
                            "Accept": "text/html,"
                                      "application/xhtml+xml,"
                                      "application/xml; q = 0.9,"
                                      "image/webp,"
                                      "image/apng,"
                                      "*/*;q = 0.8"}
        self._search_query = "?kw="
        self._space = "%20"

    @property
    def timeout_long(self):
        return self._timeout_long

    @property
    def timeout_short(self):
        return self._timeout_short

    @property
    def misc_args(self):
        return self._misc_args

    @property
    def misc_kwargs(self):
        return self._misc_kwargs

    @property
    def headers(self):
        return self._rq_headers

    @property
    def target_url(self):
        return self._BASE_URL

    @property
    def search_query(self):
        return self._search_query

    @property
    def space(self):
        return self._space
