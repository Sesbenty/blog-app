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
    def __init__(self):
        self.msg = "Incorrect user id"
        super().__init__(self.msg)

    def __str__(self):
        return self.msg


class BlogDidNotExist(ServicesException):
    def __init__(self):
        self.msg = "The blog was deleted or did not exist"
        super().__init__()

    def __str__(self):
        return self.msg


class BlogDidNotPublish(ServicesException):
    def __init__(self):
        self.msg = "The blog did not publish"
        super().__init__()

    def __str__(self):
        return self.msg


class IncorrectCommentId(ServicesException):
    def __init__(self):
        self.msg = "Incorrect comment id"
        super().__init__(self.msg)

    def __str__(self):
        return self.msg


class UserNotOwnerCommentException(ServicesException):
    def __init__(self):
        self.msg = "The user is not the author of the comment"
        super().__init__(self.msg)

    def __str__(self):
        return self.msg
