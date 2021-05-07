from django.db import models
from members.models import *

# Vendors.
class Vendor(models.Model):
    name = models.CharField(max_length=20, unique=True)

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
  serial = models.CharField(max_length=20, blank=True, default='')
  size = models.CharField(max_length=5, blank=True, default='')
  member = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL)
  commissioning_date = models.DateField(null=True)
  decommissioning_date = models.DateField(null=True)
  comment = models.CharField(max_length=50, blank=True, default='')
