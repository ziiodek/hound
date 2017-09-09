from django.db import models
from django.core.validators import MaxValueValidator
from .user import User
from .driver import Driver

class VacationsDates(models.Model):
    user_id = models.ForeignKey( User, on_delete=models.CASCADE )
    assigned_id = models.OneToOneField( Driver, primary_key=True ,on_delete=models.CASCADE)
    year = models.IntegerField( default=1900, validators=[MaxValueValidator( 2100 )] )
    date = models.DateField