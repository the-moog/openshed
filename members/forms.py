from django import forms
from .models import Member

class MemberForm(forms.Form):
    last_name = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20)
    departure_date = forms.DateField(required=False)
