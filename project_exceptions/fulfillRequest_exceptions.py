class UnfulfillableInquiry(Exception):
    def __init__(self, err_msg=None, requested=None, found=None):
        self.message = err_msg
        self.requested = requested
        self.found = found
        if self.message is not None:
            super(Exception, self).__init__(self.message)

    def __str__(self):
        return "Not enough recipes with given parameters found:\nRequested count: {}\nFound only: {}".format(
            self.requested, self.found)
