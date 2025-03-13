class NoLoginError(Exception):
    """未登录，但是调用登录后才能用的接口"""

    def __repr__(self):
        return "<未登录>"


class LoginReadyError(Exception):
    """已登录，但是调用登录前才能用的接口"""

    def __repr__(self):
        return "<已登录>"
