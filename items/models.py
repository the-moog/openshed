from django.db import models
from phone_field import PhoneField as OldPhoneField
from phone_field import PhoneNumber
from address.models import AddressField
from utilities.base_x import IntBaseX
from django.core.files.storage import FileSystemStorage
from members.models import Member
from items.utils import release_reserved
import datetime



itemfs = FileSystemStorage(location='media/items')


class PhoneField(OldPhoneField):
    # see GitHub
    def get_prep_value(self, value):
        if not value:
            # return ''
            return None

        if not isinstance(value, PhoneNumber):
            value = PhoneNumber(value)
        return value.cleaned


# Suppliers.
class Supplier(models.Model):
    """Suppliers are the source of vendor products"""
    name = models.CharField(max_length=100, unique=True)
    contact = models.CharField(max_length=100, null=True, blank=True, default=None, help_text='Contact name')
    url = models.URLField(null=True, unique=True, default=None, help_text='Website')
    address = AddressField(null=True, unique=True, default=None, help_text='Contact address')
    phone = PhoneField(null=True, unique=True, default=None, help_text='Contact phone number')
    email = models.EmailField(null=True, unique=True, default=None)


# Vendors.
class Vendor(models.Model):
    """Vendor is the Original Equipment Manufacturer"""
    name = models.CharField(max_length=100, unique=True)


# Categories.
class Category(models.Model):
    """Category is the collective name for similar products"""
    name = models.CharField(max_length=20, unique=True)


# Products
class Product(models.Model):
    """Products are made by Vendors and sold by Suppliers"""
    vendor = models.ForeignKey(Vendor, null=True, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, null=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.long_name()

    def long_name(self):
        return f"({self.category.name}) {self.name} {self.description} by {self.vendor.name}"


# Items
class Item(models.Model):
    """An item is a single instance of a product"""
    item = models.CharField(max_length=20, unique=True)



    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)

    serial = models.CharField(max_length=20, blank=True, default='')
    size = models.CharField(max_length=5, blank=True, default='')
    commissioning_date = models.DateField(null=True)
    decommissioning_date = models.DateField(null=True)
    comment = models.CharField(max_length=50, blank=True, default='')
    image = models.ImageField(storage=itemfs, blank=True)

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

