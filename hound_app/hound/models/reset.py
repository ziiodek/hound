from django.db import models
from django.forms import ModelForm
from django import forms
from datetime import datetime

class Reset(models.Model):
    token = models.CharField(primary_key=True,blank=False,max_length=8)
    email = models.EmailField(blank=False)

    @classmethod
    def create(cls, token,email):
        reset = cls(token=token,email=email)
        return reset

class ResetForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    retype = forms.CharField(widget=forms.PasswordInput(),required=True)
    tmp_token=forms.CharField(widget=forms.PasswordInput(),required=True)
    class Meta:
        model = Reset
        exclude=['email','token']

class ChangePasswordForm(ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput(),required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(),required=True)
    retype = forms.CharField(widget=forms.PasswordInput(), required=True)
    class Meta:
        model = Reset
        exclude=['email','token']