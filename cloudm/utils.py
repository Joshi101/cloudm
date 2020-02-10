import functools

from flask import request
from marshmallow import ValidationError

from cloudm.domains.cloud_manager.models import (
    RegionChoices,
    MachineStateChoices,
    OperationTypeChoices,
)
from cloudm.exception import APIException

SITE_CONSTANT_SWITCHER = {
    "region": RegionChoices,
    "machine_state": MachineStateChoices,
    "machine_operation": OperationTypeChoices,
}


def schema_validator(schema, many=False):
    def schema_validator_inner(func):
        def wrapper(*args, **kwargs):
            data = getattr(request, "json")
            print(data)
            try:
                parsed_request = schema().load(data=data, many=many)
            except ValidationError as e:
                print(e)
                raise APIException(message=str(e))

            return func(*args, **kwargs, parsed_request=parsed_request)

        return functools.update_wrapper(wrapper, func)

    return schema_validator_inner
