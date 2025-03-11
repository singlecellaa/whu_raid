from django.db import models
from django.core.validators import MaxLengthValidator,MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class User(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length=10)
    student_id = models.CharField(max_length=13,validators=[MaxLengthValidator(13),MinLengthValidator(13)],unique=True)
    college = models.CharField(max_length=20)
    team = models.ForeignKey('Team',on_delete=models.SET_NULL,null=True,blank=True)
    USERNAME_FIELD = 'student_id'
    
class Team(models.Model):
    name = models.CharField(max_length=10)
    leader_id = models.CharField(max_length=13,validators=[MaxLengthValidator(13),MinLengthValidator(13)],unique=True)
    reservation_time = models.DateTimeField(null=True,blank=True)
    start_time = models.DateTimeField(null=True,blank=True)
    end_time = models.DateTimeField(null=True,blank=True)
    position = models.CharField(max_length=10,default='桂操')