from typing import Optional
from fastapi import status


class ArnoldError(Exception):
    def __init__(self, message: str):
        self.message = message


class InsertError(ArnoldError):
    def __init__(
        self,
        message: str,
        code: Optional[int] = status.HTTP_405_METHOD_NOT_ALLOWED,
    ):
        self.message = message
        self.code = code
        super().__init__(message)


class MissingResultsError(ArnoldError):
    def __init__(
        self,
        message: str,
        code: Optional[int] = status.HTTP_404_NOT_FOUND,
    ):
        self.message = message
        self.code = code
        super().__init__(message)
