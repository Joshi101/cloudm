import functools
import time
from datetime import datetime

from flask import Blueprint, request
from marshmallow import ValidationError

from cloudm.api.api_response import ApiResponse
from cloudm.api.serializers import (
    MachineSerializer,
    ValidateAddMachineSerializer,
    ClusterSerializer,
    ValidateAddClusterSerializer,
    ValidateEditMachineSerializer,
)
from cloudm.domains.cloud_manager.operations import CloudManagerOperation
from cloudm.domains.cloud_manager.repositories import (
    MachineRepository,
    ClusterRepository,
)
from cloudm.services.cloud_manager import CloudManagerService
from cloudm.utils import SITE_CONSTANT_SWITCHER

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
        "system datetime": datetime.now(),
    }

    return ApiResponse.build(status_code=200, data=response)


@blueprint.route("/clusters", methods=["GET"])
def get_all_clusters():
    clusters = ClusterRepository.get_all_clusters()
    cluster_list = CloudManagerService().create_cluster_list_for_response(clusters)
    response_schema = ClusterSerializer(many=True)
    response_data = response_schema.dump(cluster_list)
    return ApiResponse.build(status_code=200, data=response_data)


@blueprint.route("/clusters", methods=["POST"])
@schema_validator(ValidateAddClusterSerializer)
def add_cluster(parsed_request):

    created_cluster = CloudManagerService().add_cluster(parsed_request)
    response_schema = ClusterSerializer()
    response_data = response_schema.dump(created_cluster)
    return ApiResponse.build(status_code=200, data=response_data)


@blueprint.route("/machines", methods=["GET"])
def get_all_machines():
    machines = MachineRepository.get_all_machines()
    machine_list = CloudManagerService().create_machine_list_for_response(machines)
    response_schema = MachineSerializer(many=True)
    response_data = response_schema.dump(machine_list)
    return ApiResponse.build(status_code=200, data=response_data)


@blueprint.route("/machines", methods=["POST"])
@schema_validator(ValidateAddMachineSerializer)
def add_machine(parsed_request):
    created_machine = CloudManagerService().add_machine(parsed_request)
    response_schema = MachineSerializer()
    response_data = response_schema.dump(created_machine)
    return ApiResponse.build(status_code=200, data=response_data)


@blueprint.route("/machines/<string:machine_id>", methods=["PATCH"])
@schema_validator(ValidateEditMachineSerializer)
def edit_machine(parsed_request, machine_id):
    machine_obj = CloudManagerOperation().edit_machine(machine_id, parsed_request)
    edited_machine = CloudManagerService.create_machine_dict_for_response(machine_obj)
    response_schema = MachineSerializer()
    response_data = response_schema.dump(edited_machine)
    return ApiResponse.build(status_code=200, data=response_data)


@blueprint.route("/site-constants", methods=["GET"])
def get_constants():
    constant = request.args.get("constant")
    constant_class = SITE_CONSTANT_SWITCHER.get(constant)
    constant_value_list = []
    if constant_class:
        for name, value in constant_class.choices():
            constant_dict = {"code": name, "value": value}
            constant_value_list.append(constant_dict)
    return ApiResponse.build(status_code=200, data=constant_value_list)
