from django.db import models
from address.models import AddressField
from utilities.forms.fields import PhoneField


# Suppliers.
class Supplier(models.Model):
    """Suppliers are the source of vendor products"""
    name = models.CharField(max_length=100, unique=True)
    contact = models.CharField(max_length=100, null=True, blank=True, default=None, help_text='Contact name')
    url = models.URLField(null=True, unique=True, default=None, help_text='Website')
    address = AddressField(null=True, unique=True, default=None, help_text='Contact address')
    phone = PhoneField(null=True, unique=True, default=None, help_text='Contact phone number')
    email = models.EmailField(null=True, unique=True, default=None)


