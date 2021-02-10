from django import forms
from .models import ItemType

from utilities.forms.fields import DynamicModelChoiceField

class ItemForm(forms.Form):
    name = forms.CharField(label='name', max_length=100)
    type = DynamicModelChoiceField(queryset=ItemType.objects.all(), display_field='type')

class TypeForm(forms.Form):
    vendor = forms.CharField(label='vendor', max_length=50)
    type = forms.CharField(label='type', max_length=50)
    description = forms.CharField(label='description', max_length=100)
