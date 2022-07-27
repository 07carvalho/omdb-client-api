from backend.wsgi import ApplicationError


class Error(ApplicationError):
    def __init__(self, message=None):
        super(Error, self).__init__(message, error_name=self.__class__.__name__)


class CredentialsInvalid(Error):
    pass


class EmailTaken(Error):
    pass


class EmailInvalid(Error):
    pass


class NotFound(Error):
    pass


class PaginationFieldMissingOrInvalid(Error):
    pass


class Unauthorized(Error):
    pass
