class NoLoginError(Exception):
    def __repr__(self):
        return "<未登录>"
