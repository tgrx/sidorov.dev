from typing import Iterable
from typing import Optional

from django import forms
from django.db import models

from project.utils.xmodels import a


def gen_textinput_admin_form(
    model_cls: type, model_fields: Iterable[models.Field], size: Optional[int] = 100
) -> type:
    """
    Give me these:
    :param model - a model you want to be displayed in Django Admin
    :param model_fields: model fields you want to be displayed as textinput
    And I will generate and
    :return a ModelForm class
    """
    form_cls_name = f"{model_cls.__name__}AdminFormWithTextInputs"
    model_field_names = (a(_field) for _field in model_fields)
    size = size or 100
    widgets = {
        _field: forms.TextInput(attrs={"size": str(size)})
        for _field in model_field_names
    }

    form_cls = type(
        form_cls_name,
        (forms.ModelForm,),
        {
            "Meta": type(
                "Meta",
                (),
                {"model": model_cls, "fields": "__all__", "widgets": widgets,},
            )
        },
    )

    return form_cls
