from django.db import models
from django.forms import ModelForm
import django_tables2 as tables
from .vacations import Vacations
from datetime import datetime

class Date(models.Model):
    vacation_id = models.ForeignKey(Vacations,on_delete=models.CASCADE)
    date = models.DateField(blank=False,default=datetime.now)
    date_id = models.AutoField(null=True,primary_key=True)


    def __str__(self):
        attributes = []
        for attribute in self._meta.get_fields():
            attributes.append(getattr(self,str(attribute),''))
        return ' '.join(attributes)

class DateForm(ModelForm):
    class Meta:
        model = Date
        exclude = ['vacation_id']

class DateTable(tables.Table):
    select_dates = tables.CheckBoxColumn(accessor = 'pk', attrs = { "th__input": {"onclick": "toggle_date(this)"}}, orderable=False)
    class Meta:
        model = Date
        exclude = ('vacation_id','date_id')

class DateTable_esp(tables.Table):
    fecha = tables.TemplateColumn('{{record.date}}')
    select_dates = tables.CheckBoxColumn(accessor = 'pk', attrs = { "th__input": {"onclick": "toggle_date(this)"}}, orderable=False)
    class Meta:
        model = Date
        exclude = ('vacation_id','date_id','date')

