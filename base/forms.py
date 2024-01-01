from django import forms
from .models import Alimento, RegistroDiario, PerfilNutricional, AlimentoNutriente, Nutriente
from django.core.exceptions import ValidationError

class AlimentoForm(forms.ModelForm):
    class Meta:
        model = Alimento
        fields = ['nombre', 'calorias', 'proteinas', 'carbohidratos', 'grasas', 'descripcion', 'imagen']  # Esto incluirá todos los campos del modelo en el formulario

    def clean_calorias(self):
        data = self.cleaned_data['calorias']
        if data < 0:
            raise ValidationError("Las calorías no pueden ser negativas.")
        return data

    def clean_proteinas(self):
        data = self.cleaned_data['proteinas']
        if data < 0:
            raise ValidationError("Las proteínas no pueden ser negativas.")
        return data

    def clean_grasas(self):
        data = self.cleaned_data['grasas']
        if data < 0:
            raise ValidationError("Las grasas no pueden ser negativas.")
        return data

    def clean_carbohidratos(self):
        data = self.cleaned_data['carbohidratos']
        if data < 0:
            raise ValidationError("Los carbohidratos no pueden ser negativos.")
        return data

class RegistroDiarioForm(forms.ModelForm):
    class Meta:
        model = RegistroDiario
        fields = '__all__'
        exclude = ['usuario']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(RegistroDiarioForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['alimento'].queryset = Alimento.objects.filter(usuario=user)


class PerfilNutricionalForm(forms.ModelForm):
    class Meta:
        model = PerfilNutricional
        fields = ['edad', 'sexo', 'peso', 'altura', 'nivel_actividad']

    def clean_edad(self):
        edad = self.cleaned_data.get("edad")
        if edad < 0 or edad > 150:  # Valida que la edad sea razonable
            raise ValidationError("Por favor, ingresa una edad válida.")
        return edad

    def clean_peso(self):
        peso = self.cleaned_data.get("peso")
        if peso < 10 or peso > 500:  # Valida que el peso sea razonable
            raise ValidationError("Por favor, ingresa un peso válido.")
        return peso

    def clean_altura(self):
        altura = self.cleaned_data.get("altura")
        if altura < 0.5 or altura > 3.0:  # Valida que la altura sea razonable
            raise ValidationError("Por favor, ingresa una altura válida.")
        return altura


class NutrienteForm(forms.ModelForm):
    class Meta:
        model = Nutriente
        fields = '__all__'


class AlimentoNutrienteForm(forms.ModelForm):
    class Meta:
        model = AlimentoNutriente
        fields = '__all__'
        exclude = ['alimento']
