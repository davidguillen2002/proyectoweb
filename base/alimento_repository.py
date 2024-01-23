from django.shortcuts import get_object_or_404
from base.models import Alimento


class AlimentoRepository:
    def get_all(self):
        return Alimento.objects.all()

    def get_by_id(self, alimento_id):
        return get_object_or_404(Alimento, id=alimento_id)

    def add(self, alimento):
        alimento.save()
        return alimento

    def update(self, alimento):
        alimento.save()
        return alimento

    def delete(self, alimento_id):
        alimento = self.get_by_id(alimento_id)
        alimento.delete()
