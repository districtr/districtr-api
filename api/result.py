from flask import Response, json


class ApiResult:
    def __init__(self, value="", status=200, headers=None):
        self.value = value
        self.status = status
        self.headers = headers

    def to_response(self):
        return Response(
            json.dumps(self.value),
            status=self.status,
            mimetype="application/json",
            headers=self.headers,
        )

    def __call__(self):
        return self.to_response()
