from django import forms

class TypeForm(forms.Form):
    vendor = forms.CharField(label='vendor', max_length=50)
    type = forms.CharField(label='type', max_length=50)
    description = forms.CharField(label='description', max_length=100)

class TypeDeleteForm(forms.Form):
    ok = forms.CharField(label='ok', max_length=50)
