from django.db import models
from django.forms import ModelForm
from django import forms
from datetime import datetime

class User(models.Model):
    user_id = models.CharField(primary_key=True,max_length=5)
    email = models.EmailField(blank=False)
    password = models.CharField(blank=False,max_length=512)
    name = models.CharField(blank=False,max_length=20)
    last_name = models.CharField(blank=False,max_length=20)
    company = models.CharField(blank=True, max_length=20,default='')
    active = models.BooleanField(default=True)
    payed = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    payment_date = models.DateField(null=True,blank=True)
    profile_img = models.CharField(blank=True, max_length=100, default="hound/images/default.jpg")

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.last_name = self.last_name.lower()
        self.company = self.company.lower()
        super(User, self).save(*args, **kwargs)

class EmailForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']

class PasswordForm(ModelForm):
    tmp_password = forms.CharField(widget=forms.PasswordInput(),max_length=20)
    class Meta:
        model = User
        exclude=['user_id','email','password','name','last_name','company','active','payed','payment_date']


class RegistrationForm(ModelForm):
    tmp_password = forms.CharField(widget=forms.PasswordInput(),max_length=20)
    retype = forms.CharField(widget=forms.PasswordInput(),max_length=20)
    class Meta:
        model = User
        exclude=['user_id','active','payed','payment_date','password']

class SettingsForm(ModelForm):
    class Meta:
        model = User
        exclude=['user_id','active','password','payed']

class ActivateForm(ModelForm):
    tmp_password = forms.CharField(widget=forms.PasswordInput(), max_length=20)
    class Meta:
        model = User
        fields=['email']