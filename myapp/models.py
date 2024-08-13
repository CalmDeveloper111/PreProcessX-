from django.db import models

# Create your models here.

class datasets(models.Model) :
    name = models.CharField(max_length=50 ,null=True)
    file = models.FileField(upload_to="files/")
