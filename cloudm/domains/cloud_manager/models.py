import datetime
from enum import Enum

from cloudm.extensions import db, pwd_context


class CloudMBaseEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def names(cls):
        return [i.name for i in cls]

    @classmethod
    def values(cls):
        return [i.value for i in cls]


class MachineStateChoices(CloudMBaseEnum):

    RUNNING = "Running"
    STOPPED = "Stopped"
    TERMINATED = "Terminated"


class OperationTypeChoices(CloudMBaseEnum):

    START = "Start"
    STOP = "Stop"
    REBOOT = "Reboot"
    TERMINATE = "Terminate"


class RegionChoices(CloudMBaseEnum):

    A = "A"
    B = "B"
    C = "C"
    D = "D"


class Cluster(db.Document):

    name = db.StringField(required=True, unique=True, max_length=250)
    region = db.StringField(
        choices=RegionChoices.choices(), default=RegionChoices.A.name
    )

    meta = {"collection": "cluster"}
    created_at = db.DateTimeField(required=True, default=datetime.datetime.now())


class Machine(db.Document):

    name = db.StringField(required=True, unique=True, max_length=250)
    ipv4 = db.StringField(required=True, unique=True)
    ipv6 = db.StringField(required=True, unique=True)
    tags = db.ListField(db.StringField(), required=False)
    state = db.StringField(
        required=True,
        choices=MachineStateChoices.choices(),
        default=MachineStateChoices.RUNNING.name,
    )
    cluster = db.ReferenceField(Cluster)

    meta = {"collection": "machine"}
    created_at = db.DateTimeField(required=True, default=datetime.datetime.now())


class Operation(db.Document):

    type = db.StringField(required=True, choices=OperationTypeChoices.choices())
    machine = db.ReferenceField(Machine)
    performed_on = db.DateTimeField(required=True, default=datetime.datetime.now())
