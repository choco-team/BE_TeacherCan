import json

from ninja.renderers import JSONRenderer
from rest_framework.status import is_success


class DefaultRenderer(JSONRenderer):
    def render(self, request, *, response_status):
        if "detail" in request:
            print(request)
            res = {
                "success": False,
                "code": 400,
                "message": request['detail'],
                "data": None,
            }
        else:
            success = is_success(response_status)
            res = {
                "success": True if success else False,
                "code": 2000 if success else request['code'],
                "message": request if type(request) == str else (None if success else request['message']),
                "data": request if success and type(request) != str else None,
            }
        return json.dumps(res)
    

    