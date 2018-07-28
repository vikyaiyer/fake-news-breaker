from django.db import models

# Create your models here.
class News_Info(models.Model):
    news_id = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    url = models.CharField(max_length=500)
    source = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    publishedAt = models.CharField(max_length=100)
    urlToImage = models.CharField(max_length=500)
    score = models.IntegerField()
    user_upvotes = models.IntegerField()
    user_downvotes = models.IntegerField()
    expert_upvotes = models.IntegerField()
    expert_downvotes = models.IntegerField()

class News_Tags(models.Model):
    news_id = models.CharField(max_length=50)
    tags = models.CharField(max_length=500)

class User_Upvotes_Data(models.Model):
    news_id = models.CharField(max_length=50)
    username = models.CharField(max_length=50)

class User_Downvotes_Data(models.Model):
    news_id = models.CharField(max_length=50)
    username = models.CharField(max_length=50)

class Expert_Upvotes_Data(models.Model):
    news_id = models.CharField(max_length=50)
    username = models.CharField(max_length=50)

class Expert_Downvotes_Data(models.Model):
    news_id = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
