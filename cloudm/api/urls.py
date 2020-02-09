import time
from datetime import datetime

from flask import Blueprint, request
from cloudm.api.api_response import ApiResponse
from cloudm.api.serializers import (
    MachineSerializer,
    ValidateAddMachineSerializer,
    ClusterSerializer,
    ValidateAddClusterSerializer,
    ValidateEditMachineSerializer,
    ValidateEditClusterSerializer,
)
from cloudm.domains.cloud_manager.operations import CloudManagerOperation
from cloudm.domains.cloud_manager.repositories import (
    MachineRepository,
    ClusterRepository,
)
from cloudm.services.cloud_manager import CloudManagerService
from cloudm.utils import SITE_CONSTANT_SWITCHER, schema_validator

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")


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
    """Get list of all clusters
        ---
        get:
          tags:
            - cluster
          responses:
            200:
              content:
                application/json:
                    schema:
                        type: object
                        properties:
                            data:
                                type: array
                                items:
                                    $ref: "#/components/schemas/ClusterSerializer"
                            meta:
                                type: object
                                additionalProperties: {}
                            errors:
                                type: array
                                items:
                                    type: object
                                    properties:
                                        code:
                                          type: string
                                        developer_message:
                                          type: string
                                        extra_payload:
                                          type: object
                                        message:
                                          type: string
            400:
              description: bad request
          security: []
        """
    clusters = ClusterRepository.get_all_clusters()
    cluster_list = CloudManagerService().create_cluster_list_for_response(clusters)
    response_schema = ClusterSerializer(many=True)
    response_data = response_schema.dump(cluster_list)
    return ApiResponse.build(status_code=200, data=response_data)


@blueprint.route("/clusters", methods=["POST"])
@schema_validator(ValidateAddClusterSerializer)
def add_cluster(parsed_request):
    """Add cluster
    ---
    post:
      tags:
        - cluster
      requestBody:
            content:
              application/json:
                schema:
                    $ref: '#/components/schemas/ValidateAddClusterSerializer'
      responses:
        200:
          content:
            application/json:
                schema:
                    type: object
                    properties:
                        data:
                            type: object
                            $ref: "#/components/schemas/ClusterSerializer"
                        meta:
                            type: object
                            additionalProperties: {}
                        errors:
                            type: array
                            items:
                                type: object
                                properties:
                                    code:
                                      type: string
                                    developer_message:
                                      type: string
                                    extra_payload:
                                      type: object
                                    message:
                                      type: string
        400:
          description: bad request
      security: []
    """

    created_cluster = CloudManagerService().add_cluster(parsed_request)
    response_schema = ClusterSerializer()
    response_data = response_schema.dump(created_cluster)
    return ApiResponse.build(status_code=200, data=response_data)


@blueprint.route("/clusters/<string:cluster_id>", methods=["PATCH"])
@schema_validator(ValidateEditClusterSerializer)
def edit_cluster(parsed_request, cluster_id):
    """Edit cluster
        ---
        patch:
          tags:
            - cluster
          parameters:
           - in: path
             name: cluster_id
             required: true
             schema:
                type: integer
          requestBody:
                content:
                  application/json:
                    schema:
                        $ref: '#/components/schemas/ValidateEditClusterSerializer'
          responses:
            200:
              content:
                application/json:
                    schema:
                        type: object
                        properties:
                            data:
                                type: object
                                $ref: "#/components/schemas/ClusterSerializer"
                            meta:
                                type: object
                                additionalProperties: {}
                            errors:
                                type: array
                                items:
                                    type: object
                                    properties:
                                        code:
                                          type: string
                                        developer_message:
                                          type: string
                                        extra_payload:
                                          type: object
                                        message:
                                          type: string
            400:
              description: bad request
          security: []
        """

    cluster_obj = CloudManagerOperation().edit_cluster(cluster_id, parsed_request)
    edited_cluster = CloudManagerService.create_cluster_dict_for_response(cluster_obj)
    response_schema = MachineSerializer()
    response_data = response_schema.dump(edited_cluster)
    return ApiResponse.build(status_code=200, data=response_data)


