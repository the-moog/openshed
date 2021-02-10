from django import forms

class DynamicModelChoiceField(forms.ModelChoiceField):
    """
    :param display_field: The name of the attribute of a queryset object to display in the selection list
    """

    def __init__(self, display_field='name', *args, **kwargs):
        self.display_field = display_field

        super().__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        return getattr(obj, self.display_field)
