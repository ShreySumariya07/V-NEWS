from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class SavedNews(models.Model):
    us_id = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    id = models.AutoField(primary_key=True)
    abstract = models.CharField(max_length=500)
    web_url = models.URLField()
    image_url = models.URLField()
    title = models.CharField(max_length=300)
    published_date = models.CharField(max_length= 400)

    def __str__(self):
        return self.title