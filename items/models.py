from members.models import *
from phone_field import PhoneField
from address.models import AddressField


# Suppliers.
class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    contact = models.CharField(max_length=100, help_text='Contact name', blank=True, default=None)
    url = models.URLField(blank=True, null=True, unique=True, default=None, help_text='Website')
    address = AddressField(blank=True, null=True, unique=True, default=None, help_text='Contact address')
    phone = PhoneField(unique=True, default=None, blank=True, null=True, help_text='Contact phone number')
    email = models.EmailField(unique=True, null=True, default=None)


# Vendors.
class Vendor(models.Model):
    """Vendor is the Original Equipment Manufacturer"""
    name = models.CharField(max_length=100, unique=True)


# Categories.
class Category(models.Model):
    """Category is a tag applied to an itemtype"""
    name = models.CharField(max_length=20, unique=True)


# Item types.
class ItemType(models.Model):
    """An item type is a class of item"""
    vendor = models.ForeignKey(Vendor, null=True, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, null=True, on_delete=models.PROTECT)
    type = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=30, blank=True, default='')


# Items
class Item(models.Model):
    """An item is a single instance of a registered item"""
    item = models.CharField(max_length=20, unique=True)
    item_type = models.ForeignKey(ItemType, on_delete=models.PROTECT)

    """Who supplied this item?"""
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)

    serial = models.CharField(max_length=20, blank=True, default='')
    size = models.CharField(max_length=5, blank=True, default='')

    commissioning_date = models.DateField(null=True)
    decommissioning_date = models.DateField(null=True)
    comment = models.CharField(max_length=50, blank=True, default='')
