from django.db import models

from django.core.files.storage import FileSystemStorage
from members.models import Member
from utilities.base_x import IntBaseX
from items.utils import release_reserved
import datetime
from service_history.models import ServiceSchedule, ServiceHistory
from schedule.models.events import EventRelation


itemfs = FileSystemStorage(location='media/items')


# Items
class Item(models.Model):
    """An item is a single instance of a product"""
    item = models.CharField(max_length=20, unique=True)

    product = models.ForeignKey('items.Product', on_delete=models.PROTECT)
    supplier = models.ForeignKey('items.Supplier', on_delete=models.PROTECT)

    serial = models.CharField(max_length=20, blank=True, default='')
    size = models.CharField(max_length=5, blank=True, default='')
    commissioning_date = models.DateField(null=True)
    decommissioning_date = models.DateField(null=True)
    comment = models.CharField(max_length=50, blank=True, default='')
    image = models.ImageField(storage=itemfs, blank=True)
    calendar = models.OneToOneField('schedule.Calendar', on_delete=models.PROTECT)
    reserved_until = models.DateTimeField(null=True)
    reserved_by = models.ForeignKey(Member, null=True, on_delete=models.PROTECT)
    reserved_session = models.CharField(max_length=32, blank=True, default='')
    is_serviceable = models.BooleanField(default=True)  # Item is not broken in some way

    @property
    def uid(self):
        return IntBaseX(self.id).as_base(pad_zero=10).upper()

    @property
    def on_loan(self):
        from lending.models import LentItems
        loans = LentItems.objects.filter(item_id=self.id, return_dt__isnull=True)
        assert len(loans) <= 1
        if len(loans):
            return loans[0].loan.until_dt
        return None

    @property
    def reserved(self):
        was_reserved = self.reserved_until is not None
        still_reserved = was_reserved and self.reserved_until > datetime.datetime.utcnow()
        if was_reserved and not still_reserved:
            # Release a reserved item if timed out
            release_reserved(self)
            still_reserved = False
        return still_reserved

    @property
    def service_applicable(self):
        # The item is of a type that requires service
        return ServiceSchedule.objects.filter(category=self.product.category).count() > 0

    @property
    def last_service(self):
        # Get the date of last service if one exists else return None
        service_events = EventRelation.objects.get_events_for_object(self, 'Service')
        if not len(service_events):
            return None
        if service_events[-1].event.end is None:
            return service_events[-2].event.end
        return service_events[-1].event.end

    @property
    def next_service(self):
        # Get the date of next service.
        #
        # If item out for service return date sent out
        # If no service required return None
        # If the item requires service:
        #   If there is no previous service return today
        #   If there is a previous service get the schedule(s):
        #     If the most recent schedule has passed return today
        #     else return the soonest schedule date
        if not self.service_applicable:
            return None

        service_schedule = EventRelation.objects.get_events_for_object(self, 'Service Schedule')
        if self.out_for_service:
            service_schedule[-1].start

        if self.last_service is None:
            return datetime.datetime.today()
        else:
            # Note categories may have more than once service schedule
            # we only need the soonest one
            return service_schedule[0].start

    @property
    def out_for_service(self):
        # Return True if item is out for service
        service_events = EventRelation.objects.get_events_for_object(self, 'Service')
        if not len(service_events):
            return False
        return service_events[-1].event.end is None

    @property
    def is_in_service(self):
        # Return True if item is not out for service and is serviceable
        return not self.out_for_service and datetime.datetime.utcnow() > self.next_service and self.is_serviceable
