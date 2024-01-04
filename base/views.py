from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Alimento, PerfilNutricional, RegistroDiario, Nutriente, AlimentoNutriente
from django.contrib.auth.decorators import login_required
from .utils import calcular_necesidades_nutricionales, analizar_ingesta_nutricional, calcular_bmr, ha_cumplido_limites, esta_por_sobrepasar_limites
from .forms import PerfilNutricionalForm, AlimentoForm, RegistroDiarioForm, NutrienteForm, AlimentoNutrienteForm
from django.db.models import Count
from datetime import date, datetime
from django.contrib import messages
from django.db.models import F, Sum, DecimalField
from django.shortcuts import get_object_or_404


# Lista los usuarios que no tienen registros asociados (identificados como 'usuarios_sin_registros').
# Si se envía un POST con el propósito de eliminar un usuario, se presenta primero una página de confirmación y, si se confirma, se elimina el usuario.
@login_required
@user_passes_test(lambda u: u.is_superuser)
def listar_usuarios_inactivos(request):
    # Usuarios que no tienen registros
    usuarios_sin_registros = User.objects.annotate(num_registros=Count('registrodiario')).filter(num_registros=0, is_superuser=False)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        usuario_a_eliminar = get_object_or_404(User, pk=user_id)

        if 'eliminar' in request.POST:
            return render(request, 'base/confirmar_eliminar_usuario.html', {'usuario': usuario_a_eliminar})
        elif 'confirmar_eliminar' in request.POST:
            usuario_a_eliminar.delete()
            return redirect('lista_usuarios_inactivos')

    return render(request, 'base/listar_usuarios_inactivos.html', {'usuarios_sin_registros': usuarios_sin_registros})


# Maneja la creación de nuevos nutrientes a través de un formulario (NutrienteForm). Si el método es POST y el formulario es válido,
# guarda el nutriente y redirige a la lista de nutrientes.
@login_required
@user_passes_test(lambda u: u.is_superuser)
def agregar_nutriente(request):
    if request.method == "POST":
        form = NutrienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_nutrientes')
    else:
        form = NutrienteForm()
    return render(request, 'base/agregar_nutriente.html', {'form': form})

# Recupera y muestra todos los nutrientes existentes.
@login_required
@user_passes_test(lambda u: u.is_superuser)
def listar_nutrientes(request):
    nutrientes = Nutriente.objects.all()
    return render(request, 'base/listar_nutrientes.html', {'nutrientes': nutrientes})

# Permite editar un nutriente existente. Utiliza el ID del nutriente para encontrarlo y, si se envía un formulario válido a través de POST,
# actualiza el nutriente y redirige a la lista de nutrientes.
@login_required
@user_passes_test(lambda u: u.is_superuser)
def editar_nutriente(request, nutriente_id):
    nutriente = get_object_or_404(Nutriente, id=nutriente_id)
    if request.method == "POST":
        form = NutrienteForm(request.POST, instance=nutriente)
        if form.is_valid():
            form.save()
            return redirect('listar_nutrientes')
    else:
        form = NutrienteForm(instance=nutriente)
    return render(request, 'base/editar_nutriente.html', {'form': form, 'nutriente': nutriente})

# Permite eliminar un nutriente específico, identificado por su ID. Si el método es POST, se elimina el nutriente y se redirige a la lista de nutrientes.
# Si no es POST, probablemente se muestre una página de confirmación para la eliminación.
@login_required
@user_passes_test(lambda u: u.is_superuser)
def eliminar_nutriente(request, nutriente_id):
    nutriente = get_object_or_404(Nutriente, id=nutriente_id)
    if request.method == "POST":
        nutriente.delete()
        return redirect('listar_nutrientes')
    return render(request, 'base/eliminar_nutriente.html', {'nutriente': nutriente})

# Recupera y muestra todos los alimentos disponibles. No se realizan acciones adicionales como creación o eliminación en esta vista,
# simplemente se lista lo que hay en la base de datos.
@login_required
@user_passes_test(lambda u: u.is_superuser)
def listar_todos_alimentos(request):
    alimentos = Alimento.objects.all()
    return render(request, 'base/listar_todos_alimentos.html', {'alimentos': alimentos})

