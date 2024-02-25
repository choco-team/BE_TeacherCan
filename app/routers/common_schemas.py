from typing import Generic, TypeVar

from pydantic import BaseModel, create_model

T = TypeVar("T", bound=BaseModel)

# from functools import lru_cache

# @lru_cache()
# def get_standard_response_model(cls: Type[BaseModel]) -> Type[BaseModel]:
#     assert issubclass(cls, BaseModel)
#     return create_model(
#         f"StandardData[{cls.__name__}]",
#         result=(bool, True),
#         code=(int, 2000),
#         message=(str | None, None),
#         data=(cls | None, None),
#     )


class ResponseModel(Generic[T]):
    def __class_getitem__(cls, item):
        return create_model(
            f"StandardData[{item.__name__}]",
            result=(bool, True),
            code=(int, 2000),
            message=(str | None, None),
            data=(item | None, None),
        )
        # return get_standard_response_model(item)

    # def __new__(cls, data: Union[T, Type[T]]) -> "ResponseModel[T]":
    #     result: bool
    #     code: int
    #     message: str | None
    #     # noinspection PyUnusedLocal
    #     response_data: BaseModel | None
    #     if isinstance(data, BaseModel):
    #         response_type = get_standard_response_model(type(data))
    #         response_data = data
    #     else:
    #         assert issubclass(data, BaseModel)
    #         response_type = get_standard_response_model(data)
    #         response_data = None

    #     # noinspection PyTypeChecker
    #     return response_type(result=result, code=code, message=message, data=response_data)  # type: ignore


class ResponseWrapper(ResponseModel):
    def __init__(self, data):
        self.data = data

class ResponseResult(BaseModel):
    result: bool
    message: str

    def __repr__(self):
        return f"Result(result:{self.result}, message:{self.message})"