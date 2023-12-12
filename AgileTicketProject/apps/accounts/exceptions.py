class GeneralException(Exception):
    pass


class BadRequest(GeneralException):
    pass


class InvalidPassword(GeneralException):
    def __init__(self):
        super().__init__("invalid password")


class NotFound(Exception):
    pass


class UserNotFound(NotFound):
    def __init__(self):
        super().__init__(f'User does not exist.')


class LoginFailed(NotFound):
    def __init__(self):
        super().__init__(f"No user with these credentials found.")


class RoleNotFound(NotFound):
    def __init__(self):
        super().__init__(f'Role does not exist.')


class OrganizationNotFound(NotFound):
    def __init__(self):
        super().__init__(f'Organization does not exist.')
