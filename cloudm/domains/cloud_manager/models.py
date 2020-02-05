from enum import Enum

from cloudm.extensions import db, pwd_context


class CloudMBaseEnum(Enum):

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class MachineStatusChoices(CloudMBaseEnum):

    RUNNING = "Running"
    STOPPED = "Stopped"
    DELETED = "Terminated"


class OperationTypeChoices(CloudMBaseEnum):

    START = "Start"
    STOP = "Stop"
    REBOOT = "Reboot"


class RolePermissionChoices(CloudMBaseEnum):

    edit_cluster = "Edit Cluster"
    edit_machine = "Edit Machine"
    operate_machine = "Operate Machine"


class RegionChoices(CloudMBaseEnum):

    A = "A"
    B = "B"
    C = "C"
    D = "D"


class Role(db.Document):
    """Basic user model
    """

    name = db.StringField(required=True, unique=True, max_length=250)
    permissions = db.ListField(db.StringField(choices=RolePermissionChoices.choices()))

    meta = {
        "collection": "role"
    }


class Cluster(db.Document):

    name = db.StringField(required=True, unique=True, max_length=250)
    region = db.StringField(choices=RegionChoices.choices())

    meta = {
        "collection": "cluster"
    }


class Machine(db.Document):

    name = db.StringField(required=True, unique=True, max_length=250)
    ip_address = db.StringField(required=True, unique=True)
    tags = db.ListField(db.StringField(), required=False)
    state = db.StringField(required=True, choices=MachineStatusChoices.choices())
    cluster = db.ReferenceField(Cluster)

    meta = {
        "collection": "machine"
    }


class Operation(db.Document):

    operation_id = db.UUIDField(binary=False)
    type = db.StringField(required=True, unique=True, choices=MachineStatusChoices.choices())
    machine = db.ReferenceField(Machine)