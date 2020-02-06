from marshmallow import Schema, fields
from marshmallow.validate import OneOf

from cloudm.domains.cloud_manager.models import MachineStateChoices


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


class ValidateAddMachineSerializer(Schema):

    name = fields.String()
    cluster_name = fields.String()
    tags = fields.List(fields.String())


class ValidateEditMachineSerializer(Schema):

    name = fields.String()
    tag = fields.String()
    state_code = fields.String(validate=OneOf(MachineStateChoices.names()))


class ClusterSerializer(Schema):

    name = fields.String()
    id = fields.String()
    region = fields.String()
    region_code = fields.String()


class ValidateAddClusterSerializer(Schema):

    name = fields.String()
    region_code = fields.String()
