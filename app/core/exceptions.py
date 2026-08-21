class NotFoundError(Exception):
    def __init__(self, msg):
        self.msg = msg

class UnauthorizedError(Exception):
    def __init__(self, msg):
        self.msg = msg

class BadRequestError(Exception):
    def __init__(self, msg):
        self.msg = msg

class ConflictError(Exception):
    def __init__(self, msg: str):
        self.msg = msg
        super().__init__(msg)

class ForbiddenError(Exception):
    def __init__(self, msg: str):
        self.msg = msg
        super().__init__(msg)