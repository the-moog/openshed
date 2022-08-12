from django import forms
from phone_field import PhoneField as OldPhoneField
from phone_field import PhoneNumber


class DynamicModelChoiceField(forms.ModelChoiceField):
    """
    :param display_field: The name of the attribute of a queryset object to display in the selection list
    """

    def __init__(self, display_field='name', *args, **kwargs):
        self.display_field = display_field

        super().__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        return getattr(obj, self.display_field)


class PhoneField(OldPhoneField):
    # see GitHub
    def get_prep_value(self, value):
        if not value:
            # return ''
            return None

        if not isinstance(value, PhoneNumber):
            value = PhoneNumber(value)
        return value.cleaned

