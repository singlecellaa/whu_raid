from django.db import models
from django.core.validators import MaxLengthValidator,MinLengthValidator

class User(models.Model):
    name = models.CharField(max_length=10)
    student_id = models.CharField(max_length=13,validators=[MaxLengthValidator(13),MinLengthValidator(13)])
    college = models.CharField(max_length=20)
    team = models.ForeignKey('Team',on_delete=models.SET_NULL,null=True,blank=True)
    
class Team(models.Model):
    name = models.CharField(max_length=10)
    leader_id = models.CharField(max_length=13,validators=[MaxLengthValidator(13),MinLengthValidator(13)])
    reservation_time = models.DateTimeField(null=True,blank=True)
    start_time = models.DateTimeField(null=True,blank=True)