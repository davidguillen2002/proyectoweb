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
from .models import Tarea


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
        return reverse_lazy('tareas')


class PaginaRegistro(FormView):
    template_name = 'base/registro.html'
    form_class = UserCreationForm
    redirect_authtenticated_user = True
    success_url = reverse_lazy('tareas')

    def form_valid(self, form):
        usuario = form.save()
        if usuario is not None:
            login(self.request, usuario)
        return super(PaginaRegistro, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tareas')
        return super(PaginaRegistro, self).get(*args, **kwargs)


class ListaPendientes(LoginRequiredMixin, ListView):
    model = Tarea
    context_object_name = 'tareas'

    def get_context_data(self, **kwarg):
        context = super().get_context_data(**kwarg)
        context['tareas'] = context['tareas'].filter(usuario=self.request.user)
        context['count'] = context['tareas'].filter(completo=False).count()

        valor_buscado = self.request.GET.get('area-buscar') or ''
        if valor_buscado:
            context['tareas'] = context['tareas'].filter(titulo__icontains=valor_buscado)
        context['valor_buscado'] = valor_buscado
        return context


class DetalleTarea(LoginRequiredMixin, DetailView):
    model = Tarea
    context_object_name = 'tarea'
    template_name = 'base/tarea.html'


class CrearTarea(LoginRequiredMixin, CreateView):
    model = Tarea
    fields = ['titulo', 'descripcion', 'completo']
    success_url = reverse_lazy('tareas')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(CrearTarea, self).form_valid(form)


class EditarTarea(LoginRequiredMixin, UpdateView):
    model = Tarea
    fields = ['titulo', 'descripcion', 'completo']
    success_url = reverse_lazy('tareas')


class EliminarTarea(LoginRequiredMixin, DeleteView):
    model = Tarea
    context_object_name = 'tareas'
    success_url = reverse_lazy('tareas')





