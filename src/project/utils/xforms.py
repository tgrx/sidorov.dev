from typing import Iterable

from django import forms


def gen_textinput_admin_form(model_cls: type, model_field_names: Iterable[str]) -> type:
    class AdminFormWithTextInputs(forms.ModelForm):
        class Meta:
            model = model_cls
            fields = "__all__"
            widgets = {
                _field: forms.TextInput(attrs={"size": "100"})
                for _field in model_field_names
            }

    return AdminFormWithTextInputs
