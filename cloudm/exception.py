from cloudm.api.api_response import ApiResponse


class APIException(Exception):
    error_code = "0001"
    message = "Something went wrong"
    status_code = 500

    def __init__(self, error_code=None, message=None, status_code=None):
        if message is not None:
            self.message = message
        if error_code is not None:
            self.error_code = error_code
        if status_code is not None:
            self.status_code = status_code

    def __str__(self):
        return "exception: error_code={} message={}".format(
            self.error_code, self.message
        )

    def to_dict(self):
        rv = dict()
        rv["error_code"] = self.error_code
        rv["message"] = self.message
        return rv

    @property
    def code(self):
        return "500" + self.error_code


def exception_handler(error):

    if isinstance(error, APIException):
        # status_code = get_http_status_code_from_exception(error)
        status_code = error.status_code
        error = dict(code=error.code, message=error.message)
        return ApiResponse.build(errors=[error], status_code=status_code)

    status_code = 500
    if getattr(error, "status_code", None):
        status_code = error.status_code
    if getattr(error, "code", None):
        status_code = error.code
    response = ApiResponse.build(errors={}, status_code=status_code)
    return response
