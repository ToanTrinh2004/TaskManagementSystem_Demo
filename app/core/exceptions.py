class NotFoundError(Exception):
    def __init__(self, msg):
        self.msg = msg
class UnauthorizedError(Exception):
    def __init__(self, msg):
        self.msg = msg
class BadRequestError(Exception):
    def __init__(self, msg):
        self.msg = msg