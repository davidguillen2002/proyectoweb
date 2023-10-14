from django.db import models
from django.contrib.auth.models import User

TIPOS_SINIESTRO = (
    ('accidente', 'Accidente de tránsito'),
    ('robo', 'Robo'),
    ('falla', 'Falla de fábrica')
)


class Vehiculo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    marca = models.CharField(max_length=200)
    modelo = models.CharField(max_length=200)
    año = models.IntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_siniestro = models.CharField(max_length=50, choices=TIPOS_SINIESTRO, default='accidente')

    def __str__(self):
        return f"{self.marca} {self.modelo}"


class FactorCotizacion(models.Model):
    año_desde = models.IntegerField()
    año_hasta = models.IntegerField()
    factor = models.DecimalField(max_digits=5, decimal_places=2)
    tipo_siniestro = models.CharField(max_length=50, choices=TIPOS_SINIESTRO, default='accidente')

    def __str__(self):
        return f"Factor para {self.año_desde}-{self.año_hasta} ({self.tipo_siniestro})"


class Cotizacion(models.Model):
    vehiculo = models.OneToOneField(Vehiculo, on_delete=models.CASCADE)
    valor_cotizado = models.DecimalField(max_digits=10, decimal_places=2)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cotización para {self.vehiculo.marca} {self.vehiculo.modelo}"






