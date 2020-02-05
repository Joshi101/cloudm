

class CloudManagerService:

    def __init__(self):
        pass

    @staticmethod
    def create_machine_list_for_response(machine_objects):

        machine_list = []
        for machine in machine_objects:
            machine_dict = dict()
            machine_dict["name"] = machine.name
            machine_dict["id"] = machine.id
            machine_dict["ip"] = machine.ip_address
            machine_dict["cluster_name"] = machine.cluster
            machine_dict["region"] = machine.cluster.region
            machine_dict["state"] = machine.state
            machine_dict["cluster_id"] = str(machine.cluster.id)
            machine_dict["tags"] = machine.tags
            machine_list.append(machine_dict)

        return machine_list