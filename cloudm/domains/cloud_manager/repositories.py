from cloudm.domains.cloud_manager.models import Machine, Cluster


class MachineRepository:

    @staticmethod
    def get_machine_by_id(machine_id):

        return Machine.objects.filter(id=machine_id).first()

    @staticmethod
    def get_all_machines():

        return Machine.objects.all()

    @staticmethod
    def get_machine_by_name(machine_name):
        return Machine.objects.filter(name=machine_name).first()

    @staticmethod
    def get_machine_by_tags(tags):
        return Machine.objects.filter(tags__in=tags).all()

    @staticmethod
    def add_machine(**kwargs):
        machine = Machine(**kwargs).save()
        return machine

    @staticmethod
    def update_tags(machine_obj, tags):

        machine_obj.tags.extend(tags)
        machine_obj.save()
        return machine_obj


class ClusterRepository:

    @staticmethod
    def add_cluster(**kwargs):
        machine = Cluster(**kwargs).save()
        return machine

    @staticmethod
    def filter_cluster_by_name(name):

        return Cluster.objects.filter(name__contains=name).all()

    @staticmethod
    def get_cluster_by_region(region_name):
        return Cluster.objects.filter(region=region_name).all()

    @staticmethod
    def delete_cluster(cluster):
        cluster.delete()
        return




