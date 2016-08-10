# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from users.models import User, UserProfile
from tweets.models import Tweet


class LoginForm(forms.Form):
    usr = forms.CharField(label='User name')
    pwd = forms.CharField(label='Password', widget=forms.PasswordInput())


class TweetForm(ModelForm):
    class Meta:
        model = Tweet
        fields = ['text']


class UserSignUpForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class UserProfileSignUpForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_nick', 'description', 'localization']
