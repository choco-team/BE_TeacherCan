import json

from ninja.renderers import JSONRenderer
from rest_framework.status import is_success


class DefaultRenderer(JSONRenderer):
    def render(self, request, *, response_status):
        res = {
            "success": True if is_success(response_status) else False,
            "code": 2000 if is_success(response_status) else request['code'],
            "message": None,
            "data": None
        }
        if is_success(response_status):
            if type(request) == str:
                res.update({"message": request})
            else:
                res.update({"data": request})
        else:
            res.update({"message": request['message']})
        return json.dumps(res)