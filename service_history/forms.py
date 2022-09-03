from django import forms
from utilities.forms.fields import DynamicModelChoiceField
from items.models.category import Category
from .widgets import TimedeltaWidget
from .helpers import parse
import re
from django.core.exceptions import ValidationError


# class TimedeltaFormField(forms.Field):
#
#     default_error_messages = {
#         'invalid': 'Enter a valid time span: e.g. "3 days, 4 hours, 2 minutes"'
#     }
#
#     def __init__(self, *args, **kwargs):
#         defaults = {'widget': TimedeltaWidget}
#         defaults.update(kwargs)
#         super(TimedeltaFormField, self).__init__(*args, **defaults)
#
#     def clean(self, value):
#         """
#         This doesn't really need to be here: it should be tested in
#         parse()...
#
#         >>> t = TimedeltaFormField()
#         >>> t.clean('1 day')
#         datetime.timedelta(1)
#         >>> t.clean('1 day, 0:00:00')
#         datetime.timedelta(1)
#         >>> t.clean('1 day, 8:42:42.342')
#         datetime.timedelta(1, 31362, 342000)
#         >>> t.clean('3 days, 8:42:42.342161')
#         datetime.timedelta(3, 31362, 342161)
#         >>> try:
#         ...  t.clean('3 days, 8:42:42.3.42161')
#         ... except forms.ValidationError as arg:
#         ...  six.print_(arg.messages[0])
#         Enter a valid time span: e.g. "3 days, 4 hours, 2 minutes"
#         >>> t.clean('5 day, 8:42:42')
#         datetime.timedelta(5, 31362)
#         >>> t.clean('1 days')
#         datetime.timedelta(1)
#         >>> t.clean('1 second')
#         datetime.timedelta(0, 1)
#         >>> t.clean('1 sec')
#         datetime.timedelta(0, 1)
#         >>> t.clean('10 seconds')
#         datetime.timedelta(0, 10)
#         >>> t.clean('30 seconds')
#         datetime.timedelta(0, 30)
#         >>> t.clean('1 minute, 30 seconds')
#         datetime.timedelta(0, 90)
#         >>> t.clean('2.5 minutes')
#         datetime.timedelta(0, 150)
#         >>> t.clean('2 minutes, 30 seconds')
#         datetime.timedelta(0, 150)
#         >>> t.clean('.5 hours')
#         datetime.timedelta(0, 1800)
#         >>> t.clean('30 minutes')
#         datetime.timedelta(0, 1800)
#         >>> t.clean('1 hour')
#         datetime.timedelta(0, 3600)
#         >>> t.clean('5.5 hours')
#         datetime.timedelta(0, 19800)
#         >>> t.clean('1 day, 1 hour, 30 mins')
#         datetime.timedelta(1, 5400)
#         >>> t.clean('8 min')
#         datetime.timedelta(0, 480)
#         >>> t.clean('3 days, 12 hours')
#         datetime.timedelta(3, 43200)
#         >>> t.clean('3.5 day')
#         datetime.timedelta(3, 43200)
#         >>> t.clean('1 week')
#         datetime.timedelta(7)
#         >>> t.clean('2 weeks, 2 days')
#         datetime.timedelta(16)
#         >>> try:
#         ...  t.clean(six.u('2 we\xe8k, 2 days'))
#         ... except forms.ValidationError as arg:
#         ...  six.print_(arg.messages[0])
#         Enter a valid time span: e.g. "3 days, 4 hours, 2 minutes"
#         """
#
#         super(TimedeltaFormField, self).clean(value)
#         if (value == '' or value is None) and not self.required:
#             return ''
#         try:
#             return parse(value)
#         except TypeError:
#             raise forms.ValidationError(self.error_messages['invalid'])
#
#
# class xTimedeltaChoicesField(TimedeltaFormField):
#     def __init__(self, *args, **kwargs):
#         choices = kwargs.pop('choices')
#         defaults = {'widget': forms.Select(choices=choices)}
#         defaults.update(kwargs)
#         super(TimedeltaChoicesField, self).__init__(*args, **defaults)
#
#
# class xScheduleWidget(forms.MultiWidget):
#     template_name = r'service_history/interval_widget.html'
#
#     def __init__(self, attrs=None):
#         widgets = (
#             forms.RadioSelect(attrs, choices=[['d', "Days"], ['w', "Weeks"], ['m', "Months"], ['y', "Years"], ['o', "Other *"]]),
#             forms.TextInput(attrs)
#         )
#         super().__init__(widgets)
#
#     def decompress(self, value):
#         UNITS = "dwmy"
#         ret = {unit: None for unit in UNITS}
#         try:
#             units, value = value
#         except TypeError:
#             return ret
#
#         if units in UNITS:
#             return {units: value}
#
#         # Handle 'other' units
#         for unit in 'dwmy':
#             if unit in value:
#                 res = re.search(f"\[0-9]+{unit}", value)
#                 if not res:
#                     raise ValueError("How to handle this?")
#                 ret[unit] = value
#         return ret
#
#     #def get_context(self, name, value, attrs):
#     #    ctx = super().get_context(name, value, attrs)
#     #    return ctx
#
#     #def _get_context(self, name, value, attrs):
#     #    # First sub-widget doesn't get marked as required for some reason
#      #   self.widgets[0].is_required = attrs.get('required', False)
#     #    ctx = super().get_context(name, value, attrs)
#
#         # `get_context()` blindly copies the "required" HTML attribute from PhoneFormField to all of the sub-widget
#         # attrs. This is the opposite of the above problem, where "required" doesn't get set in the context.
#         # The text input for phone extension should always be optional. Not sure why Django isn't taking care of this.
#     #    ctx['widget']['subwidgets'][1]['attrs']['required'] = False
#     #    return ctx
#
#
# class xScheduleField(forms.MultiValueField):
#     widget = xScheduleWidget
#
#     def __init__(self, *args, **kwargs):
#         # Define one message for all fields.
#         error_messages = {
#             'required': 'This field is required.',
#         }
#
#         fields = [forms.Select, forms.CharField]
#
#         super().__init__(error_messages=error_messages,
#                          fields=fields, require_all_fields=True, *args, **kwargs)
#
#         # self.helper = FormHelper()
#         # self.helper.layout = Layout(
#         #
#         # )
#
#     def compress(self, data_list):
#         return " ".join(data_list)
#
#
# class xServiceScheduleForm(forms.Form):
#     interval = xScheduleField()
#     comment = forms.CharField(max_length=100)
#     category = DynamicModelChoiceField(queryset=Category.objects.all(), display_field='name')



class HorizontalRadioSelect(forms.RadioSelect):
    template_name = 'admin/horizontal_radios.html'
    option_template_name = 'admin/horizontal_inputs.html'

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)


class ServiceScheduleForm(forms.Form):
    INTERVAL_CHOICES = [['d', "Days"], ['w', "Weeks"], ['m', "Months"], ['y', "Years"]]#, ['o', "Other *"]]

    interval_type = forms.ChoiceField(choices=INTERVAL_CHOICES, widget=forms.RadioSelect)
    interval = forms.IntegerField()
    category = DynamicModelChoiceField(queryset=Category.objects.all(), display_field='name')
    comment = forms.CharField()

    class Meta:
        fields = ('interval_type', 'interval', 'category', 'comment')

        widgets = {
            'interval_type': HorizontalRadioSelect(attrs={'value': 'd'}),
            'interval': forms.TextInput(attrs={'placeholder': 'xx', 'value': '1'}),
            'category': forms.ChoiceField(),
            'comment': forms.TextInput(),
        }

    def clean(self):
        cleaned_data = super().clean()

        interval_type = cleaned_data.get("interval_type")

        if interval_type not in [i[0] for i in self.INTERVAL_CHOICES]:
            raise ValidationError("Invalid Interval Type")
