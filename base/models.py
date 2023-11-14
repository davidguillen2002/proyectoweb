from django.db import models
from django.contrib.auth.models import User
from datetime import date

NIVEL_ACTIVIDAD_CHOICES = [
    ('sedentario', 'Sedentario'),
    ('ligero', 'Ligero'),
    ('moderado', 'Moderado'),
    ('intenso', 'Intenso'),
    ('muy_intenso', 'Muy Intenso'),
]

# Modelo Nutriente
class Nutriente(models.Model):
    TIPO_CHOICES = [
        ('vitamina', 'Vitamina'),
        ('mineral', 'Mineral'),
    ]
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=8, choices=TIPO_CHOICES)

    def __str__(self):
        return self.nombre

class Alimento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Added this line to associate each food item with a user.
    nombre = models.CharField(max_length=255)
    calorias = models.DecimalField(max_digits=6, decimal_places=2)
    proteinas = models.DecimalField(max_digits=6, decimal_places=2)
    carbohidratos = models.DecimalField(max_digits=6, decimal_places=2)
    grasas = models.DecimalField(max_digits=6, decimal_places=2)
    descripcion = models.TextField(null=True, blank=True)
    imagen = models.ImageField(upload_to='alimentos_imagenes/', null=True, blank=True)
    nutrientes = models.ManyToManyField(Nutriente, through='AlimentoNutriente')  # Relación ManyToMany agregada

    def __str__(self):
        return self.nombre

# Modelo intermedio AlimentoNutriente
class AlimentoNutriente(models.Model):
    alimento = models.ForeignKey(Alimento, on_delete=models.CASCADE)
    nutriente = models.ForeignKey(Nutriente, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=6, decimal_places=2)
    unidad = models.CharField(max_length=20)  # ej: mg, mcg, UI...

    def __str__(self):
        return f"{self.alimento.nombre} - {self.nutriente.nombre}"

class PerfilNutricional(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    edad = models.PositiveIntegerField()
    sexo = models.CharField(max_length=10, choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer')])
    peso = models.DecimalField(max_digits=6, decimal_places=2)
    altura = models.DecimalField(max_digits=6, decimal_places=2)
    nivel_actividad = models.CharField(max_length=50, choices=NIVEL_ACTIVIDAD_CHOICES)

    def __str__(self):
        return self.usuario.username

class RegistroDiario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    alimento = models.ForeignKey(Alimento, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    cantidad = models.DecimalField(max_digits=6, decimal_places=2)  # Puede ser por gramos, porciones, etc.

    def __str__(self):
        return f"{self.usuario.username} - {self.alimento.nombre} - {self.fecha}"


