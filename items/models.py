from django.db import models
from members.models import *
from phone_field import PhoneField
from address.models import AddressField

# Suppliers.
class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact = models.CharField(max_length=100)
    url = models.URLField(blank=True, null=True)
    address = AddressField(blank=True, null=True)
    phone = PhoneField(blank=True, null=True, help_text='Contact phone number')
    email = models.EmailField(unique=True, null=True)

# Vendors.
class Vendor(models.Model):
    name = models.CharField(max_length=100, unique=True)

# Categories.
class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)

# Item types.
class ItemType(models.Model):
    vendor = models.ForeignKey(Vendor, null=True, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, null=True, on_delete=models.PROTECT)
    type = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=30, blank=True, default='')

# Items
class Item(models.Model):
  item = models.CharField(max_length=20, unique=True)
  item_type = models.ForeignKey(ItemType, on_delete=models.PROTECT)
  supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
  serial = models.CharField(max_length=20, blank=True, default='')
  size = models.CharField(max_length=5, blank=True, default='')
  member = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL)
  commissioning_date = models.DateField(null=True)
  decommissioning_date = models.DateField(null=True)
  comment = models.CharField(max_length=50, blank=True, default='')
