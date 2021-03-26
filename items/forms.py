from django import forms
from .models import ItemType, Vendor, Category

from members.models import Member

import datetime

from utilities.forms.fields import DynamicModelChoiceField

class VendorForm(forms.Form):
    name = forms.CharField(max_length=20)

class CategoryForm(forms.Form):
    name = forms.CharField(max_length=20)

class ItemForm(forms.Form):
    name = forms.CharField(max_length=20)
    type = DynamicModelChoiceField(queryset=ItemType.objects.all(), display_field='type')
    serial = forms.CharField(max_length=20, required=False)
    size = forms.CharField(max_length=5, required=False)
    commissioning_date = forms.DateField(initial=datetime.date.today)
    comment = forms.CharField(max_length=50, required=False)
    member = DynamicModelChoiceField(queryset=Member.objects.all(), display_field='display_name')

class TypeForm(forms.Form):
    category = DynamicModelChoiceField(queryset=Category.objects.all(), display_field='name')
    vendor = DynamicModelChoiceField(queryset=Vendor.objects.all(), display_field='name', required=False)
    type = forms.CharField(max_length=20)
    description = forms.CharField(max_length=30)
