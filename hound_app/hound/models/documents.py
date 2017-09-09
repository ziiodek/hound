from django.db import models
from django import forms
from django.forms import ModelForm
from django import forms
from .user import User
from .driver import Driver

class Documents(models.Model):
    user_id = models.ForeignKey( User, on_delete=models.CASCADE )
    id_documents = models.AutoField(blank=True, null=True, auto_created=True, primary_key=True)
    id_driver = models.OneToOneField(Driver, on_delete=models.CASCADE,blank=True,null=True)
    assigned_id = models.IntegerField(blank=True, default=0)
    id = models.CharField(blank=True,max_length=20,default='')
    rfc = models.CharField(blank=True,max_length=10,default='')
    curp = models.CharField(blank=True,max_length=18,default='')
    license_no = models.CharField(blank=True,max_length=20,default='')
    license_issue_date = models.DateField(null=True,blank=True)
    license_exp_date = models.DateField(null=True,blank=True)
    license_type = models.CharField(blank=True,max_length=10,default='')
    passport_no = models.CharField(blank=True,max_length=30,default='')
    passport_issue_date = models.DateField(null=True,blank=True)
    passport_exp_date = models.DateField(null=True,blank=True)
    dot = models.BooleanField(default=False)
    criminal_record = models.BooleanField(default=False)
    prints_img = models.CharField(blank=True, max_length=100, default="hound/images/default.jpg")

    def save(self, *args, **kwargs):
        self.id = self.id.upper()
        self.rfc = self.rfc.upper()
        self.curp = self.curp.upper()
        self.license_no = self.license_no.upper()
        self.license_type = self.license_type.upper()
        self.passport_no = self.passport_no.upper()
        super(Documents, self).save(*args, **kwargs)

class DocumentsForm(ModelForm):
    id = forms.CharField(required=False)
    rfc = forms.CharField(required=False)
    curp = forms.CharField(required=False)
    class Meta:
        model = Documents
        exclude=['user_id','assigned_id','profile_img','finger_prints_img','id_documents']


class Id(ModelForm):
    id = forms.CharField(required=False)
    class Meta:
        model = Documents
        fields = ['id']

class RFC(ModelForm):
    rfc = forms.CharField(required=False)
    class Meta:
        model = Documents
        fields = ['rfc']