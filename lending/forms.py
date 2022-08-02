from django import forms
import datetime


class LoanOutForm(forms.Form):
    now = datetime.datetime.now()
    then = now + datetime.timedelta(days=1)
    until_dt = forms.DateField(label="Return by", required=True, widget=forms.SelectDateWidget(), initial=then)
    reason = forms.CharField(label="Reason for loan", required=True, widget=forms.Textarea())


class SignoffForm(forms.Form):
    pass

