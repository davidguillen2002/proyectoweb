from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    Logueo,
    PaginaRegistro,
    main_page,
    agregar_alimento,
    registro_diario,
    perfil_nutricional,
    analisis_nutricional,
    listar_alimentos,
    editar_alimento,
    eliminar_alimento,
    sugerencias_alimentos,
    listar_usuarios_inactivos,
    listar_todos_alimentos,
    agregar_nutriente_a_alimento,
    agregar_nutriente,
    listar_nutrientes,
    editar_nutriente,
    eliminar_nutriente,
    editar_nutriente_de_alimento,
    eliminar_nutriente_de_alimento
)

urlpatterns = [
    path('', Logueo.as_view(), name='login'),
    path('registro/', PaginaRegistro.as_view(), name='registro'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('main_page/', main_page, name='main_page'),
    path('agregar_alimento/', agregar_alimento, name='agregar_alimento'),
    path('registro_diario/', registro_diario, name='registro_diario'),
    path('perfil_nutricional/', perfil_nutricional, name='perfil_nutricional'),
    path('analisis_nutricional/', analisis_nutricional, name='analisis_nutricional'),
    path('listar_alimentos/', listar_alimentos, name='listar_alimentos'),
    path('editar_alimento/<int:alimento_id>/', editar_alimento, name='editar_alimento'),
    path('eliminar_alimento/<int:alimento_id>/', eliminar_alimento, name='eliminar_alimento'),
    path('sugerencias_alimentos/', sugerencias_alimentos, name='sugerencias_alimentos'),
    path('listar-usuarios-inactivos/', listar_usuarios_inactivos, name='lista_usuarios_inactivos'),
    path('super/listar_todos_alimentos/', listar_todos_alimentos, name='listar_todos_alimentos'),
    path('super/agregar_nutriente_a_alimento/<int:alimento_id>/', agregar_nutriente_a_alimento,
         name='agregar_nutriente_a_alimento'),
    path('agregar_nutriente/', agregar_nutriente, name='agregar_nutriente'),
    path('listar_nutrientes/', listar_nutrientes, name='listar_nutrientes'),
    path('editar_nutriente/<int:nutriente_id>/', editar_nutriente, name='editar_nutriente'),
    path('eliminar_nutriente/<int:nutriente_id>/', eliminar_nutriente, name='eliminar_nutriente'),
    path('super/editar_nutriente_de_alimento/<int:alimento_id>/<int:relacion_id>/',
         editar_nutriente_de_alimento, name='editar_nutriente_de_alimento'),

    path('super/eliminar_nutriente_de_alimento/<int:alimento_id>/<int:relacion_id>/',
         eliminar_nutriente_de_alimento, name='eliminar_nutriente_de_alimento')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