@blueprint.route("/clusters/<string:cluster_id>", methods=["DELETE"])
def delete_cluster(cluster_id):
    """Delete cluster
        ---
        delete:
          tags:
            - cluster
          parameters:
           - in: path
             name: cluster_id
             required: true
             schema:
                type: integer
          responses:
            204:
              description: object is deleted
            400:
              description: bad request
          security: []
        """

    CloudManagerOperation().delete_cluster(cluster_id)
    return ApiResponse.build(status_code=204)


@blueprint.route("/machines", methods=["GET"])
def get_all_machines():

    """Get list of all machines
    ---
    get:
      tags:
        - machine
      parameters:
       - in: query
         name: cluster_name
         required: false
         schema:
            type: string
       - in: query
         name: tag
         required: false
         schema:
            type: string
      responses:
        200:
          content:
            application/json:
                schema:
                    type: object
                    properties:
                        data:
                            type: array
                            items:
                                $ref: "#/components/schemas/MachineSerializer"
                        meta:
                            type: object
                            additionalProperties: {}
                        errors:
                            type: array
                            items:
                                type: object
                                properties:
                                    code:
                                      type: string
                                    developer_message:
                                      type: string
                                    extra_payload:
                                      type: object
                                    message:
                                      type: string
        400:
          description: bad request
      security: []
    """

    tag = request.args.get("tag")
    cluster_name = request.args.get("cluster_name")
    machines = MachineRepository.get_all_machines([tag], cluster_name)
    machine_list = CloudManagerService().create_machine_list_for_response(machines)
    response_schema = MachineSerializer(many=True)
    response_data = response_schema.dump(machine_list)
    return ApiResponse.build(status_code=200, data=response_data)


@blueprint.route("/machines/<string:machine_id>", methods=["GET"])
def get_machine(machine_id):

    """Get list of all machines
    ---
    get:
      tags:
        - machine
      parameters:
       - in: path
         name: machine_id
         required: false
         schema:
            type: string
      responses:
        200:
          content:
            application/json:
                schema:
                    type: object
                    properties:
                        data:
                            type: object
                            $ref: "#/components/schemas/MachineSerializer"
                        meta:
                            type: object
                            additionalProperties: {}
                        errors:
                            type: array
                            items:
                                type: object
                                properties:
                                    code:
                                      type: string
                                    developer_message:
                                      type: string
                                    extra_payload:
                                      type: object
                                    message:
                                      type: string
        400:
          description: bad request
      security: []
    """
    print(machine_id)
    machine_obj = MachineRepository.get_machine_by_id(machine_id)
    print(machine_obj)
    machine = CloudManagerService().create_machine_dict_for_response(machine_obj)
    response_schema = MachineSerializer()
    response_data = response_schema.dump(machine)
    return ApiResponse.build(status_code=200, data=response_data)


@blueprint.route("/machines", methods=["POST"])
@schema_validator(ValidateAddMachineSerializer)
def add_machine(parsed_request):
    """Create new machine
        ---
        post:
          tags:
            - machine
        requestBody:
            content:
              application/json:
                schema:
                    $ref: '#/components/schemas/ValidateAddMachineSerializer'
        responses:
            200:
              content:
                application/json:
                    schema:
                        type: object
                        properties:
                            data:
                                type: object
                                $ref: "#/components/schemas/MachineSerializer"
                            meta:
                                type: object
                                additionalProperties: {}
                            errors:
                                type: array
                                items:
                                    type: object
                                    properties:
                                        code:
                                          type: string
                                        developer_message:
                                          type: string
                                        extra_payload:
                                          type: object
                                        message:
                                          type: string
            400:
              description: bad request
        security: []
        """
    created_machine = CloudManagerService().add_machine(parsed_request)
    response_schema = MachineSerializer()
    response_data = response_schema.dump(created_machine)
    return ApiResponse.build(status_code=200, data=response_data)


