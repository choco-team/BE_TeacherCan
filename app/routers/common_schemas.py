from typing import Generic, TypeVar

from pydantic import BaseModel, create_model

T = TypeVar("T", bound=BaseModel)

class ResponseModel(Generic[T]):
    def __class_getitem__(cls, item):
        return create_model(
            f"StandardData[{item.__name__}]",
            result=(bool, True),
            code=(int, 2000),
            message=(str | None, None),
            data=(item | None, None),
        )

class ResponseWrapper(ResponseModel):
    def __init__(self, data):
        self.data = data