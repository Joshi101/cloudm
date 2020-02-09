from cloudm.domains.cloud_manager.models import Machine, Cluster, Operation


class MachineRepository:
    @staticmethod
    def get_machine_by_id(machine_id):

        return Machine.objects.filter(id=machine_id).first()

    @staticmethod
    def get_all_machines(tags=None, cluster_name=None):

        qs = Machine.objects.filter()
        if tags:
            qs.filter(tags__in=tags)
        if cluster_name:
            qs.filter(cluster__name__iexact=cluster_name)

        return qs.all()

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
    def edit_machine(machine_obj, **kwargs):
        machine_obj.update(**kwargs)
        machine_obj.reload()
        return machine_obj

    @staticmethod
    def update_tags(machine_obj, tags):

        machine_obj.tags.extend(tags)
        machine_obj.save()
        return machine_obj

    @staticmethod
    def delete_machine(machine):
        machine.delete()
        return


class ClusterRepository:
    @staticmethod
    def get_cluster_by_id(cluster_id):
        return Cluster.objects.filter(id=cluster_id).first()

    @staticmethod
    def get_all_clusters():
        return Cluster.objects.all()

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
    def get_cluster_by_name(name):
        return Cluster.objects.filter(name=name).first()

    @staticmethod
    def delete_cluster(cluster):
        cluster.delete()
        return

    @staticmethod
    def edit_clister(cluster_obj, **kwargs):
        cluster_obj.update(**kwargs)
        cluster_obj.reload()
        return cluster_obj


class OperationRepository:
    @staticmethod
    def get_all_machine_operations():

        return Operation.objects.all()

    @staticmethod
    def add_operation(**kwargs):
        operation = Operation(**kwargs).save()
        return operation
