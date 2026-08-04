"""domain/entities/__init__.py"""
from .usuario import UsuarioEntity
from .convocatoria import ConvocatoriaEntity
from .work_group import WorkGroupEntity
from .comentario import ComentarioEntity
from .calificacion import CalificacionEntity

__all__ = [
    'UsuarioEntity',
    'ConvocatoriaEntity',
    'WorkGroupEntity',
    'ComentarioEntity',
    'CalificacionEntity',
]
