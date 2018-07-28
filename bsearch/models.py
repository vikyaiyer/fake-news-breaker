from django.db import models

# Create your models here.
class SearchHistory(models.Model):
    queries = models.CharField(max_length=2000)
