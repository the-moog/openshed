from django import forms
from utilities.forms.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
import datetime
from openshed.jsignature.forms import JSignatureField, JSignatureWidget


class LoanOutForm(forms.Form):
    now = datetime.datetime.now()
    then = now + datetime.timedelta(days=1)
    until_dt = forms.DateField(label="Return by", required=True, initial=then, widget=DatePickerInput)
    reason = forms.CharField(label="Reason for loan", required=True, widget=forms.Textarea)


class LoanSignOffForm(forms.Form):
    until_dt = forms.DateField(label="Return by 9pm on", required=True, widget=DatePickerInput)
    reason = forms.CharField(label="Reason for loan", required=True, widget=forms.Textarea)
    signature = JSignatureField(label="Signature against receipt of items", required=True,
                                widget=JSignatureWidget(jsignature_attrs={'background-color': 'grey'}))

