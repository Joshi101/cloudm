from marshmallow import Schema, fields


class MachineSerializer(Schema):

    name = fields.String()
    id = fields.String()
    ip_address = fields.String()
    cluster_id = fields.String()
    cluster_name = fields.String()
    region = fields.String()
    state = fields.String()
    tags = fields.List(fields.String)


class ValidateAddMachineSerializer(Schema):

    name = fields.String()
    cluster_name = fields.String()
    tags = fields.List(fields.String())


