from django.db import models
from django.forms import ModelForm
from .user import User
from django import forms
import django_tables2 as tables
import datetime

class Trailer(models.Model):
    year = []


    for y in range(1900, int((datetime.datetime.now().year + 20))):
        year.append((y, y))

    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    id = models.AutoField(blank=True, null=True, auto_created=True, primary_key=True)
    economic_no = models.IntegerField( default=0,blank=True)
    plate_no = models.CharField( max_length=10,blank=True,default='')
    country = models.CharField(max_length=10,blank=True,default='')
    state = models.CharField(max_length=20,blank=True,default='')
    year = models.IntegerField(default=0,blank=True,null=True,choices=year)
    capacity =  models.IntegerField(default=0,blank=True,null=True)
    type = models.CharField(max_length=30,blank=True,default='')
    client_name = models.CharField(max_length=20,blank=True,default='')
    client_last_name = models.CharField(max_length=20, blank=True,default='')
    use = models.CharField(max_length=20,blank=True,default='')
    status = models.CharField(max_length=35,blank=True,default='')
    active = models.BooleanField(default=True)
    rent_date = models.DateField(blank=True,null=True)
    deliver_date = models.DateField(blank=True,null=True)
    start_service_date = models.DateField(blank=True,null=True)
    end_service_date = models.DateField(blank=True,null=True)
    profile_img = models.CharField(max_length=100,blank=True,default="hound/images/default.jpg")

    def save(self, *args, **kwargs):
        self.plate_no = self.plate_no.upper()
        self.country = self.country.upper()
        self.state = self.state.lower()
        self.type = self.type.lower()
        self.client_name = self.client_name.lower()
        self.client_last_name = self.client_last_name.lower()
        self.use = self.use.lower()
        self.status = self.status.lower()
        super(Trailer, self).save(*args, **kwargs)

class TrailerForm(ModelForm):
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
    economic_no = forms.IntegerField(widget=forms.TextInput,required=False)
    states_usa = forms.ChoiceField(required=False, widget=forms.Select,choices=usa)
    states_mx = forms.ChoiceField(required=False, widget=forms.Select,choices=mx)
    capacity = forms.IntegerField(widget=forms.TextInput,required=False)

    country = (('',''),('USA', 'USA'), ('MX', 'MX'))
    types = (('',''),('Flat Bed', 'Flat Bed'), ('Dry Van and Enclosed', 'Dry Van and Enclosed'),
             ('Refrigerated and Reefers', 'Refrigerated and Reefers'),('Lowboy', 'Lowboy'),
             ('Step Deck-Single Drop', 'Step Deck-Single Drop'),('Extendable Flatbed', 'Extendable Flatbed'),
             ('Stretch Single Drop Deck', 'Stretch Single Drop Deck'),('Stretch Double Drop', 'Stretch Double Drop'),
             ('Extendable Double Drop', 'Extendable Double Drop'),('Removable Gooseneck (RGN)', 'Removable Gooseneck (RGN)'),
             ('Stretch RGN', 'Stretch RGN'),('Conestoga', 'Conestoga'),
             ('Side Kit', 'Side Kit'),('Power', 'Power'),
             ('Specialized', 'Specialized')
             )


    country_select = forms.ChoiceField(required=False, widget=forms.Select, choices=country, initial='')

    type_select = forms.ChoiceField(required=False, widget=forms.Select, choices=types, initial='')

    class Meta:
        model = Trailer
        exclude=['user_id']

class SearchTrailerForm(ModelForm):
    country = (('',''),('USA', 'USA'), ('MX', 'MX'))
    economic_no = forms.IntegerField(widget=forms.TextInput,required=False)
    capacity = forms.IntegerField(widget=forms.TextInput,required=False)
    country_select = forms.ChoiceField(required=False, widget=forms.Select, choices=country, initial='')

    types = (('',''),('Flat Bed', 'Flat Bed'), ('Dry Van and Enclosed', 'Dry Van and Enclosed'),
                   ('Refrigerated and Reefers', 'Refrigerated and Reefers'), ('Lowboy', 'Lowboy'),
                   ('Step Deck-Single Drop', 'Step Deck-Single Drop'), ('Extendable Flatbed', 'Extendable Flatbed'),
                   ('Stretch Single Drop Deck', 'Stretch Single Drop Deck'),
                   ('Stretch Double Drop', 'Stretch Double Drop'),
                   ('Extendable Double Drop', 'Extendable Double Drop'),
                   ('Removable Gooseneck (RGN)', 'Removable Gooseneck (RGN)'),
                   ('Stretch RGN', 'Stretch RGN'), ('Conestoga', 'Conestoga'),
                   ('Side Kit', 'Side Kit'), ('Power', 'Power'),
                   ('Specialized', 'Specialized')
                   )

    type_select = forms.ChoiceField(required=False, widget=forms.Select, choices=types, initial='')
    class Meta:
        model = Trailer
        fields=['use','plate_no','status','year','state','capacity','client_name','client_last_name']



class TrailerTable(tables.Table):
    select = tables.CheckBoxColumn(accessor = 'economic_no', attrs = { "th__input": {"onclick": "toggle(this)"}}, orderable=False)
    economic_no = tables.TemplateColumn('<a href=/view_trailer/0/{{record.economic_no}}/>{{record.economic_no}}</a>')
    profile = tables.TemplateColumn('<center><img style="width:100px; height:100px; border-radius:100px;" src=/static/{{record.profile_img}} %}\' ></center>')
    class Meta:
        model = Trailer
        sequence=('profile','economic_no')
        fields=('economic_no','plate_no','country','state','year','capacity')
        exclude=('user_id','profile_img','id')


class TrailerTable_esp(tables.Table):
    select = tables.CheckBoxColumn(accessor = 'economic_no', attrs = { "th__input": {"onclick": "toggle(this)"}}, orderable=False)
    no_económico = tables.TemplateColumn('<a href=/view_trailer/1/{{record.economic_no}}/>{{record.economic_no}}</a>')
    perfil = tables.TemplateColumn('<center><img style="width:100px; height:100px; border-radius:100px;" src=/static/{{record.profile_img}} %}\' ></center>')
    placas = tables.TemplateColumn('{{record.plate_no}}')
    país = tables.TemplateColumn('{{record.country}}')
    estado = tables.TemplateColumn('{{record.state}}')
    año = tables.TemplateColumn('{{record.year}}')
    capacidad = tables.TemplateColumn('{{record.capacity}}')
    class Meta:
        model = Trailer
        sequence=('perfil','no_económico','placas','país','estado','año','capacidad')
        exclude=('user_id','profile_img','economic_no','plate_no','country','state','year','capacity','type',
                 'client_name','client_last_name','use','status','active','rent_date','deliver_date',
                 'start_service_date','end_service_date','id')
