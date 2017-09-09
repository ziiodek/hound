from django.db import models
from django.forms import ModelForm
from django import forms
from .driver import Driver
from .user import User

class Address(models.Model):

    user_id = models.ForeignKey( User, on_delete=models.CASCADE )
    id = models.AutoField(blank=True, null=True, auto_created=True, primary_key=True)
    id_driver = models.OneToOneField(Driver,on_delete=models.CASCADE,blank = True,null=True)
    assigned_id = models.IntegerField(blank=True,default=0)
    street = models.CharField(blank=True,max_length=60)
    country_addr = models.CharField(max_length=10, blank=True,default='')
    state_addr = models.CharField(blank=True,max_length=20,default='')
    city_addr = models.CharField(blank=True, max_length=20,default='')
    zip_code = models.IntegerField(blank=True,null=True,default=0)
    ext = models.CharField(blank=True,null=True,max_length=8)
    phone_number = models.CharField(blank=True,null=True,max_length=20)
    def save(self, *args, **kwargs):
        self.street = self.street.lower()
        self.country_addr = self.country_addr.upper()
        self.state_addr = self.state_addr.upper()
        self.city_addr = self.city_addr.lower()
        super(Address, self).save(*args, **kwargs)

class AddressForm(ModelForm):
    zip_code = forms.IntegerField(widget=forms.TextInput(),required=False)
    ext = forms.IntegerField(widget=forms.TextInput(),required=False)
    phone_number = forms.CharField(required=False)
    class Meta:
        model = Address
        exclude=['user_id','assigned_id']