from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import MemberForm, MemberEditForm
from .models import Member


class CustomUserAdmin(UserAdmin):
    add_form = MemberForm
    form = MemberEditForm
    model = Member
    list_display = ["email", "username", "first_name", "last_name"]


admin.site.register(Member, CustomUserAdmin)

