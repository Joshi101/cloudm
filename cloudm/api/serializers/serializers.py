from marshmallow import Schema, fields
from marshmallow.validate import OneOf

from cloudm.domains.cloud_manager.models import MachineStateChoices


class OperationSerializer(Schema):

    type = fields.String()
    performed_on = fields.DateTime(format="%Y-%m-%d %H:%M:%S")


class MachineSerializer(Schema):

    name = fields.String()
    id = fields.String()
    ipv4 = fields.String()
    ipv6 = fields.String()
    cluster_id = fields.String()
    cluster_name = fields.String()
    region = fields.String()
    state = fields.String()
    tags = fields.List(fields.String)
    operations = fields.Nested(OperationSerializer, many=True)


class ValidateAddMachineSerializer(Schema):

    name = fields.String()
    cluster_name = fields.String()
    tags = fields.List(fields.String())


class ValidateEditMachineSerializer(Schema):

    name = fields.String(required=False)
    tags = fields.List(fields.String(), required=False)


class ClusterSerializer(Schema):

    name = fields.String()
    id = fields.String()
    region = fields.String()
    region_code = fields.String()


class ValidateAddClusterSerializer(Schema):

    name = fields.String()
    region_code = fields.String()


class ValidateEditClusterSerializer(Schema):

    name = fields.String()
    region_code = fields.String()
