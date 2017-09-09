from django.db import models
from django.forms import ModelForm
from .user import User
from django import forms
import django_tables2 as tables
import datetime

class Vehicle(models.Model):
    year = []

    for y in range(1900, int((datetime.datetime.now().year + 20))):
        year.append((y, y))

    user_id = models.ForeignKey( User, on_delete=models.CASCADE )
    id = models.AutoField(blank=True, null=True, auto_created=True, primary_key=True)
    economic_no = models.IntegerField(default=0,blank=True)
    vin = models.CharField(max_length=17,blank=True,default='')
    plate_no = models.CharField(max_length=10,blank=True,default='')
    country = models.CharField(max_length=10, blank=True,default = '')
    state = models.CharField(max_length=20,blank=True,default='')
    year = models.IntegerField(default=0,blank=True,choices=year,null=True)
    model = models.CharField(max_length=30,blank=True,default='')
    brand = models.CharField(max_length=30,blank=True,default='')
    type = models.CharField(max_length=20,blank=True,default='')
    active= models.BooleanField(default=True)
    status = models.CharField(max_length=35, blank=True, default='')
    profile_img = models.CharField(max_length=100, blank=True, default="hound/images/default.jpg")

    def save(self, *args, **kwargs):
        self.vin = self.vin.upper()
        self.plate_no = self.plate_no.upper()
        self.country = self.country.upper()
        self.state = self.state.lower()
        self.model = self.model.upper()
        self.brand = self.brand.upper()
        self.type = self.type.lower()
        super(Vehicle, self).save(*args, **kwargs)

class SearchVehicleForm(ModelForm):
    country = (('',''),('USA', 'USA'), ('MX', 'MX'))

    economic_no = forms.IntegerField(widget=forms.TextInput,required=False)
    country_select = forms.ChoiceField(required=False,widget=forms.Select ,choices=country,initial='')
    class Meta:
        model=Vehicle
        exclude=['economic_no','user_id','profile_img']

class VehicleForm(ModelForm):
    usa = (('',''),('Alabama', 'AL,Alabama'),
           ('Alaska', 'AK,Alaska'),
           ('Arizona', 'AZ,Arizona'),
           ('Arkansas','AR,Arkansas'),
           ('California', 'CA,California'),
           ('Colorado', 'CO,Colorado'),
           ('Connecticut','CT, Connecticut'),
           ('Delaware', 'DE,Delaware'),
           ('Dist. of Columbia', 'DC,Dist. of Columbia'),
           ('Florida', 'FL,Florida'),
           ('Georgia', 'GE,Georgia'),
           ('Hawaii', 'HI,Hawaii'),
           ('Idaho','ID,Idaho'),
           ('Illinois','IL,Illinois'),
           ('Indiana','IN,Indiana'),
           ('Iowa','IA,Iowa'),
           ('Kansas', 'KS,Kansas'),
           ('Kentucky','KY,Kentucky'),
           ('Louisiana', 'LA,Louisiana'),
           ('Maine', 'ME,Maine'),
           ('Maryland','MD,Maryland'),
           ('Massachusetts','MA,Massachusetts'),
           ('Michigan', 'MI,Michigan'),
           ('Minnesota', 'MN,Minnesota'),
           ('Mississippi', 'MS,Mississippi'),
           ('Montana', 'MT,Montana'),
           ('Nebraska','NE,Nebraska'),
           ('Nevada', 'NV,Nevada'),
           ('New Hampshire', 'NH,New Hampshire'),
           ('New Jersey', 'NJ,New Jersey'),
           ('New Mexico', 'NM,New Mexico'),
           ('New York','NY,New York'),
           ('North Carolina','NC,Noth Carolina'),
           ('North Dakota', 'ND,North Dakota'),
           ('Ohio', 'OH,Ohio'),
           ('Oklahoma', 'OK,Oklahoma'),
           ('Oregon','OR,Oregon'),
           ('Pennsylvania','PA,Pennsylvania'),
           ('Rhode Island','RI,Rhode Island'),
           ('South Carolina','SC,South Carolina'),
           ('South Dakota','SD,South Dakota'),
           ('Tennessee', 'TN,Tennessee'),
           ('Texas', 'TX,Texas'),
           ('Vermont', 'VT,Vermont'),
           ('Virginia', 'VA,Virginia'),
           ('Washington', 'WA,Washington'),
           ('West Virginia', 'WV,West Virginia'),
           ('Wisconsin', 'WI,Wisconsin'),
           ('Wyoming', 'WY,Wyoming'),
           )
    mx = (('',''),('Aguascalientes', 'AG,Aguascalientes'),
          ('Baja California', 'BC,Baja California'),
          ('Baja California Sur', 'BS,Baja California Sur'),
          ('Campeche', 'CM,Campeche'),
          ('Chiapas', 'CS,Chiapas'),
          ('Chihuahua', 'CH,Chihuahua'),
          ('Coahuila', 'CO,Coahuila'),
          ('Colima', 'CL,Colima'),
          ('Distrito Federal', 'DF,Distrito Federal'),
          ('Durango', 'DG,Durango'),
          ('Guanajuato', 'GT,Guanajuato'),
          ('Hidalgo', 'HG,Hidalgo'),
          ('Jalisco', 'JC,Jalisco'),
          ('Estado de México', 'ME,Estado de México'),
          ('Michoacán', 'MN,Michoacán'),
          ('Nayarit', 'NT,Nayarit'),
          ('Nuevo León', 'NL,Nuevo León'),
          ('Oaxaca', 'OC,Oaxaca'),
          ('Puebla', 'PL,Puebla'),
          ('Querétaro', 'QO,Querétaro'),
          ('Quintana Roo', 'QR,Quintana Roo'),
          ('San Luis Potosí', 'SP,San Luis Potosí'),
          ('Sinaloa', 'SL,Sinaloa'),
          ('Sonora', 'SR,Sonora'),
          ('Tabasco', 'TC,Tabasco'),
          ('Tamaulipas', 'TS,Tamaulipas'),
          ('Tlaxcala', 'TL,Tlaxcala'),
          ('Veracruz', 'VZ,Veracruz'),
          ('Yucatán', 'YN,Yucatán'),
          ('Zacatecas', 'ZS,Zacatecas'),
          )

    country = (('',''),('USA', 'USA'), ('MX', 'MX'))

    economic_no = forms.IntegerField(widget=forms.TextInput, required=False)
    states_usa = forms.ChoiceField(required=False, widget=forms.Select,choices=usa)
    states_mx = forms.ChoiceField(required=False,widget=forms.Select, choices=mx)
    country_select = forms.ChoiceField(required=False,widget=forms.Select ,choices=country,initial='')

    class Meta:
        model = Vehicle
        exclude=['user_id','profile_img']



