from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Vehiculo, Cotizacion, FactorCotizacion
from decimal import Decimal


@user_passes_test(lambda u: u.is_superuser)
def listar_eliminar_usuarios(request):
    usuarios_normales = User.objects.filter(is_superuser=False)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        usuario_a_eliminar = get_object_or_404(User, pk=user_id)

        # Si el formulario de confirmación de eliminación se envía, elimina al usuario.
        if 'confirmar_eliminar' in request.POST:
            usuario_a_eliminar.delete()
            return redirect('lista_usuarios')  # Redirige a la lista de usuarios después de eliminar.
        else:
            # Si el usuario cancela la eliminación, vuelve a la lista de usuarios.
            return redirect('lista_usuarios')

    return render(request, 'base/listar_eliminar_usuarios.html', {'usuarios_normales': usuarios_normales})


class Logueo(LoginView):
    template_name = "base/login.html"
    field = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('cotizar')  # Cambiado de 'tareas' a 'cotizar'


class PaginaRegistro(FormView):
    template_name = 'base/registro.html'
    form_class = UserCreationForm
    redirect_authtenticated_user = True
    success_url = reverse_lazy('cotizar')  # Cambiado de 'tareas' a 'cotizar'

    def form_valid(self, form):
        usuario = form.save()
        if usuario is not None:
            login(self.request, usuario)
        return super(PaginaRegistro, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('cotizar')  # Cambiado de 'tareas' a 'cotizar'
        return super(PaginaRegistro, self).get(*args, **kwargs)


def calcular_cotizacion(vehiculo):
    # Primero obtenemos el factor base según el año del vehículo y el tipo de siniestro.
    try:
        factor = FactorCotizacion.objects.get(
            año_desde__lte=vehiculo.año,
            año_hasta__gte=vehiculo.año,
            tipo_siniestro=vehiculo.tipo_siniestro
        )
    except FactorCotizacion.DoesNotExist:
        print(
            f"No se encontró FactorCotizacion para el año {vehiculo.año} y el tipo de siniestro {vehiculo.tipo_siniestro}")
        # Si no hay un factor definido para ese año y tipo de siniestro, retornamos un valor por defecto.
        return vehiculo.valor * Decimal('0.9')  # 90% de cobertura por defecto.
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return vehiculo.valor * Decimal('0.9')  # 90% de cobertura por defecto.

    print(f"Factor encontrado: {factor}")

    # Ajustamos el factor según el tipo de siniestro.
    ajuste_siniestro = 1.0  # Valor por defecto, no hay ajuste.

    if vehiculo.tipo_siniestro == 'robo':
        ajuste_siniestro = Decimal('1.25')  # Robo es un 25% más costoso que el valor base.
    elif vehiculo.tipo_siniestro == 'accidente':
        ajuste_siniestro = Decimal('1.15')  # Accidente es un 15% más costoso que el valor base.
    elif vehiculo.tipo_siniestro == 'falla':
        ajuste_siniestro = Decimal('1.05')  # Falla es un 5% más costoso que el valor base.

    # Finalmente, calculamos la cotización.
    cotizacion_base = Decimal(vehiculo.valor) * Decimal(factor.factor)
    cotizacion = min(cotizacion_base * Decimal(str(ajuste_siniestro)), vehiculo.valor)

    print(f"Cotización calculada: {cotizacion}")

    return cotizacion


class CotizacionView(LoginRequiredMixin, CreateView):
    model = Vehiculo
    fields = ['marca', 'modelo', 'año', 'valor', 'tipo_siniestro']  # Agrega valor_asegurado
    template_name = 'base/cotizacion_form.html'

    def form_valid(self, form):
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.usuario = self.request.user
            vehiculo.save()
            valor_cotizado = calcular_cotizacion(vehiculo)
            Cotizacion.objects.create(vehiculo=vehiculo, valor_cotizado=valor_cotizado)
            return redirect('lista_cotizaciones')


class ListaCotizaciones(LoginRequiredMixin, ListView):
    model = Cotizacion
    template_name = 'base/lista_cotizaciones.html'
    context_object_name = 'cotizaciones'

    def get_queryset(self):
        queryset = Cotizacion.objects.filter(vehiculo__usuario=self.request.user)

        # Filtrado por rango de fechas
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            try:
                queryset = queryset.filter(creado__date__range=(fecha_inicio, fecha_fin))
            except:
                # manejar error de formato de fecha aquí si es necesario
                pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Cálculo de pérdidas
        perdidas_totales = sum([(c.vehiculo.valor - c.valor_cotizado) for c in context['cotizaciones']])
        context['perdidas_totales'] = perdidas_totales

        return context


class EditarCotizacion(LoginRequiredMixin, UpdateView):
    model = Vehiculo
    fields = ['marca', 'modelo', 'año', 'valor', 'tipo_siniestro']
    template_name = 'base/cotizacion_form.html'

    def get_success_url(self):
        return reverse_lazy('lista_cotizaciones')

    def form_valid(self, form):
        vehiculo = form.save()
        cotizacion = Cotizacion.objects.get(vehiculo=vehiculo)
        cotizacion.valor_cotizado = calcular_cotizacion(vehiculo)
        cotizacion.save()
        return super().form_valid(form)


class EliminarCotizacion(LoginRequiredMixin, DeleteView):
    model = Cotizacion
    template_name = 'base/cotizacion_confirm_delete.html'
    success_url = reverse_lazy('lista_cotizaciones')
