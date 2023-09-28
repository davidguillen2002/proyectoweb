from django.urls import path
from .views import ListaPendientes


urlpatterns = [path('', ListaPendientes.as_view(), name='pendientes')]