class VehicleTable(tables.Table):
    select = tables.CheckBoxColumn(accessor = 'economic_no', attrs = { "th__input": {"onclick": "toggle(this)"}}, orderable=False)
    economic_no = tables.TemplateColumn('<a href=/view_vehicle/0/{{record.economic_no}}/>{{record.economic_no}}</a>')
    profile = tables.TemplateColumn('<center><img style="width:100px; height:100px; border-radius:100px;" src=/static/{{record.profile_img}} %}\' ></center>')
    class Meta:
        model = Vehicle
        sequence=('profile','economic_no')
        fields=('economic_no','vin','plate_no','country','state','year','model','brand','type','status')
        exclude=('user_id','profile_img','id')


class VehicleTable_esp(tables.Table):
    select = tables.CheckBoxColumn(accessor = 'economic_no', attrs = { "th__input": {"onclick": "toggle(this)"}}, orderable=False)
    no_económico = tables.TemplateColumn('<a href=/view_vehicle/1/{{record.economic_no}}/>{{record.economic_no}}</a>')
    perfil = tables.TemplateColumn('<center><img style="width:100px; height:100px; border-radius:100px;" src=/static/{{record.profile_img}} %}\' ></center>')
    vin = tables.TemplateColumn('{{record.vin}}')
    placas = tables.TemplateColumn('{{record.plate_no}}')
    país =  tables.TemplateColumn('{{record.country}}')
    estado =  tables.TemplateColumn('{{record.state}}')
    año =  tables.TemplateColumn('{{record.year}}')
    modelo =  tables.TemplateColumn('{{record.model}}')
    marca =  tables.TemplateColumn('{{record.brand}}')
    tipo =  tables.TemplateColumn('{{record.type}}')
    condición = tables.TemplateColumn('{{record.status}}')
    class Meta:
        model = Vehicle
        sequence=('perfil','no_económico','vin','placas','país','estado','año','modelo','marca','tipo','condición')
        exclude=('user_id','economic_no','plate_no','country','state','year','model','brand','type','active','profile_img','status','id')


