from django import forms
from dataclasses import fields

from accounts.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'] = forms.CharField(widget=forms.PasswordInput)


class AgentForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'] = forms.CharField(widget=forms.PasswordInput)


class CreateOrganizationForm(forms.Form):
    name = forms.CharField(max_length=255)
    address = forms.CharField(required=False)
    phone = forms.IntegerField(required=False)
    description = forms.CharField(required=False)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class AgentProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'organization', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(AgentProfileForm, self).__init__(*args, **kwargs)
        self.fields['organization'].widget.attrs['disabled'] = True

    def clean_organization(self):
        return self.cleaned_data['organization']


