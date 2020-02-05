from flask import jsonify, make_response


class ApiResponse:
    @staticmethod
    def build(status_code, data=None, errors=None, meta=None, resource_version=None):
        if meta is None:
            meta = dict()
        if data is None:
            data = dict()
        if errors is None:
            errors = list()
        response = dict(data=data, errors=errors, meta=meta)
        if resource_version:
            response["resource_version"] = resource_version
        return make_response(jsonify(response), status_code)