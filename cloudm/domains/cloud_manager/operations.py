from faker import Faker
from string import ascii_letters

from cloudm.domains.cloud_manager.repositories import MachineRepository


def generate_random_name():

    allowed = ascii_letters + "-"
    fake = Faker("it_IT")
    name = fake.name()
    continuous_name = "-".join(name.split(" "))
    clean_name = "".join(l for l in continuous_name if l in allowed)
    return clean_name.lower()


class CloudManagerOperation:
    def __init__(self):

        pass

    def get_all_machine_names(self):

        machines = MachineRepository.get_all_machines()
        names = [m.name for m in machines]
        return names

    def get_unique_machine_name(self):

        existing_machine_name = self.get_all_machine_names()
        while True:
            generated_name = generate_random_name()
            if generated_name not in existing_machine_name:
                break
        return generated_name

    def get_all_machine_ipv4(self):

        machines = MachineRepository.get_all_machines()
        ipv4_list = [m.ipv4 for m in machines]
        return ipv4_list

    def get_unique_ipv4(self):

        """
            currently generating random unique ip address.
            Practically there should be a range option to generate ip address
        """

        fake = Faker()
        existing_ipv4s = self.get_all_machine_ipv4()
        while True:
            ipv4 = fake.ipv4()
            if ipv4 not in existing_ipv4s:
                break

        return ipv4

    def get_all_machine_ipv6(self):

        machines = MachineRepository.get_all_machines()
        ipv6_list = [m.ipv6 for m in machines]
        return ipv6_list

    def get_unique_ipv6(self):

        """
            currently generating random unique ip address.
            Practically there should be a range option to generate ip address
        """

        fake = Faker()
        existing_ipv6s = self.get_all_machine_ipv6()
        while True:
            ipv6 = fake.ipv6()
            if ipv6 not in existing_ipv6s:
                break

        return ipv6

    def edit_machine(self, machine_id, machine_params):

        machine_obj = MachineRepository.get_machine_by_id(machine_id)
        edit_dict = dict()
        if "name" in machine_params:
            edit_dict["name"] = machine_params["name"]
        if "tag" in machine_params:
            updated_tags = machine_obj.tags
            if machine_params["tag"] not in updated_tags:
                updated_tags.append(machine_params["tag"])
            edit_dict["tags"] = updated_tags
        machine_obj = MachineRepository.edit_machine(machine_obj, **edit_dict)

        return machine_obj