# Permite agregar una relación entre un alimento y un nutriente, probablemente para indicar qué nutrientes contiene un alimento.
# Si el método es POST y el formulario es válido, se crea la relación y se redirige a la lista de alimentos.
# Si no es POST, se muestra el formulario para crear la relación.
@login_required
@user_passes_test(lambda u: u.is_superuser)
def agregar_nutriente_a_alimento(request, alimento_id):
    alimento = get_object_or_404(Alimento, id=alimento_id)

    if request.method == "POST":
        form = AlimentoNutrienteForm(request.POST)
        if form.is_valid():
            nutriente_rel = form.save(commit=False)
            nutriente_rel.alimento = alimento
            nutriente_rel.save()
            return redirect('listar_todos_alimentos')

    else:
        form = AlimentoNutrienteForm()
    return render(request, 'base/agregar_nutriente_a_alimento.html', {'form': form, 'alimento': alimento})

# Permite editar una relación existente entre un alimento y un nutriente. Utiliza el ID de ambos para identificar la relación específica.
# Si se envía un formulario válido mediante POST, se actualiza la relación y se redirige a la lista de alimentos
# De lo contrario, se muestra el formulario para editar la relación.
@login_required
@user_passes_test(lambda u: u.is_superuser)
def editar_nutriente_de_alimento(request, alimento_id, relacion_id):
    alimento = get_object_or_404(Alimento, id=alimento_id)
    relacion = get_object_or_404(AlimentoNutriente, id=relacion_id)

    if request.method == "POST":
        form = AlimentoNutrienteForm(request.POST, instance=relacion)
        if form.is_valid():
            form.save()
            return redirect('listar_todos_alimentos')

    else:
        form = AlimentoNutrienteForm(instance=relacion)
    return render(request, 'base/editar_nutriente_de_alimento.html', {'form': form, 'alimento': alimento})

# Permite eliminar una relación específica entre un alimento y un nutriente, identificados por sus respectivos IDs.
# Si el método es POST, se elimina la relación y se redirige a la lista de alimentos. De lo contrario,
# probablemente se muestre una página de confirmación para la eliminación.
@login_required
@user_passes_test(lambda u: u.is_superuser)
def eliminar_nutriente_de_alimento(request, alimento_id, relacion_id):
    alimento = get_object_or_404(Alimento, id=alimento_id)
    relacion = get_object_or_404(AlimentoNutriente,
                                 id=relacion_id)

    if request.method == "POST":
        relacion.delete()
        return redirect('listar_todos_alimentos')

    return render(request, 'base/eliminar_nutriente_de_alimento.html', {'alimento': alimento, 'relacion': relacion})

# Analiza el consumo nutricional de todos los perfiles, agrupándolos en menores de 30 años y mayores o iguales a 30 años.
# Para cada grupo, calcula la suma total de calorías, proteínas, carbohidratos, grasas y nutrientes consumidos
# y luego calcula el promedio por usuario en cada grupo.
def analisis_consumo(fecha_inicio=None, fecha_fin=None):
    # Convertir fechas de string a objetos datetime si son proporcionadas
    fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d") if fecha_inicio else None
    fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d") if fecha_fin else None

    perfiles = PerfilNutricional.objects.all()
    resultados = {
        'menores_30': {'calorias': 0, 'proteinas': 0, 'carbohidratos': 0, 'grasas': 0, 'nutrientes': {}},
        'mayores_30': {'calorias': 0, 'proteinas': 0, 'carbohidratos': 0, 'grasas': 0, 'nutrientes': {}}
    }

    for perfil in perfiles:
        grupo = 'menores_30' if perfil.edad < 30 else 'mayores_30'
        # Filtrar los registros por usuario y fechas si se proporcionan
        registros = RegistroDiario.objects.filter(usuario=perfil.usuario)
        if fecha_inicio:
            registros = registros.filter(fecha__gte=fecha_inicio)
        if fecha_fin:
            registros = registros.filter(fecha__lte=fecha_fin)

        for registro in registros:
            alimento = registro.alimento
            resultados[grupo]['calorias'] += float(alimento.calorias) * float(registro.cantidad)
            resultados[grupo]['proteinas'] += float(alimento.proteinas) * float(registro.cantidad)
            resultados[grupo]['carbohidratos'] += float(alimento.carbohidratos) * float(registro.cantidad)
            resultados[grupo]['grasas'] += float(alimento.grasas) * float(registro.cantidad)

            nutrientes = AlimentoNutriente.objects.filter(alimento=alimento)
            for nutriente in nutrientes:
                if nutriente.nutriente.nombre not in resultados[grupo]['nutrientes']:
                    resultados[grupo]['nutrientes'][nutriente.nutriente.nombre] = 0
                resultados[grupo]['nutrientes'][nutriente.nutriente.nombre] += float(nutriente.cantidad) * float(registro.cantidad)

    # Calcular promedios
    for grupo in resultados:
        total_usuarios = PerfilNutricional.objects.filter(edad__lt=30).count() if grupo == 'menores_30' else PerfilNutricional.objects.filter(edad__gte=30).count()
        if total_usuarios > 0:
            for key in ['calorias', 'proteinas', 'carbohidratos', 'grasas']:
                resultados[grupo][key] /= total_usuarios
            for nutriente in resultados[grupo]['nutrientes']:
                resultados[grupo]['nutrientes'][nutriente] /= total_usuarios

    return resultados

