from django.db import  models
from django.forms import ModelForm
from django import forms
from .driver import Driver
from .user import User

class Phone(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    id = models.AutoField(blank=True, null=True, auto_created=True, primary_key=True)
    id_driver = models.OneToOneField(Driver, on_delete=models.CASCADE,blank=True,null=True)
    assigned_id = models.IntegerField(blank=True, default=0)
    ext = models.CharField(blank=True, null=True, max_length=8)
    phone_number = models.CharField(blank=True, null=True, max_length=15)

    def __str__(self):
        attributes = []
        for attribute in self._meta.get_fields():
            attributes.append(getattr(self,str(attribute),''))
        return ' '.join(attributes)

class PhoneForm(ModelForm):
    class Meta:
        model = Phone
        exclude = ['user_id','id','id_driver','assigned_id']