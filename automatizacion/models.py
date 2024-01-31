from ckeditor.fields import RichTextField
from django.db import models


# Create your models here.
class Prueba(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField()


class Mail(models.Model):
    de = models.CharField(max_length=100)
    asunto = models.CharField(max_length=200)
    cuerpo = RichTextField()
    leido = models.BooleanField(default=False)
