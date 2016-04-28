from django.db import models

from nodeconductor.structure import models as structure_models


class OracleService(structure_models.Service):
    projects = models.ManyToManyField(
        structure_models.Project, related_name='oracle_services', through='OracleServiceProjectLink')

    @classmethod
    def get_url_name(cls):
        return 'oracle'


class OracleServiceProjectLink(structure_models.ServiceProjectLink):
    service = models.ForeignKey(OracleService)

    @classmethod
    def get_url_name(cls):
        return 'oracle-spl'


class Flavor(structure_models.GeneralServiceProperty):
    cores = models.PositiveSmallIntegerField(help_text='Number of cores in a VM')
    ram = models.PositiveIntegerField(help_text='Memory size in MiB')
    disk = models.PositiveIntegerField(help_text='Root disk size in MiB')


class Deployment(structure_models.Resource):

    service_project_link = models.ForeignKey(
        OracleServiceProjectLink, related_name='deployments', on_delete=models.PROTECT)

    support_request = models.ForeignKey('nodeconductor_jira.Issue', related_name='+', null=True)
    tenant = models.ForeignKey('openstack.Tenant', related_name='+')
    flavor = models.ForeignKey(Flavor, related_name='+')
    report = models.TextField(blank=True)
    db_name = models.CharField(max_length=256)
    db_size = models.PositiveIntegerField(help_text='Storage size in GB')
    db_type = models.CharField(max_length=256)
    db_version = models.CharField(max_length=256)
    db_template = models.CharField(max_length=256)
    db_charset = models.CharField(max_length=256)
    user_data = models.TextField(blank=True)

    @property
    def flavor_info(self):
        flavor = self.flavor
        backend = self.get_backend()
        return "%s -- vCPUs: %d, RAM: %d GB, System Storage: %d GB" % (
            flavor.name,
            flavor.cores,
            backend.mb2gb(flavor.ram),
            backend.mb2gb(flavor.disk))

    @classmethod
    def get_url_name(cls):
        return 'oracle-deployments'