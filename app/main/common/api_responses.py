from typing import Generic, Optional, TypeVar


# Define SuccessResponse and ErrorResponse models using Python Generics
DataT = TypeVar("DataT")


class SuccessResponse(Generic[DataT]):
    success: bool = True
    message: Optional[str]
    data: Optional[DataT]


class ErrorResponse(Generic[DataT]):
    success: bool = False
    message: str
    error_code: Optional[int]
    data: Optional[DataT]
