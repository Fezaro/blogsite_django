from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    """class represents log in details form"""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    """ class representing usser registration form"""
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class UserEditForm(forms.ModelForm):
    """class representing user edit form"""
    class Meta:
        model = User
        # user can edit these fields of their  registered account
        fields = ('first_name', 'last_name', 'email') 


class ProfileEditForm(forms.ModelForm):
    """class representing profile edit form"""
    class Meta:
        model = Profile
        # user can edit these profile data fields
        fields = ('role', 'photo')