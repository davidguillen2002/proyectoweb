from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Alimento, PerfilNutricional, RegistroDiario, Nutriente, AlimentoNutriente
from django.contrib.auth.decorators import login_required
from .utils import calcular_necesidades_nutricionales, analizar_ingesta_nutricional, calcular_bmr, ha_cumplido_limites, esta_por_sobrepasar_limites, MICRONUTRIENTES_ESENCIALES
from .forms import PerfilNutricionalForm, AlimentoForm, RegistroDiarioForm, NutrienteForm, AlimentoNutrienteForm
from django.db.models import Count
from datetime import date
from django.contrib import messages
from django.db.models import F
from django.shortcuts import get_object_or_404

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


@login_required
@user_passes_test(lambda u: u.is_superuser)
def listar_nutrientes(request):
    nutrientes = Nutriente.objects.all()
    return render(request, 'base/listar_nutrientes.html', {'nutrientes': nutrientes})


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


@login_required
@user_passes_test(lambda u: u.is_superuser)
def eliminar_nutriente(request, nutriente_id):
    nutriente = get_object_or_404(Nutriente, id=nutriente_id)
    if request.method == "POST":
        nutriente.delete()
        return redirect('listar_nutrientes')
    return render(request, 'base/eliminar_nutriente.html', {'nutriente': nutriente})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def listar_todos_alimentos(request):
    alimentos = Alimento.objects.all()
    return render(request, 'base/listar_todos_alimentos.html', {'alimentos': alimentos})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def agregar_nutriente_a_alimento(request, alimento_id):
    alimento = get_object_or_404(Alimento, id=alimento_id)

    if request.method == "POST":
        # Assuming a form class named AlimentoNutrienteForm which handles the addition of nutrients to foods.
        form = AlimentoNutrienteForm(request.POST)
        if form.is_valid():
            nutriente_rel = form.save(commit=False)
            nutriente_rel.alimento = alimento
            nutriente_rel.save()
            return redirect('listar_todos_alimentos')

    else:
        form = AlimentoNutrienteForm()
    return render(request, 'base/agregar_nutriente_a_alimento.html', {'form': form, 'alimento': alimento})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def editar_nutriente_de_alimento(request, alimento_id, relacion_id):
    alimento = get_object_or_404(Alimento, id=alimento_id)
    relacion = get_object_or_404(AlimentoNutriente, id=relacion_id) # Asume que tienes un modelo llamado AlimentoNutriente

    if request.method == "POST":
        form = AlimentoNutrienteForm(request.POST, instance=relacion)
        if form.is_valid():
            form.save()
            return redirect('listar_todos_alimentos')

    else:
        form = AlimentoNutrienteForm(instance=relacion)
    return render(request, 'base/editar_nutriente_de_alimento.html', {'form': form, 'alimento': alimento})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def eliminar_nutriente_de_alimento(request, alimento_id, relacion_id):
    alimento = get_object_or_404(Alimento, id=alimento_id)
    relacion = get_object_or_404(AlimentoNutriente,
                                 id=relacion_id)  # Nuevamente, asume que tienes un modelo llamado AlimentoNutriente

    if request.method == "POST":
        relacion.delete()
        return redirect('listar_todos_alimentos')

    return render(request, 'base/eliminar_nutriente_de_alimento.html', {'alimento': alimento, 'relacion': relacion})


class Logueo(LoginView):
    template_name = "base/login.html"
    field = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('main_page')  # Cambiado de 'tareas' a 'cotizar'


class PaginaRegistro(FormView):
    template_name = 'base/registro.html'
    form_class = UserCreationForm
    redirect_authtenticated_user = True
    success_url = reverse_lazy('main_page')  # Cambiado de 'tareas' a 'cotizar'

    def form_valid(self, form):
        usuario = form.save()
        if usuario is not None:
            login(self.request, usuario)
        return super(PaginaRegistro, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('main_page')  # Cambiado de 'tareas' a 'cotizar'
        return super(PaginaRegistro, self).get(*args, **kwargs)

@login_required
def main_page(request):
    return render(request, 'index.html')


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


@login_required
def listar_alimentos(request):
    alimentos = Alimento.objects.filter(usuario=request.user)
    return render(request, 'base/listar_alimentos.html', {'alimentos': alimentos})


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


@login_required
def eliminar_alimento(request, alimento_id):
    alimento = get_object_or_404(Alimento, id=alimento_id)
    if request.method == "POST":
        alimento.delete()
        return redirect('listar_alimentos')
    return render(request, 'base/eliminar_alimento.html', {'alimento': alimento})


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

            # Obtener el alimento desde la base de datos
            alimento_obj = get_object_or_404(Alimento, id=form.cleaned_data['alimento'].id)
            alimento_info = {
                'calorias': alimento_obj.calorias,
                'proteinas': alimento_obj.proteinas,
                'carbohidratos': alimento_obj.carbohidratos,
                'grasas': alimento_obj.grasas,
                'cantidad': form.cleaned_data.get('cantidad', 1)  # Asumimos que 1 es el valor por defecto
            }

            if esta_por_sobrepasar_limites(analisis, necesidades, alimento_info):
                messages.warning(request, 'Este alimento te hará sobrepasar o alcanzar tus límites diarios.')
                return render(request, 'base/registro_diario.html', {'form': form})

            form.save()
            if ha_cumplido_limites(analisis, necesidades):
                messages.success(request, '¡Felicidades! Has cumplido con tu dosis diaria.')

            return redirect('analisis_nutricional')
    else:
        form = RegistroDiarioForm(user=request.user)
    return render(request, 'base/registro_diario.html', {'form': form})



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


@login_required
def analisis_nutricional(request):
    perfil = get_object_or_404(PerfilNutricional, usuario=request.user)
    registros = RegistroDiario.objects.filter(usuario=request.user, fecha=date.today())
    necesidades = calcular_necesidades_nutricionales(perfil)
    analisis = analizar_ingesta_nutricional(registros, necesidades)

    if ha_cumplido_limites(analisis, necesidades):
        messages.success(request, '¡Felicidades! Has cumplido con tu dosis diaria.')

    return render(request, 'base/analisis_nutricional.html', {'analisis': analisis})


@login_required
def sugerencias_alimentos(request):
    # Obtener el perfil nutricional del usuario
    perfil = get_object_or_404(PerfilNutricional, usuario=request.user)
    bmr = calcular_bmr(perfil)

    # Filtrar registros por la fecha de hoy
    registros = RegistroDiario.objects.filter(usuario=request.user, fecha=date.today())
    necesidades = calcular_necesidades_nutricionales(perfil)
    analisis = analizar_ingesta_nutricional(registros, necesidades)

    # Obtener top 6 de alimentos ricos en micronutrientes y macronutrientes
    sugerencias_macro_micro = Alimento.objects.filter(usuario=request.user).annotate(total_macro=F('proteinas') + F('carbohidratos') + F('grasas') + F('nutrientes')).order_by('-total_macro')[:5]

    Alimento.objects.filter(usuario=request.user)


    return render(request, 'base/sugerencias_alimentos.html', {
        'bmr': bmr,
        'analisis': analisis,
        'sugerencias_macro_micro': sugerencias_macro_micro,
    })




