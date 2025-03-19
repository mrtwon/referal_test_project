class AppBaseException(Exception):
    detail: str
    status: int


class TokenNotFoundException(AppBaseException):
    detail = 'token not found'
    status = 403


class TokeNotValidException(AppBaseException):
    detail = 'token not valid'
    status = 403


class ReferalCannotBeAddedException(AppBaseException):
    detail = 'referal code cannot be add'
    status = 403


class UserNotFoundException(AppBaseException):
    detail = 'user not found'
    status = 404


class ForbiddenException(AppBaseException):
    detail = 'access denied'
    status = 403


class NotAuthorization(AppBaseException):
    detail = 'need authorization'
    status = 401


class ActiveRefCodeNotFoundException(AppBaseException):
    detail = 'active ref code not found'
    status = 404


class UserReferenceNotFoundException(AppBaseException):
    detail = 'user reference not found or been delete'
    status = 404


class AlreadyHasActiveCodeException(AppBaseException):
    detail = 'you already has the active ref code'
    status = 403


class AlreadyHasRefCodeException(AppBaseException):
    detail = 'you already has one active ref code'
    status = 403


class LongTimeLifeRefException(AppBaseException):
    detail = 'long time life ref'
    status = 403
