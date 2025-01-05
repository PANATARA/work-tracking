from django import forms
from django.forms import ModelForm
from django.forms.widgets import Textarea


class CustomTextarea(Textarea):
    def __init__(self, attrs=None):
        default_attrs = {"cols": "79", "rows": "2"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class ImprovedModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.CharField):
                field.widget = CustomTextarea()
