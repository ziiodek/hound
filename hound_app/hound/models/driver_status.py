from django.db import  models
from django.forms import ModelForm
from django import forms
from .driver import Driver
from .user import User
from datetime import datetime

class DriverStatus(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    id = models.AutoField(blank=True, null=True, auto_created=True, primary_key=True)
    id_driver = models.OneToOneField(Driver, on_delete=models.CASCADE,blank=True,null=True)
    assigned_id = models.IntegerField(blank=True, default=0)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    leave_reason = models.TextField(blank=True,default='')
    expired = models.BooleanField(default=False)

    def __str__(self):
        attributes = []
        for attribute in self._meta.get_fields():
            attributes.append(getattr(self,str(attribute),''))
        return ' '.join(attributes)

class DriverStatusForm(ModelForm):
    class Meta:
        model = DriverStatus
        exclude = ['user_id','assigned_id']

class StartDate(ModelForm):
    start_date = forms.DateField(required=False)
    class Meta:
        model = DriverStatus
        fields = ['start_date']