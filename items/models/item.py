from django.db import models

from django.core.files.storage import FileSystemStorage
from members.models import Member
from utilities.base_x import IntBaseX
from items.utils import release_reserved
import datetime


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
    def last_service(self):
        return datetime.datetime.utcnow()
