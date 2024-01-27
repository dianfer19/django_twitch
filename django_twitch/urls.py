"""
URL configuration for django_twitch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from jobs.scheduler import start
urlpatterns = [
    path('admin/', admin.site.urls),
]

start()
#
# mail = 'dbajana@codeec.com.ec'
# print("Enviar Mail")
# context = {'usuario': 'Dianfer'}
# asunto = "Notificaciones Prueba"
# content = 'Hola'
# from_email = settings.EMAIL_HOST_USER
# print(from_email)
# to_email = {mail}
# to_cc = {}
# email = EmailMultiAlternatives(
#     asunto,
#     '',
#     from_email,
#     to_email,
#     cc=to_cc,
# )
# email.attach_alternative(content, 'text/html')
# email.send()