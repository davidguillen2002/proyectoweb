from base.alimento_repository import AlimentoRepository
from base.models import Alimento
class AlimentoService:
    def __init__(self):
        self.repository = AlimentoRepository()

    def listar_todos_alimentos(self):
        return self.repository.get_all()

    def agregar_alimento(self, alimento_data):
        alimento = Alimento(**alimento_data)
        return self.repository.add(alimento)

    def editar_alimento(self, alimento_id, alimento_data):
        alimento = self.repository.get_by_id(alimento_id)
        for key, value in alimento_data.items():
            setattr(alimento, key, value)
        return self.repository.update(alimento)

    def eliminar_alimento(self, alimento_id):
        return self.repository.delete(alimento_id)
