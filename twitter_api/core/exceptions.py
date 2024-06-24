from fastapi import HTTPException, status


class DetailedHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = 'Server error'

    def __init__(self, *args, **kwargs) -> None:
        kwargs.setdefault('status_code', self.STATUS_CODE)
        kwargs.setdefault('detail', self.DETAIL)
        super().__init__(*args, **kwargs)


class PermissionDenied(DetailedHTTPException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = 'Permission denied'


class NotFound(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND


class BadRequest(DetailedHTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = 'Bad Request'


class NotAuthenticated(DetailedHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = 'User not authenticated'

    def __init__(self) -> None:
        super().__init__(headers={'Authenticate': 'Bearer'})
