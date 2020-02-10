from cloudm.commons.apispec import APISpecExt
from cloudm.domains.cloud_manager.models import (
    RegionChoices,
    OperationTypeChoices,
    MachineStateChoices,
)
from cloudm.domains.cloud_manager.operations import CloudManagerOperation
from cloudm.domains.cloud_manager.repositories import (
    ClusterRepository,
    MachineRepository,
    OperationRepository,
)
from cloudm.exception import APIException


class CloudManagerService:
    def __init__(self):
        pass

    def get_machine_id_operations_mapping(self):

        operations = OperationRepository.get_all_machine_operations()
        map_dict = dict()
        for operation in operations:
            machine_id = operation.machine.id
            operation_dict = {
                "type": operation.type,
                "performed_on": operation.performed_on,
            }
            map_dict.setdefault(machine_id, []).append(operation_dict)
        return map_dict

    @staticmethod
    def create_machine_dict_for_response(
        machine_obj, machine_id_operation_mapping=None
    ):

        if not machine_id_operation_mapping:
            machine_id_operation_mapping = (
                CloudManagerService().get_machine_id_operations_mapping()
            )
        machine_dict = dict()
        machine_dict["name"] = machine_obj.name
        machine_dict["id"] = machine_obj.id
        machine_dict["ipv4"] = machine_obj.ipv4
        machine_dict["ipv6"] = machine_obj.ipv6
        machine_dict["cluster_name"] = machine_obj.cluster.name
        machine_dict["region"] = machine_obj.cluster.region
        machine_dict["state"] = machine_obj.state
        machine_dict["cluster_id"] = str(machine_obj.cluster.id)
        machine_dict["tags"] = machine_obj.tags
        machine_dict["operations"] = machine_id_operation_mapping.get(machine_obj.id)

        return machine_dict

    def create_machine_list_for_response(self, machine_objects):

        machine_list = []
        machine_id_operation_mapping = self.get_machine_id_operations_mapping()
        for machine in machine_objects:
            machine_dict = self.create_machine_dict_for_response(
                machine, machine_id_operation_mapping
            )
            machine_list.append(machine_dict)

        return machine_list

    def add_machine(self, machine_params):

        name = machine_params.get(
            "name", CloudManagerOperation().get_unique_machine_name()
        )
        ipv4 = CloudManagerOperation().get_unique_ipv4()
        ipv6 = CloudManagerOperation().get_unique_ipv6()
        cluster_name = machine_params.get("cluster_name")
        cluster = ClusterRepository.get_cluster_by_name(cluster_name)
        if not cluster:
            raise APIException(
                message="Cluster {} does not exists.".format(cluster_name)
            )
        tags = machine_params.get("tags")

        created_machine = MachineRepository.add_machine(
            name=name, ipv4=ipv4, ipv6=ipv6, cluster=cluster, tags=tags
        )

        return self.create_machine_dict_for_response(created_machine)

    @staticmethod
    def create_cluster_dict_for_response(cluster_obj):

        cluster_dict = dict()
        cluster_dict["name"] = cluster_obj.name
        cluster_dict["id"] = cluster_obj.id
        cluster_dict["region"] = cluster_obj.region

        return cluster_dict

    def create_cluster_list_for_response(self, cluster_objects):

        cluster_list = []
        for cluster in cluster_objects:
            cluster_dict = self.create_cluster_dict_for_response(cluster)
            cluster_list.append(cluster_dict)
        return cluster_list

    def add_cluster(self, cluster_params):

        name = cluster_params.get("name")
        region_code = cluster_params.get("region_code")
        if region_code not in RegionChoices.names():
            region_code = None

        cluster = ClusterRepository.add_cluster(name=name, region=region_code)

        return self.create_cluster_dict_for_response(cluster)

    def run_operation_on_machine(self, machine_id, action):

        machine = MachineRepository.get_machine_by_id(machine_id)
        if action == OperationTypeChoices.START.name:

            if machine.state != MachineStateChoices.RUNNING.name:
                _ = OperationRepository.add_operation(
                    type=OperationTypeChoices.START.name, machine=machine
                )
                machine = MachineRepository.edit_machine(
                    machine, state=MachineStateChoices.RUNNING.name
                )
            else:
                raise APIException(message="Machine already in start state.")

        if action == OperationTypeChoices.REBOOT.name:

            _ = OperationRepository.add_operation(
                type=OperationTypeChoices.REBOOT.name, machine=machine
            )
            machine = MachineRepository.edit_machine(
                machine, state=MachineStateChoices.RUNNING.name
            )
        if action == OperationTypeChoices.TERMINATE.name:

            if machine.state != MachineStateChoices.TERMINATED.name:
                _ = OperationRepository.add_operation(
                    type=OperationTypeChoices.TERMINATE.name, machine=machine
                )
                machine = MachineRepository.edit_machine(
                    machine, state=MachineStateChoices.TERMINATED.name
                )
            else:
                raise APIException(message="Machine already terminated.")

        if action == OperationTypeChoices.STOP.name:

            if machine.state != MachineStateChoices.STOPPED.name:
                _ = OperationRepository.add_operation(
                    type=OperationTypeChoices.STOP.name, machine=machine
                )
                machine = MachineRepository.edit_machine(
                    machine, state=MachineStateChoices.STOPPED.name
                )
            else:
                raise APIException(message="Machine already in stop state.")
        return machine
