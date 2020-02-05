import functools
import time
from datetime import datetime

from flask import Blueprint, request
from marshmallow import ValidationError

from cloudm.api.api_response import ApiResponse
from cloudm.api.serializers import MachineSerializer, ValidateAddMachineSerializer
from cloudm.domains.cloud_manager.repositories import MachineRepository
from cloudm.services.cloud_manager import CloudManagerService

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")


def schema_validator(schema, many=False):

    def schema_validator_inner(func):
        def wrapper(*args, **kwargs):
            data = getattr(request, "json")
            try:
                parsed_request = schema().load(data=data, many=many)
            except ValidationError:
                raise

            return func(*args, **kwargs, parsed_request=parsed_request)

        return functools.update_wrapper(wrapper, func)

    return schema_validator_inner

@blueprint.route("/ping", methods=["GET"])
def ping():

    response = {
        "msg": "pong",
        "system timestamp": time.time(),
        "system datetime": datetime.now()
    }

    return ApiResponse.build(status_code=200, data=response)



@blueprint.route("/machines", methods=["GET"])
def get_all_machines():

    machines = MachineRepository.get_all_machines()
    machine_list = CloudManagerService.create_machine_list_for_response(machines)
    response_schema = MachineSerializer(many=True)
    response_data = response_schema.dump(machine_list)
    return ApiResponse.build(status_code=200, data=response_data)


@blueprint.route("/machines", methods=["POST"])
@schema_validator(ValidateAddMachineSerializer)
def add_machine(parsed_request):

    CloudManagerService
    return ApiResponse.build(status_code=200, data=parsed_request)






