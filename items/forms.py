from django import forms
from .models import Product, Vendor, Category, Supplier
from phone_field import PhoneFormField
from address.forms import AddressField

import datetime

from utilities.forms.fields import DynamicModelChoiceField


class SupplierForm(forms.Form):
    name = forms.CharField()
    contact = forms.CharField(required=False)
    url = forms.URLField(required=False)
    address = AddressField(required=False)
    phone = PhoneFormField(required=False, help_text='Contact phone number')
    email = forms.EmailField(required=False)


class VendorForm(forms.Form):
    name = forms.CharField()


class CategoryForm(forms.Form):
    name = forms.CharField(max_length=20)


class ItemForm(forms.Form):
    name = forms.CharField(max_length=20)
    product = DynamicModelChoiceField(queryset=Product.objects.all(), display_field='name')
    supplier = DynamicModelChoiceField(queryset=Supplier.objects.all(), display_field='name')
    serial = forms.CharField(max_length=20, required=False)
    size = forms.CharField(max_length=5, required=False)
    commissioning_date = forms.DateField(initial=datetime.date.today, required=False)
    decommissioning_date = forms.DateField(required=False)
    comment = forms.CharField(max_length=50, required=False)
    image = forms.ImageField(allow_empty_file=True)


class ProductForm(forms.Form):
    category = DynamicModelChoiceField(queryset=Category.objects.all(), display_field='name', required=False)
    vendor = DynamicModelChoiceField(queryset=Vendor.objects.all(), display_field='name', required=False)
    name = forms.CharField(max_length=20)
    description = forms.CharField(max_length=30, required=False)
