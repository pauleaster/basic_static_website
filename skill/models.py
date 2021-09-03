from django.db import models

# Create your models here.
class Skill(models.Model):
    title = models.CharField(max_length=30)
    summary = models.CharField(max_length=1000)


    def __str__(self):
     return self.title