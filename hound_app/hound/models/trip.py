import django_tables2 as tables
from django.db import models
from django.forms import ModelForm
from django import forms
from .user import User
from .driver import Driver
from .vehicle import Vehicle
from .trailer import Trailer
from datetime import datetime
from django.utils import timezone

class Trip(models.Model):
    status = (('CANCELED', 'CANCELED'), ('DELIVERED', 'DELIVERED'),('PENDING', 'PENDING'))

    user_id = models.ForeignKey( User, on_delete=models.CASCADE )
    trip_id = models.AutoField(blank=True, null=True, auto_created=True, primary_key=True)
    assigned_id = models.IntegerField(blank=True,default=0,null=True)
    vehicle_no = models.IntegerField(default=0,blank=True,null=True)
    trailer_no = models.IntegerField(blank=True,null=True)
    date = models.DateField(blank=False, default=timezone.now)
    start_time = models.TimeField(blank=True,default= timezone.now)
    end_time = models.TimeField(blank=True, default=timezone.now)
    origin = models.CharField(blank=False, max_length=35, default='')
    destiny = models.CharField(blank=False, max_length=35, default='')
    trip_type = models.CharField(blank=False, max_length=20, default='')
    status = models.CharField(max_length=10,default='PENDING',blank=True,choices=status)

    def __str__(self):
        attributes = []
        for attribute in self._meta.get_fields( ):
            attributes.append( getattr( self, attribute, '' ) )
        return ' '.join( attributes )

    def save(self, *args, **kwargs):
        self.origin = self.origin.lower()
        self.destiny = self.destiny.lower()
        self.trip_type = self.trip_type.lower()
        super(Trip, self).save(*args, **kwargs)

class TripForm(ModelForm):

    assigned_id = forms.IntegerField(widget=forms.TextInput())
    vehicle_no = forms.IntegerField(widget=forms.TextInput())
    trailer_no = forms.IntegerField(widget=forms.TextInput(),required=False)
    class Meta:
        model = Trip
        exclude = ['user_id','assigned_id','vehicle_no','trailer_no']

class SearchTripForm(ModelForm):
    assigned_id = forms.IntegerField(widget=forms.TextInput(),required=False)
    vehicle_no = forms.IntegerField(widget=forms.TextInput(),required= False)
    trailer_no = forms.IntegerField(widget=forms.TextInput(),required = False)
    origin = forms.CharField(required=False)
    destiny = forms.CharField(required=False)
    trip_type=forms.CharField(required=False)
    class Meta:
        model = Trip
        fields = ['origin','destiny','trip_type']

class SearchBitacoraForm(ModelForm):
    assigned_id = forms.IntegerField(widget=forms.TextInput(),required=False)
    vehicle_no = forms.IntegerField(widget=forms.TextInput(),required= False)
    trailer_no = forms.IntegerField(widget=forms.TextInput(),required = False)
    date = forms.DateField(required=False)
    origin = forms.CharField(required=False)
    destiny = forms.CharField(required=False)
    trip_type=forms.CharField(required=False)
    class Meta:
        model = Trip
        fields = ['origin','destiny','trip_type']


class TripTable(tables.Table):
    select = tables.CheckBoxColumn(accessor='pk', attrs={"th__input": {"onclick": "toggle(this)"}}, orderable=False)
    assigned_id = tables.TemplateColumn('<a href=/trip_status/0/{{record.pk}}/>{{record.assigned_id}}</a>')
    vehicle_no = tables.TemplateColumn('{{record.vehicle_no}}')
    trailer_no = tables.TemplateColumn('{{record.trailer_no}}')
    class Meta:
        model = Trip
        exclude=('user_id','trip_id')

class TripTable_esp(tables.Table):
    id_asignado = tables.TemplateColumn('<a href=/trip_status/1/{{record.pk}}/>{{record.assigned_id}}</a>')
    no_vehiculo = tables.TemplateColumn('{{record.vehicle_no}}')
    no_caja = tables.TemplateColumn('{{record.trailer_no}}')
    fecha = tables.TemplateColumn('{{record.date}}')
    salió = tables.TemplateColumn('{{record.start_time}}')
    llegó = tables.TemplateColumn('{{record.end_time}}')
    origen = tables.TemplateColumn('{{record.origin}}')
    destino = tables.TemplateColumn('{{record.destiny}}')
    tipo_de_viaje = tables.TemplateColumn('{{record.trip_type}}')
    estado = tables.TemplateColumn('{{record.status}}')
    select = tables.CheckBoxColumn(accessor='pk', attrs={"th__input": {"onclick": "toggle(this)"}}, orderable=False)
    class Meta:
        model = Trip
        exclude=('user_id','trip_id','assigned_id','vehicle_no','trailer_no','date','start_time','end_time',
                 'origin','destiny','trip_type','status')

class BitacoraTable(tables.Table):
    select = tables.CheckBoxColumn(accessor='pk', attrs={"th__input": {"onclick": "toggle(this)"}}, orderable=False)
    assigned_id = tables.TemplateColumn('<a href=/view_driver/0/{{record.assigned_id}}/>{{record.assigned_id}}</a>')
    vehicle_no = tables.TemplateColumn('<a href=/view_vehicle/0/{{record.vehicle_no}}/>{{record.vehicle_no}}</a>')
    trailer_no = tables.TemplateColumn('<a href=/view_trailer/0/{{record.trailer_no}}/>{{record.trailer_no}}</a>')
    class Meta:
        model = Trip
        exclude=('user_id','trip_id')


class BitacoraTable_esp(tables.Table):
    id_asignado = tables.TemplateColumn('<a href=/view_driver/1/{{record.assigned_id}}/>{{record.assigned_id}}</a>')
    no_vehiculo = tables.TemplateColumn('<a href=/view_vehicle/1/{{record.vehicle_no}}/>{{record.vehicle_no}}</a>')
    no_caja = tables.TemplateColumn('<a href=/view_trailer/1/{{record.trailer_no}}/>{{record.trailer_no}}</a>')
    fecha = tables.TemplateColumn('{{record.date}}')
    salió = tables.TemplateColumn('{{record.start_time}}')
    llegó = tables.TemplateColumn('{{record.end_time}}')
    origen = tables.TemplateColumn('{{record.origin}}')
    destino = tables.TemplateColumn('{{record.destiny}}')
    tipo_de_viaje = tables.TemplateColumn('{{record.trip_type}}')
    estado = tables.TemplateColumn('{{record.status}}')
    select = tables.CheckBoxColumn(accessor='pk', attrs={"th__input": {"onclick": "toggle(this)"}}, orderable=False)
    class Meta:
        model = Trip
        exclude = ('user_id', 'trip_id', 'assigned_id', 'vehicle_no', 'trailer_no', 'date', 'start_time', 'end_time',
                   'origin', 'destiny', 'trip_type', 'status')





