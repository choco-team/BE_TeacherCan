from rest_framework.status import is_success
import json
from ninja.renderers import JSONRenderer


class DefaultRenderer(JSONRenderer):
    def render(self, request, data, *, response_status):
        success = is_success(response_status)
        res = {
            "success": success,
            "code": 2000 if success else data['code'],
            "message": None,
            "data": None
        }
        if success:
            if type(data) == str:
                res["message"] = data
            else:
                res["data"] = data
        else:
            res["message"] = data['message']
            if "data" in data:
                res["data"] = data['data']
        return json.dumps(res, cls=self.encoder_class, **self.json_dumps_params)
