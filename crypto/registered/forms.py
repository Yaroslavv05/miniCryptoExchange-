from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm, TextInput


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={"class": 'form-control'}))
    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={"class": 'form-control'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": 'form-control'}))
    password2 = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput(attrs={"class": 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
            }),
        }


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя:", widget=forms.TextInput(attrs={"class": 'form-control'}))
    password = forms.CharField(label="Пароль:", widget=forms.PasswordInput(attrs={"class": 'form-control'}))


class KYCForm(forms.Form):
    fio = forms.CharField(label="ФИО", widget=forms.TextInput(attrs={"class": 'form-control'}))
    phone_number = forms.CharField(label="Номер телефона", widget=forms.TextInput(attrs={"class": 'form-control'}))
    passport = forms.CharField(label="Паспорт", widget=forms.FileInput(attrs={'class': 'form-control'}))