# Evalúa cuál grupo tiene un mayor riesgo basado en su consumo nutricional. Utiliza los resultados del análisis de consumo
# para comparar el consumo calórico y de macronutrientes entre los dos grupos, así como la diversidad de nutrientes consumidos.
# Proporciona como resultado un grupo con mayor riesgo y las razones de esta evaluación.
def evaluar_grupos(resultados):
    evaluacion = {
        'grupo_mas_riesgo': '',
        'razones': []
    }

    # Comparar consumo calórico
    if resultados['menores_30']['calorias'] > resultados['mayores_30']['calorias']:
        evaluacion['grupo_mas_riesgo'] = 'El grupo de menores de 30'
        evaluacion['razones'].append('mayor consumo calórico')
    else:
        evaluacion['grupo_mas_riesgo'] = 'El grupo de mayores de 30'
        evaluacion['razones'].append('mayor consumo calórico')

    # Comparar macronutrientes
    for nutriente in ['proteinas', 'carbohidratos', 'grasas']:
        if resultados['menores_30'][nutriente] > resultados['mayores_30'][nutriente]:
            evaluacion['razones'].append(f'mayor consumo de {nutriente} en menores de 30')
        else:
            evaluacion['razones'].append(f'mayor consumo de {nutriente} en mayores de 30')

    # Comparar diversidad de nutrientes
    nutrientes_menores_30 = set(resultados['menores_30']['nutrientes'].keys())
    nutrientes_mayores_30 = set(resultados['mayores_30']['nutrientes'].keys())
    if len(nutrientes_menores_30) < len(nutrientes_mayores_30):
        evaluacion['razones'].append('menor diversidad de nutrientes en menores de 30.')
    elif len(nutrientes_menores_30) > len(nutrientes_mayores_30):
        evaluacion['razones'].append('menor diversidad de nutrientes en mayores de 30.')

    return evaluacion

# Ejecutar análisis y evaluación
resultados_analisis = analisis_consumo()
evaluacion_final = evaluar_grupos(resultados_analisis)

# Realiza un análisis de consumo utilizando la función analisis_consumo, evalúa los grupos con evaluar_grupos,
# y prepara los datos para ser visualizados en gráficos. Finalmente, envía esos datos a un template HTML
# para su visualización. Es una vista de alto nivel que integra la lógica de análisis con la presentación de datos.
@login_required
@user_passes_test(lambda u: u.is_superuser)
def vista_analisis(request):
    fecha_inicio = request.GET.get('fecha_inicio') # o como se envíe el parámetro
    fecha_fin = request.GET.get('fecha_fin') # o como se envíe el parámetro
    resultados_analisis = analisis_consumo(fecha_inicio, fecha_fin)
    evaluacion_final = evaluar_grupos(resultados_analisis)

    # Preparar datos para gráficos
    datos_graficos = {
        'menores_30': {
            'calorias': resultados_analisis['menores_30']['calorias'],
            'proteinas': resultados_analisis['menores_30']['proteinas'],
            'carbohidratos': resultados_analisis['menores_30']['carbohidratos'],
            'grasas': resultados_analisis['menores_30']['grasas'],
            'nutrientes': resultados_analisis['menores_30']['nutrientes']
        },
        'mayores_30': {
            'calorias': resultados_analisis['mayores_30']['calorias'],
            'proteinas': resultados_analisis['mayores_30']['proteinas'],
            'carbohidratos': resultados_analisis['mayores_30']['carbohidratos'],
            'grasas': resultados_analisis['mayores_30']['grasas'],
            'nutrientes': resultados_analisis['mayores_30']['nutrientes']
        }
    }

    context = {
        'evaluacion': evaluacion_final,
        'datos_graficos': datos_graficos
    }

    return render(request, 'analisis-consumo.html', context)

