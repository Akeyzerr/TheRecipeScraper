class RequiredArgException(Exception):
    def __init__(self, req_arg="-n", message=None):
        self.req_arg = req_arg
        self.message = message
        if message is not None:
            super(Exception, self).__init__(self.message)

    def __str__(self):
        return "Required Argument is missing: {}".format(self.req_arg)


class RequiredArgParamException(Exception):
    def __init__(self, message=None):
        self.message = message
        if message is not None:
            super(Exception, self).__init__(self.message)

    def __str__(self):
        return "Required argument got no parameter(required)"
