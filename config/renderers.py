import json

from ninja.renderers import JSONRenderer


class DefaultRenderer(JSONRenderer):
    def render(self, request, data, *, response_status):
        res = {
            "success": response_status < 400,
            "code": response_status,
        }
        if "message" in data:
            res.update(
                {
                    "data": data["data"] if "data" in data else None,
                    "message": data["message"],
                }
            )
        else:
            res.update({"data": data})

        return json.dumps(res, cls=self.encoder_class, **self.json_dumps_params)
