from django import forms
from .models import ItemType

import datetime

from utilities.forms.fields import DynamicModelChoiceField

class ItemForm(forms.Form):
    name = forms.CharField(label='name', max_length=100)
    type = DynamicModelChoiceField(queryset=ItemType.objects.all(), display_field='type')
    serial = forms.CharField(label='serial', max_length=20)
    size = forms.CharField(label='size', max_length=5)
    commissioning_date = forms.DateField(initial=datetime.date.today)
    comment = forms.CharField(label='description', max_length=50)

class TypeForm(forms.Form):
    vendor = forms.CharField(label='vendor', max_length=50)
    type = forms.CharField(label='type', max_length=50)
    description = forms.CharField(label='description', max_length=30)
