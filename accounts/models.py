from django.db import models

# Create your models here.
class UserData(models.Model):
    username = models.CharField(max_length=50)
    expert = models.IntegerField()
    rewards=models.IntegerField()
    tags = models.CharField(max_length=500)
