class BaseAppException(Exception):
    def __init__(self, message: str):
        self.message = message
    code = 500


class NotFound(BaseAppException):
    code = 404


class BadRequest(BaseAppException):
    code = 400


class ValidationError(BaseAppException):
    code = 200


class UserNotFound(BaseAppException):
    code = 401


class InvalidPassword(BaseAppException):
    code = 401


class TokenExpired(BaseAppException):
    code = 401


class AccessDenied(BaseAppException):
    code = 401
