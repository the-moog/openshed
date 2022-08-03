
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Member


class MemberForm(UserCreationForm):

    class Meta:
        model = Member
        fields = ("username", "first_name", "last_name", "email")


class MemberEditForm(UserChangeForm):

    class Meta:
        model = Member
        fields = ("username", "first_name", "last_name", "email", "departure_date")