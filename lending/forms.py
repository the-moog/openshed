from django import forms
import datetime


class LoanOutForm(forms.Form):
    now = datetime.datetime.now()
    then = now + datetime.timedelta(days=1)
    until_dt = forms.DateField(label="Return by", required=True, widget=forms.SelectDateWidget(), initial=then)
    reason = forms.CharField(label="Reason for loan", required=True, widget=forms.Textarea())


class LoanSignOffForm(forms.Form):
    hire_to = forms.CharField(label="Loaned to", disabled=True)
    from_dt = forms.DateTimeField(label="Loan from", required=True, widget=forms.SplitDateTimeWidget())
    to_date = forms.DateField(label="Return by", required=True, widget=forms.SelectDateWidget())
    reason = forms.CharField(label="Reason for loan", required=True, widget=forms.Textarea())