@blueprint.route("/machines/<string:machine_id>", methods=["PATCH"])
@schema_validator(ValidateEditMachineSerializer)
def edit_machine(parsed_request, machine_id):
    """Edit machine
    ---
    patch:
        tags:
           - machine
        parameters:
           - in: path
             name: machine_id
             required: true
             schema:
                type: integer
        requestBody:
            content:
              application/json:
                schema:
                    $ref: '#/components/schemas/ValidateEditMachineSerializer'
    responses:
        200:
          content:
            application/json:
                schema:
                    type: object
                    properties:
                        data:
                            type: object
                            $ref: "#/components/schemas/MachineSerializer"
                        meta:
                            type: object
                            additionalProperties: {}
                        errors:
                            type: array
                            items:
                                type: object
                                properties:
                                    code:
                                      type: string
                                    developer_message:
                                      type: string
                                    extra_payload:
                                      type: object
                                    message:
                                      type: string
        400:
          description: bad request
    security: []
    """
    machine_obj = CloudManagerOperation().edit_machine(machine_id, parsed_request)
    edited_machine = CloudManagerService.create_machine_dict_for_response(machine_obj)
    response_schema = MachineSerializer()
    response_data = response_schema.dump(edited_machine)
    return ApiResponse.build(status_code=200, data=response_data)


@blueprint.route("/machines/<string:machine_id>", methods=["POST"])
def operate_machine(machine_id):
    """take action on machine
    ---
    post:
        tags:
           - machine
        parameters:
           - in: path
             name: machine_id
             required: true
             schema:
                type: string
           - in: query
             name: action
             required: true
             schema:
                type: string
                enum:
                    - REBOOT
                    - START
                    - STOP
                    - TERMINATE
    responses:
        200:
          content:
            application/json:
                schema:
                    type: object
                    properties:
                        data:
                            type: object
                            $ref: "#/components/schemas/MachineSerializer"
                        meta:
                            type: object
                            additionalProperties: {}
                        errors:
                            type: array
                            items:
                                type: object
                                properties:
                                    code:
                                      type: string
                                    developer_message:
                                      type: string
                                    extra_payload:
                                      type: object
                                    message:
                                      type: string
        400:
          description: bad request
    security: []
    """

    action = request.args.get("action")
    machine_obj = CloudManagerService().run_operation_on_machine(machine_id, action)
    edited_machine = CloudManagerService.create_machine_dict_for_response(machine_obj)
    response_schema = MachineSerializer()
    response_data = response_schema.dump(edited_machine)
    return ApiResponse.build(status_code=200, data=response_data)


@blueprint.route("/site-constants", methods=["GET"])
def get_constants():
    """constants
        ---
        get:
            tags:
              - constant
            parameters:
               - in: query
                 name: constant
                 required: false
                 schema:
                    type: string
                    enum:
                       - machine_state
                       - region
        responses:
            200:
              content:
                application/json:
                    schema:
                        type: object
                        properties:
                            data:
                                type: object
                                properties:
                                    code:
                                        type:string
                                    name:
                                        type:string
                            meta:
                                type: object
                                additionalProperties: {}
                            errors:
                                type: array
                                items:
                                    type: object
                                    properties:
                                        code:
                                          type: string
                                        developer_message:
                                          type: string
                                        extra_payload:
                                          type: object
                                        message:
                                          type: string
            400:
              description: bad request
        security: []
        """
    constant = request.args.get("constant")
    constant_class = SITE_CONSTANT_SWITCHER.get(constant)
    constant_value_list = []
    if constant_class:
        for name, value in constant_class.choices():
            constant_dict = {"code": name, "value": value}
            constant_value_list.append(constant_dict)
    return ApiResponse.build(status_code=200, data=constant_value_list)
