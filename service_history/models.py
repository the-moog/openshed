from django.db import models
from items.models import Item, Supplier
from django.db.models import Q
from timedelta import timedelta


class ServiceHistory(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    interval = timedelta.fields.TimedeltaField()
    out_dt = models.DateField()
    ret_dt = models.DateField()
    comment = models.TextField()
    report = models.FileField()
    service_by = models.ForeignKey(Supplier, on_delete=models.PROTECT)

    @property
    def next_service(self):
        services = self.objects.filter(service_by__item=self.item)
        service = services.exclude(Q(ret_dt__isnull=True)).order_by("out_dt").last()
        return service.item.last_service + self.interval


