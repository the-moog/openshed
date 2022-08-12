from django.db import models


# Vendors.
class Vendor(models.Model):
    """Vendor is the Original Equipment Manufacturer"""
    name = models.CharField(max_length=100, unique=True)

