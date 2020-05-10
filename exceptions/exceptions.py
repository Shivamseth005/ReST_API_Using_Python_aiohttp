""" exceptions """


class ServerException(Exception):
    """Root exception."""


# API
class APIError(ServerException, RuntimeError):
    """API errors."""


class APIForbidden(APIError):
    """API forbidden error."""
