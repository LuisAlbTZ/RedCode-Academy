"""domain/repositories/__init__.py"""
from .usuario_repository import UsuarioRepositoryInterface
from .convocatoria_repository import ConvocatoriaRepositoryInterface

__all__ = [
    'UsuarioRepositoryInterface',
    'ConvocatoriaRepositoryInterface',
]
