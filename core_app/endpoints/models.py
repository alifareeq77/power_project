from django.db import models


# Create your models here.
class Esp(models.Model):
    status = models.CharField(max_length=3)

