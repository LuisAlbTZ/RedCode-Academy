"""
Interfaz abstracta para el repositorio de Usuarios.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities.usuario import UsuarioEntity


class UsuarioRepositoryInterface(ABC):
    """Contrato de acceso a datos para la entidad Usuario."""

    @abstractmethod
    def guardar(self, usuario: UsuarioEntity) -> UsuarioEntity:
        raise NotImplementedError

    @abstractmethod
    def buscar_por_id(self, usuario_id: int) -> Optional[UsuarioEntity]:
        raise NotImplementedError

    @abstractmethod
    def buscar_por_correo(self, correo: str) -> Optional[UsuarioEntity]:
        raise NotImplementedError

    @abstractmethod
    def listar_todos(self) -> List[UsuarioEntity]:
        raise NotImplementedError

    @abstractmethod
    def actualizar(self, usuario: UsuarioEntity) -> UsuarioEntity:
        raise NotImplementedError

    @abstractmethod
    def eliminar(self, usuario_id: int) -> bool:
        raise NotImplementedError
