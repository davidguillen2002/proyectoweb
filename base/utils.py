from decimal import Decimal

MICRONUTRIENTES_ESENCIALES = [
    'Vitamina C',
    'Vitamina D',
    'Vitamina B12',
    'Calcio',
    'Hierro',
    'Magnesio',
    'Zinc',
    'Omega 3',
]

# Necesidades diarias de micronutrientes importantes (la lista es ajustable según las necesidades del proyecto)
NECESIDADES_MICRONUTRIENTES_ESPECIFICOS = {
    'Vitamina C': 90.0,  # mg
    'Vitamina D': 15.0,  # mcg
    'Vitamina B12': 2.4,  # mcg
    'Calcio': 1000.0,  # mg
    'Hierro': 18.0,  # mg
    'Magnesio': 400.0,  # mg
    'Zinc': 11.0,  # mg
    'Omega 3': 1.2, #mg
}


def calcular_bmr(perfil):
    peso = float(perfil.peso)  # Convertimos a float
    altura = float(perfil.altura) * 100  # Convertimos la altura a cm
    edad = perfil.edad

    if perfil.sexo == 'Hombre':
        bmr = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
    else:
        bmr = (10 * peso) + (6.25 * altura) - (5 * edad) - 161

    return round(bmr, 2)
def calcular_necesidades_nutricionales(perfil):
    bmr = calcular_bmr(perfil)
    # Asumimos un factor de actividad sedentario por defecto
    factor_actividad = 1.2

    # Ajustar el factor según el nivel de actividad del perfil
    if perfil.nivel_actividad == 'ligera':
        factor_actividad = 1.375
    elif perfil.nivel_actividad == 'moderada':
        factor_actividad = 1.55
    elif perfil.nivel_actividad == 'intensa':
        factor_actividad = 1.725
    elif perfil.nivel_actividad == 'muy intensa':
        factor_actividad = 1.9

    calorias_mantenimiento = bmr * factor_actividad

    # Las distribuciones recomendadas de macronutrientes son aproximadamente:
    # Proteínas: 10-35% del total de calorias.
    # Carbohidratos: 45-65% del total de calorias.
    # Grasas: 20-35% del total de calorias.

    # Estas cifras pueden variar según las fuentes y necesidades individuales, pero sirven como guía general.
    proteinas = (calorias_mantenimiento * 0.15) / 4
    carbohidratos = (calorias_mantenimiento * 0.55) / 4
    grasas = (calorias_mantenimiento * 0.3) / 9

    return {
        'calorias': round(calorias_mantenimiento, 2),
        'proteinas': round(proteinas, 2),
        'carbohidratos': round(carbohidratos, 2),
        'grasas': round(grasas, 2)
    }

def analizar_ingesta_nutricional(registros, necesidades):
    total_calorias = 0.0
    total_proteinas = 0.0
    total_carbohidratos = 0.0
    total_grasas = 0.0

    micronutrientes_ingestidos = {}

    for registro in registros:
        total_calorias += float(registro.alimento.calorias)
        total_proteinas += float(registro.alimento.proteinas)
        total_carbohidratos += float(registro.alimento.carbohidratos)
        total_grasas += float(registro.alimento.grasas)

        for alimento_nutriente in registro.alimento.alimentonutriente_set.all():
            nutriente_nombre = alimento_nutriente.nutriente.nombre
            cantidad_nutriente = float(alimento_nutriente.cantidad) * float(registro.cantidad)
            micronutrientes_ingestidos[nutriente_nombre] = micronutrientes_ingestidos.get(nutriente_nombre, 0) + cantidad_nutriente

    # Calcular deficiencias o excesos
    calorias_deficit = necesidades['calorias'] - total_calorias
    proteinas_deficit = (necesidades['proteinas'] - total_proteinas) * 4
    carbohidratos_deficit = (necesidades['carbohidratos'] - total_carbohidratos) * 4
    grasas_deficit = (necesidades['grasas'] - total_grasas) * 9

    recomendaciones = []

    if calorias_deficit > 0:
        recomendaciones.append(f"Necesitas consumir {round(calorias_deficit,2)} calorias adicionales.")
    if proteinas_deficit > 0:
        recomendaciones.append(f"Necesitas consumir {round(proteinas_deficit,2)} calorias adicionales de proteínas.")
    if carbohidratos_deficit > 0:
        recomendaciones.append(f"Necesitas consumir {round(carbohidratos_deficit,2)} calorias adicionales de carbohidratos.")
    if grasas_deficit > 0:
        recomendaciones.append(f"Necesitas consumir {round(grasas_deficit,2)} calorias adicionales de grasas.")


    # Analizamos sólo los micronutrientes esenciales
    for nutriente, necesidad in NECESIDADES_MICRONUTRIENTES_ESPECIFICOS.items():
        ingesta_actual = micronutrientes_ingestidos.get(nutriente, 0)
        if ingesta_actual < necesidad:
            recomendaciones.append(f"Necesitas más {nutriente}. Considera agregar alimentos ricos en {nutriente} a tu dieta.")

    analisis = {
        'calorias_consumidas': round(total_calorias,2),
        'calorias_necesarias': round(necesidades['calorias'],2),
        'proteinas_consumidas': round(total_proteinas,2),
        'proteinas_necesarias': round(necesidades['proteinas'],2),
        'carbohidratos_consumidas': round(total_carbohidratos,2),
        'carbohidratos_necesarios': round(necesidades['carbohidratos'],2),
        'grasas_consumidas': round(total_grasas,2),
        'grasas_necesarias': round(necesidades['grasas'],2),
        'micronutrientes_consumidos': micronutrientes_ingestidos,
        'recomendaciones': recomendaciones
    }

    return analisis


def ha_cumplido_limites(analisis, necesidades):
    """
    Comprueba si el usuario ha alcanzado sus límites diarios de calorias, proteinas, carbohidratos y grasas.
    """
    for nutriente in ['calorias', 'proteinas', 'carbohidratos', 'grasas']:
        if analisis[f"{nutriente}_consumidas"] >= necesidades[nutriente]:
            return True
    return False

def esta_por_sobrepasar_limites(analisis, necesidades, alimento):
    """
    Comprueba si un alimento adicional haría que el usuario sobrepase o alcance sus límites diarios de calorias, proteinas, carbohidratos y grasas..
    """
    # Considera la cantidad del alimento para calcular el valor nutricional total
    cantidad = alimento.get('cantidad', 1)
    for nutriente in ['calorias', 'proteinas', 'carbohidratos', 'grasas']:
        valor_analisis = Decimal(analisis[f"{nutriente}_consumidas"])
        valor_alimento = Decimal(alimento.get(nutriente, 0))
        if valor_analisis + (valor_alimento * cantidad) > Decimal(necesidades[nutriente]):
            return True
    return False


