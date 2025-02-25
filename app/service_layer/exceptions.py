class ServicesException(Exception):
    pass


class UserRegisteredException(ServicesException):
    def __init__(self, email: str):
        self.msg = f"User with email address {email} is already registered"
        super().__init__(self.msg)

    def __str__(self):
        return self.msg


class IncorrectLoginOrPasswordException(ServicesException):
    def __init__(self):
        self.msg = "Incorrect login or password"
        super().__init__(self.msg)

    def __str__(self):
        return self.msg


class UserNotOwnerBlogException(ServicesException):
    def __init__(self):
        self.msg = "The user is not the owner of the blog"
        super().__init__(self.msg)

    def __str__(self):
        return self.msg


class IncorrectUserId(ServicesException):
    def __init__(self, *args):
        self.msg = "Incorrect user id"
        super().__init__(self.msg)

    def __str__(self):
        return self.msg
