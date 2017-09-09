from django import forms
from django.db import models
from django.forms import ModelForm
import django_tables2 as tables
from .user import User

class Driver(models.Model):

    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    id = models.AutoField(blank=True, null=True, auto_created=True, primary_key=True)
    assigned_id = models.IntegerField(blank=True,default=0)
    name = models.CharField(blank=False,max_length=20)
    middle_name = models.CharField(blank=True,max_length=20)
    last_name = models.CharField(blank=False,max_length=20)
    date_of_birth = models.DateField(blank=True,null=True)
    country = models.CharField(blank=True,max_length=20,default='')
    state = models.CharField(blank=True,max_length=20,default='')
    city = models.CharField(blank=True,max_length=20,default='')
    email_address =  models.EmailField(blank=True)
    profile_img = models.CharField( blank=True, max_length=100, default="hound/images/default.jpg",verbose_name = 'Perfil')

    @classmethod
    def create(cls,assigned_id):
        driver = cls(assigned_id=assigned_id)
        return driver

    def __str__(self):
        attributes = []
        for attribute in self._meta.get_fields():
            attributes.append(getattr(self,str(attribute),''))
        return ' '.join(attributes)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.middle_name = self.middle_name.lower()
        self.last_name = self.last_name.lower()
        self.country = self.country.upper()
        self.state = self.state.upper()
        self.city = self.city.lower()
        super(Driver, self).save(*args, **kwargs)



class DriverForm(ModelForm):
    assigned_id = forms.IntegerField(widget=forms.TextInput,required=False)
    class Meta:
        model = Driver
        exclude=['user_id']


class DriverTable(tables.Table):
    select = tables.CheckBoxColumn(accessor = 'assigned_id', attrs = { "th__input": {"onclick": "toggle(this)"}}, orderable=False)
    assigned_id = tables.TemplateColumn('<a href=/view_driver/0/{{record.assigned_id}}/>{{record.assigned_id}}</a>')
    profile = tables.TemplateColumn('<center><img style="width:100px; height:100px; border-radius:100px;" src=/static/{{record.profile_img}} %}\' ></center>')

    class Meta:
        model = Driver
        sequence=('profile','assigned_id')
        exclude=('user_id','profile_img','id','email_address')


class DriverTable_esp(tables.Table):
    select = tables.CheckBoxColumn(accessor = 'assigned_id', attrs = { "th__input": {"onclick": "toggle(this)"}}, orderable=False)
    id_asignado = tables.TemplateColumn('<a href=/view_driver/1/{{record.assigned_id}}/>{{record.assigned_id}}</a>')
    perfil = tables.TemplateColumn('<center><img style="width:100px; height:100px; border-radius:100px;" src=/static/{{record.profile_img}} %}\' ></center>')
    nombre = tables.TemplateColumn('{{record.name}}')
    apellido = tables.TemplateColumn('{{record.last_name}}')
    segundo_nombre = tables.TemplateColumn('{{record.middle_name}}')
    nació = tables.TemplateColumn('{{record.date_of_birth}}')
    país = tables.TemplateColumn('{{record.country}}')
    estado = tables.TemplateColumn('{{record.state}}')
    ciudad = tables.TemplateColumn('{{record.city}}')

    class Meta:
        model = Driver
        sequence=('perfil','id_asignado','nombre','segundo_nombre','apellido','nació','país','estado','ciudad')
        exclude=('user_id','assigned_id','profile_img','name','last_name','middle_name','date_of_birth','country','state','city','id','email_address')



class Name(ModelForm):
    name = forms.CharField(required=False)
    class Meta:
        model = Driver
        fields = ['name']

class LastName(ModelForm):
    last_name = forms.CharField(required=False)
    class Meta:
        model = Driver
        fields=['last_name']

class Country(ModelForm):
    country = forms.CharField(required=False)
    class Meta:
        model = Driver
        fields=['country']

class AssignedId(ModelForm):
    assigned_id = forms.IntegerField(widget=forms.TextInput(),required=False)
    name = forms.CharField(required=False)

    class Meta:
        model = Driver
        fields = ['name']


