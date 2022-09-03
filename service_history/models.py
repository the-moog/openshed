from django.db import models
from django.db.models import Q


class ServiceSchedule(models.Model):
    """A given Category can have zero or more service schedules"""
    interval = models.OneToOneField('schedule.Rule', on_delete=models.PROTECT)
    category = models.ForeignKey('items.Category', on_delete=models.PROTECT)


class ServiceHistory(models.Model):
    """A given item of a Category that is serviceable (has a ServiceSchedule)
    can have multiple service history records"""
    item = models.ForeignKey('items.Item', on_delete=models.PROTECT)
    out_dt = models.DateField()
    ret_dt = models.DateField()
    comment = models.TextField()
    report = models.FileField()
    service_by = models.ForeignKey('items.Supplier', on_delete=models.PROTECT)

    @property
    def next_service(self):
        services = self.objects.filter(service_by__item=self.item)
        service = services.exclude(Q(ret_dt__isnull=True)).order_by("out_dt").last()
        return service.item.last_service + self.interval




