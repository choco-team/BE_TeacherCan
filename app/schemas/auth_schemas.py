from app.routers import common_schemas


class Token(common_schemas.ResponseResult):
    token: str
