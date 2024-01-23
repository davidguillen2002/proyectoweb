from rest_framework import serializers
from .models import Alimento, Nutriente

class NutrienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutriente
        fields = '__all__'

class AlimentoSerializer(serializers.ModelSerializer):
    nutrientes = NutrienteSerializer(many=True, read_only=True)

    class Meta:
        model = Alimento
        fields = '__all__'
