from django import forms
from django.contrib.auth.models import User
from . import models


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=50, widget=forms.PasswordInput, label='رمزعبور')
    password_confirm = forms.CharField(max_length=50, widget=forms.PasswordInput, label='تایید رمزعبور')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password_confirm(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_confirm']:
            raise forms.ValidationError("پسورد مطابقت ندارد")
        return cd['password_confirm']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class AccountEditForm(forms.ModelForm):
    class Meta:
        model = models.Account
        fields = ['bio', 'job', 'date_of_birth','photo']
