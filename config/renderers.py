import json

from ninja.renderers import JSONRenderer


class DefaultRenderer(JSONRenderer):
    def render(self, request, data, *, response_status):
        is_success = response_status < 400
        res = {
            "success": is_success,
            "code": 2000 if is_success else data["code"],
        }
        if "message" in data:
            res.update(
                {
                    "message": data["message"],
                    "data": data["data"] if "data" in data else None,
                }
            )
        else:
            res.update({"message": None, "data": data})
        return json.dumps(res, cls=self.encoder_class, **self.json_dumps_params)
