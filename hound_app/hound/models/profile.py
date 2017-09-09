from django import forms
from django.db import models
from django.forms import ModelForm

class Profile(models.Model):
    id = models.AutoField(blank=True, null=True, auto_created=True, primary_key=True)
    user_id = models.CharField(blank=True,max_length=5,default='none')
    profile = models.FileField(blank=True,null=True,default='/hound/images/default.jpg')
    path = models.CharField(max_length=100,blank=True,default='/hound/images/default.jpg')
    type=models.CharField(blank=True,max_length=10,default='none')
    gen_id = models.IntegerField(blank=True,null=True,default=0)

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields=['profile']
