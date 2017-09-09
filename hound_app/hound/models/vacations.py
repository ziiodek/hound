import django_tables2 as tables
from django.db import models
from django.forms import ModelForm
from django import forms
from .user import User
from.driver import Driver
import datetime

class Vacations(models.Model):
    year = []
    coin = (('DLL','DLL'),('MXN','MXN'),)
    for y in range(1900, int((datetime.datetime.now( ).year + 20)) ):
        year.append( (y, y) )

    user_id = models.ForeignKey( User, on_delete=models.CASCADE )
    id_driver = models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True, null=True)
    assigned_id = models.IntegerField(blank=True, default=0)
    vacation_id = models.AutoField(blank=True,null=True,auto_created=True,primary_key=True)
    year = models.IntegerField(default=0,blank=False,choices=year)
    no_days = models.IntegerField(default=0,blank=False)
    payment_rate = models.IntegerField(default=0,blank=False)
    taken_days = models.IntegerField(default=0,blank=True,null=True)
    amount_payed = models.IntegerField(default=0,blank=False)
    payed = models.BooleanField(default=False,blank=True)
    exchange_rate = models.CharField(default='DLL',max_length=5,blank=False,choices=coin)

    def __str__(self):
        attributes = []
        for attribute in self._meta.get_fields( ):
            attributes.append( getattr( self, attribute, '' ) )
        return ' '.join( attributes )

class VacationsForm(ModelForm):
    no_days = forms.IntegerField(widget=forms.TextInput())
    payment_rate = forms.IntegerField(widget=forms.TextInput())
    amount_payed = forms.IntegerField(widget=forms.TextInput())
    class Meta:
        model = Vacations
        exclude = ['user_id','assigned_id','payed','taken_days']

class SearchVacationForm(ModelForm):
    class Meta:
        model = Vacations
        fields = ['year']


class VacationsTable(tables.Table):
    select = tables.CheckBoxColumn( accessor='pk', attrs={"td__input": {"onclick": "toggle_helper(this)"}}, orderable=False )
    class Meta:
        model = Vacations
        exclude=('vacation_id','user_id','assigned_id','id_driver')

class VacationsTable_esp(tables.Table):
    año = tables.TemplateColumn('{{record.year}}')
    no_dias = tables.TemplateColumn('{{record.no_days}}')
    tarifa_de_pago = tables.TemplateColumn('{{record.payment_rate}}')
    dias_usados = tables.TemplateColumn('{{record.taken_days}}')
    monto_pagado = tables.TemplateColumn('{{record.amount_payed}}')
    liquidado = tables.TemplateColumn('{{record.payed}}')
    tipo_de_cambio = tables.TemplateColumn('{{record.exchange_rate}}')
    select = tables.CheckBoxColumn(accessor='pk', attrs={"td__input": {"onclick": "toggle_helper(this)"}},orderable=False)
    class Meta:
        model = Vacations
        exclude=('vacation_id','user_id','assigned_id','year','no_days','payment_rate','taken_days','amount_payed','payed','exchange_rate','id_driver')



