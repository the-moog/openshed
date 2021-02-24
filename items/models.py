from django.db import models
from members.models import *

# Vendors.
class Vendor(models.Model):
    name = models.CharField(max_length=20)

# Item types.
class ItemType(models.Model):
    vendor = models.ForeignKey(Vendor, null=True, on_delete=models.PROTECT)
    type = models.CharField(max_length=20)
    description = models.CharField(max_length=30)

# Items
class Item(models.Model):
  item = models.CharField(max_length=20)
  item_type = models.ForeignKey(ItemType, on_delete=models.PROTECT)
  serial = models.CharField(max_length=20, null=True)
  size = models.CharField(max_length=5, null=True)
  member = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL)
  commissioning_date = models.DateField(null=True)
  comment = models.CharField(max_length=50, null=True)
