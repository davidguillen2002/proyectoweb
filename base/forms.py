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

    # Hacer lo mismo para carbohidratos y grasas...
    # Continúa con esta lógica para otros campos que necesiten validación.

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


class NutrienteForm(forms.ModelForm):
    class Meta:
        model = Nutriente
        fields = '__all__'


class AlimentoNutrienteForm(forms.ModelForm):
    class Meta:
        model = AlimentoNutriente
        fields = '__all__'
        exclude = ['alimento']
