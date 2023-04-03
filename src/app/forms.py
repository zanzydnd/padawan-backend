from django import forms
from django.forms import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password

User = get_user_model()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=True, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    def save(self, commit=True):
        if self.cleaned_data.get("password1") != self.cleaned_data.get("password2"):
            raise Exception

        return self.Meta.model.objects.create(
            first_name=self.cleaned_data.get("first_name"),
            last_name=self.cleaned_data.get("last_name"),
            email=self.cleaned_data.get("email"),
            password=make_password(self.cleaned_data.get("password1"))
        )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]


class SubmitAssignmentForm(forms.Form):
    url = forms.URLField(required=True)

    class Meta:
        fields = ("url",)
