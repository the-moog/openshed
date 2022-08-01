from django import forms


class LoanForm(forms.Form):
    lent_by = forms.
    lent_to = forms.
    out_dt = forms.
    until_dt = forms.
    billed = forms.
    reason = forms.

    last_name = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20)
    departure_date = forms.DateField(required=False)
