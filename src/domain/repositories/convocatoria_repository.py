"""
Interfaz abstracta para el repositorio de Convocatorias.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities.convocatoria import ConvocatoriaEntity


class ConvocatoriaRepositoryInterface(ABC):
    """Contrato de acceso a datos para la entidad Convocatoria."""

    @abstractmethod
    def guardar(self, convocatoria: ConvocatoriaEntity) -> ConvocatoriaEntity:
        raise NotImplementedError

    @abstractmethod
    def buscar_por_id(self, convocatoria_id: int) -> Optional[ConvocatoriaEntity]:
        raise NotImplementedError

    @abstractmethod
    def listar_todas(self) -> List[ConvocatoriaEntity]:
        raise NotImplementedError

    @abstractmethod
    def listar_activas(self) -> List[ConvocatoriaEntity]:
        raise NotImplementedError

    @abstractmethod
    def actualizar(self, convocatoria: ConvocatoriaEntity) -> ConvocatoriaEntity:
        raise NotImplementedError

    @abstractmethod
    def eliminar(self, convocatoria_id: int) -> bool:
        raise NotImplementedError
