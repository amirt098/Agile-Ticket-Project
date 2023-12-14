from django import forms
from dataclasses import fields


def create_dataclass_form(data_class):
    class DataClassForm(forms.Form):
        data_class_fields = fields(data_class)

        for field in data_class_fields:
            field_name = field.name
            field_type = field.type

            if field_name =='password':
                form_field = forms.CharField(widget=forms.PasswordInput)
            elif field_type == str:
                form_field = forms.CharField(max_length=255, required=field.default is None)
            elif field_type == int:
                form_field = forms.IntegerField(required=field.default is None)
            elif field_type == bool:
                form_field = forms.BooleanField(required=field.default is None)
            elif field_type == list:
                form_field = forms.MultipleChoiceField(
                    choices=[(value, value) for value in field.default],
                    required=field.default is None
                )
            else:
                form_field = forms.CharField(required=field.default is None)

            if field_type != list:

                form_field.initial = field.default

            locals()[field_name] = form_field

    return DataClassForm


class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)


class CreateAgentForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    organization = forms.CharField()  # Assuming organization is a CharField in the form
    role_name = forms.CharField(required=False)
    role_description = forms.CharField(required=False)


class CreateOrganizationForm(forms.Form):
    name = forms.CharField(max_length=255)
    address = forms.CharField(required=False)
    phone = forms.IntegerField(required=False)
    description = forms.CharField(required=False)
