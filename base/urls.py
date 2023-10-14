from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    Logueo,
    PaginaRegistro,
    listar_eliminar_usuarios,
    CotizacionView,
    ListaCotizaciones
)

urlpatterns = [
    path('', Logueo.as_view(), name='login'),
    path('registro/', PaginaRegistro.as_view(), name='registro'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('cotizar/', CotizacionView.as_view(), name='cotizar'),
    path('mis-cotizaciones/', ListaCotizaciones.as_view(), name='lista_cotizaciones'),
    path('listar-usuarios/', listar_eliminar_usuarios, name='lista_usuarios'),
]

