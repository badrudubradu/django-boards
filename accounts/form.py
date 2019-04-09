from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    email = forms.CharField(widget=forms.EmailInput(),
    max_length=254,
    required=True,
    help_text='Maximum length is 250 characters.')

    class Meta:
        model = User
        fields = ['username','email','password1','password2']
