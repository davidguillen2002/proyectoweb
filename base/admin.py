from django.contrib import admin
from .models import Alimento, RegistroDiario, PerfilNutricional, AlimentoNutriente, Nutriente

admin.site.register(Alimento)
admin.site.register(PerfilNutricional)
admin.site.register(RegistroDiario)
admin.site.register(AlimentoNutriente)
admin.site.register(Nutriente)
