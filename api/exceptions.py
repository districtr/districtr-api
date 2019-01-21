from .result import ApiResult


class ApiException(Exception):
    def __init__(self, message, status=400):
        self.message = message
        self.status = status

    def to_result(self):
        return ApiResult({"message": self.message}, status=self.status)


def not_found(error):
    return ApiException("Not found.", 404).to_result()
