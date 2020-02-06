from cloudm.domains.cloud_manager.models import RegionChoices
from cloudm.domains.cloud_manager.operations import CloudManagerOperation
from cloudm.domains.cloud_manager.repositories import (
    ClusterRepository,
    MachineRepository,
)


class CloudManagerService:
    def __init__(self):
        pass

    @staticmethod
    def create_machine_dict_for_response(machine_obj):

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

        return machine_dict

    def create_machine_list_for_response(self, machine_objects):

        machine_list = []
        for machine in machine_objects:
            machine_dict = self.create_machine_dict_for_response(machine)
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
            raise
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
