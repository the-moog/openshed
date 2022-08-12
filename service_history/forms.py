
from django import forms
from utilities.forms.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
import datetime
from openshed.jsignature.forms import JSignatureField, JSignatureWidget


class ProductForm(forms.Form):
    category = DynamicModelChoiceField(queryset=Category.objects.all(), display_field='name', required=False)
    vendor = DynamicModelChoiceField(queryset=Vendor.objects.all(), display_field='name', required=False)
    name = forms.CharField(max_length=20)
    description = forms.CharField(max_length=30, required=False)
