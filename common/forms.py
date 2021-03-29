from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "email")


class ChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        labels: {
            'username': '이름',
            'password': '비밀번호',
            'password1': '비밀번호확인'

        }
