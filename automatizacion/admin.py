from django.contrib import admin

from automatizacion.models import Prueba, Mail


# Register your models here.
@admin.register(Prueba)
class PruebaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'edad']
    search_fields = ['nombre', 'apellido', 'edad']
    list_filter = ['edad']


@admin.register(Mail)
class PruebaAdmin(admin.ModelAdmin):
    list_display = ['de', 'asunto', 'cuerpo']
    search_fields = ['de', 'asunto', 'cuerpo']
    list_filter = ['asunto']