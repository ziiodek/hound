from django.db import models
from django.forms import ModelForm
import django_tables2 as tables
from .user import User
from .driver import Driver

class Directory(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.AutoField(blank=True, null=True, auto_created=True, primary_key=True)
    assigned_id = models.IntegerField(default=0,blank=False)
    phone_number = models.CharField(blank=False, null=True, max_length=20)

    def __str__(self):
        attributes = []
        for attribute in self._meta.get_fields():
            attributes.append(getattr(self,str(attribute),''))
        return ' '.join(attributes)

class DirectoryForm(ModelForm):
    class Meta:
        model = Directory
        exclude = ['id','user_id','assigned_id']

class DirectoryTable(tables.Table):
    phone_number = tables.TemplateColumn('<a href=/edit_directory/0/{{record.assigned_id}}/{{record.pk}}/>{{record.phone_number}}</a>')
    select_numbers = tables.CheckBoxColumn(accessor = 'pk', attrs = { "th__input": {"onclick": "toggle_date(this)"}}, orderable=False)
    class Meta:
        model = Directory
        exclude = ('id','user_id','assigned_id')

class DirectoryTableEsp(tables.Table):
    teléfono = tables.TemplateColumn('<a href=/edit_directory/1/{{record.assigned_id}}/{{record.pk}}/>{{record.phone_number}}</a>')
    select_numbers = tables.CheckBoxColumn(accessor = 'pk', attrs = { "th__input": {"onclick": "toggle_date(this)"}}, orderable=False)
    class Meta:
        model = Directory
        exclude = ('assigned_id','id','user_id','phone_number')

