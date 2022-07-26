from backend import error


class CredentialsInvalid(error.Error):
    pass


class EmailTaken(error.Error):
    pass


class EmailInvalid(error.Error):
    pass


class NotFound(error.Error):
    pass


class Unauthorized(error.Error):
    pass
