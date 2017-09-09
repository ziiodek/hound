from django.db import models
from django.core.validators import MaxValueValidator
from .user import User
from .vehicle import Vehicle

class VehicleValidator(models.Model):
    user_id = models.ForeignKey( User, on_delete=models.CASCADE )
    id = models.AutoField(blank=True, null=True, auto_created=True, primary_key=True)
    economic_no = models.OneToOneField(Vehicle,on_delete=models.CASCADE)
    fuel = models.IntegerField(default=0,validators=[MaxValueValidator(100)])
    oil = models.IntegerField(default=0,validators=[MaxValueValidator(100)])
    water = models.IntegerField(default=0,validators=[MaxValueValidator(100)])
    miliage = models.IntegerField(default=0,validators=[MaxValueValidator(300)])