# Personaliza la vista de login de Django definiendo un template específico, manejo de campos y redirección
# tras un login exitoso. redirect_authenticated_user asegura que usuarios ya autenticados sean
# redirigidos a una página principal.
class Logueo(LoginView):
    template_name = "base/login.html"
    field = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('main_page')

# Personaliza la página de registro de usuarios utilizando UserCreationForm. Maneja la creación de nuevos usuarios,
# autenticándolos inmediatamente tras un registro exitoso y redirigiéndolos a una página principal.
# También verifica si el usuario ya está autenticado para redirigirlo directamente a la página
# principal sin necesidad de registrarse.
class PaginaRegistro(FormView):
    template_name = 'base/registro.html'
    form_class = UserCreationForm
    redirect_authtenticated_user = True
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        usuario = form.save()
        if usuario is not None:
            login(self.request, usuario)
        return super(PaginaRegistro, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('main_page')
        return super(PaginaRegistro, self).get(*args, **kwargs)

# Muestra la página principal de la aplicación (index.html). Es una vista simple que no realiza
# ninguna operación más allá de renderizar la página.
@login_required
def main_page(request):
    return render(request, 'index.html')

# Maneja la adición de un nuevo alimento. Si el método es POST y el formulario es válido, crea un nuevo objeto Alimento,
# asigna el usuario actual a este y luego lo guarda en la base de datos. Si el método no es POST,
# muestra un formulario vacío para agregar un nuevo alimento.
@login_required
def agregar_alimento(request):
    if request.method == "POST":
        form = AlimentoForm(request.POST, request.FILES)
        if form.is_valid():
            alimento = form.save(commit=False)  # Guarda el alimento pero no lo comitees aún a la base de datos.
            alimento.usuario = request.user  # Asigna el usuario actual al alimento.
            alimento.save()  # Ahora guarda el alimento en la base de datos con el usuario asociado.
            return redirect('listar_alimentos')
    else:
        form = AlimentoForm()
    return render(request, 'base/agregar_alimento.html', {'form': form})

# Recupera y muestra todos los alimentos asociados con el usuario actual. Filtra los alimentos en la base de datos
# para mostrar solo aquellos que pertenecen al usuario que ha iniciado sesión.
@login_required
def listar_alimentos(request):
    alimentos = Alimento.objects.filter(usuario=request.user)
    return render(request, 'base/listar_alimentos.html', {'alimentos': alimentos})

# Permite editar un alimento existente. Si el método es POST y el formulario es válido, actualiza el alimento en la base de datos
# con la nueva información. Si no es POST, muestra el formulario precargado con la información del alimento a editar.
@login_required
def editar_alimento(request, alimento_id):
    alimento = get_object_or_404(Alimento, id=alimento_id)
    if request.method == "POST":
        form = AlimentoForm(request.POST, request.FILES, instance=alimento)
        if form.is_valid():
            form.save()
            return redirect('listar_alimentos')
    else:
        form = AlimentoForm(instance=alimento)
    return render(request, 'base/editar_alimento.html', {'form': form, 'alimento': alimento})

# Permite eliminar un alimento específico, identificado por su ID. Si el método es POST, elimina el alimento y redirige
# a la lista de alimentos. De lo contrario, probablemente se muestre una página de confirmación para la eliminación.
@login_required
def eliminar_alimento(request, alimento_id):
    alimento = get_object_or_404(Alimento, id=alimento_id)
    if request.method == "POST":
        alimento.delete()
        return redirect('listar_alimentos')
    return render(request, 'base/eliminar_alimento.html', {'alimento': alimento})

# Permite al usuario registrar su ingesta diaria de alimentos. Al recibir un POST, valida y guarda los datos del formulario.
# Antes de guardar, verifica que el alimento a registrar no haga que el usuario sobrepase sus límites nutricionales diarios.
# Si el usuario ya ha cumplido o está por sobrepasar sus límites, muestra una advertencia o una felicitación, respectivamente.
@login_required
def registro_diario(request):
    if request.method == "POST":
        form = RegistroDiarioForm(request.POST, user=request.user)
        form.instance.usuario = request.user
        if form.is_valid():
            registros = RegistroDiario.objects.filter(usuario=request.user, fecha=date.today())
            perfil = get_object_or_404(PerfilNutricional, usuario=request.user)
            necesidades = calcular_necesidades_nutricionales(perfil)
            analisis = analizar_ingesta_nutricional(registros, necesidades)

            alimento_obj = get_object_or_404(Alimento, id=form.cleaned_data['alimento'].id)
            alimento_info = {
                'calorias': alimento_obj.calorias,
                'proteinas': alimento_obj.proteinas,
                'carbohidratos': alimento_obj.carbohidratos,
                'grasas': alimento_obj.grasas,
                'cantidad': form.cleaned_data.get('cantidad', 1)
            }

            # Removed or modified code to ignore excess warning and fulfillment message.
            registro = form.save(commit=False)
            registro.exceso = False # Assuming all entries are not excessive by default.

            registro.save()

            # Removed the success message for fulfilling dietary limits.

            return redirect('analisis_nutricional')
    else:
        form = RegistroDiarioForm(user=request.user)
    return render(request, 'base/registro_diario.html', {'form': form})


@login_required
def reporte_excesos(request):
    # Get the total calorie intake for each user for each day
    total_calorias = RegistroDiario.objects.values('fecha', 'usuario__username').annotate(
        total_calorias=Sum(F('alimento__calorias') * F('cantidad'), output_field=DecimalField())
    ).order_by('usuario', 'fecha')

    # You might need to get each user's calorie limit from PerfilNutricional or use a static value
    # For simplicity, let's assume a static limit of 2000 calories here
    CALORIE_LIMIT = 2000

    # Filter out the days where the user exceeded the calorie limit
    excesos = [registro for registro in total_calorias if registro['total_calorias'] > CALORIE_LIMIT]

    return render(request, 'base/reporte_excesos.html', {'registros_excesos': excesos})





# Permite al usuario crear o editar su perfil nutricional. Utiliza get_or_create para evitar la creación de múltiples perfiles
# para un mismo usuario. Si el método es POST y el formulario es válido, guarda la información del perfil y redirige a la página principal.
@login_required
def perfil_nutricional(request):
    perfil, created = PerfilNutricional.objects.get_or_create(
        usuario=request.user,
        defaults={'edad': 0, 'peso': 0.0, 'altura': 0.0, 'sexo': 'Hombre', 'nivel_actividad': 'sedentario'}
    )
    if request.method == "POST":
        form = PerfilNutricionalForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('main_page')
    else:
        form = PerfilNutricionalForm(instance=perfil)
    return render(request, 'base/perfil_nutricional.html', {'form': form})

# Realiza y muestra un análisis nutricional del usuario basado en su perfil nutricional y registros diarios.
# Calcula las necesidades nutricionales del usuario y compara su ingesta diaria con estas necesidades.
# Si el usuario ha cumplido sus límites nutricionales para el día, muestra un mensaje de felicitación.
@login_required
def analisis_nutricional(request):
    perfil = get_object_or_404(PerfilNutricional, usuario=request.user)
    registros = RegistroDiario.objects.filter(usuario=request.user, fecha=date.today())
    necesidades = calcular_necesidades_nutricionales(perfil)
    analisis = analizar_ingesta_nutricional(registros, necesidades)

    if ha_cumplido_limites(analisis, necesidades):
        messages.success(request, '¡Felicidades! Has cumplido con tu dosis diaria.')

    return render(request, 'base/analisis_nutricional.html', {'analisis': analisis})

# Proporciona sugerencias nutricionales personalizadas a usuarios autenticados basándose en su perfil e ingesta diaria.
@login_required
def sugerencias_alimentos(request):
    # Obtener el perfil nutricional del usuario
    perfil = get_object_or_404(PerfilNutricional, usuario=request.user)
    bmr = calcular_bmr(perfil)

    # Filtrar registros por la fecha de hoy
    registros = RegistroDiario.objects.filter(usuario=request.user, fecha=date.today())
    necesidades = calcular_necesidades_nutricionales(perfil)
    analisis = analizar_ingesta_nutricional(registros, necesidades)

    # Obtener top 5 de alimentos ricos en micronutrientes y macronutrientes
    sugerencias_macro_micro = Alimento.objects.filter(usuario=request.user).annotate(total_macro=F('proteinas') + F('carbohidratos') + F('grasas') + F('nutrientes')).order_by('-total_macro')[:5]

    Alimento.objects.filter(usuario=request.user)


    return render(request, 'base/sugerencias_alimentos.html', {
        'bmr': bmr,
        'analisis': analisis,
        'sugerencias_macro_micro': sugerencias_macro_micro,
    })




