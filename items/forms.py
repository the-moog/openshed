from django import forms

class ItemForm(forms.Form):
    name = forms.CharField(label='name', max_length=100)
    type = forms.IntegerField(label='Item type')

class TypeForm(forms.Form):
    vendor = forms.CharField(label='vendor', max_length=50)
    type = forms.CharField(label='type', max_length=50)
    description = forms.CharField(label='description', max_length=100)
