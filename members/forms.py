from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Member


class MemberForm(UserCreationForm):

    class Meta:
        model = Member
        fields = ("username", "first_name", "last_name", "email")


class MemberEditForm(UserChangeForm):

    class Meta:
        model = Member
        fields = ("username", "first_name", "last_name", "email", "departure_date")