from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Tarea


class ListaPendientes(ListView):
    model = Tarea
    context_object_name = 'tareas'


class DetalleTarea(DetailView):
    model = Tarea
    context_object_name = 'tarea'
    template_name = 'base/tarea.html'


class CrearTarea(CreateView):
    model = Tarea
    fields = '__all__'
    success_url = reverse_lazy('tareas')


class EditarTarea(UpdateView):
    model = Tarea
    fields = '__all__'
    success_url = reverse_lazy('tareas')


class EliminarTarea(DeleteView):
    model = Tarea
    context_object_name = 'tareas'
    success_url = reverse_lazy('tareas')
