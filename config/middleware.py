import json


class JsonResponseWrapperMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if (
            response
            and response.has_header("Content-Type")
            and "application/json" in response["Content-Type"]
        ):
            data = json.loads(response.content.decode())
            response.content = json.dumps({"success": True, "data": data})
        return response
