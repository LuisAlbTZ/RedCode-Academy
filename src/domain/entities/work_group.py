"""
domain/entities/work_group.py
Entidad de dominio puro para WorkGroup (publicación/entregable).
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class WorkGroupEntity:
    """Representación pura del dominio para un WorkGroup (publicación tipo Reddit/repositorio)."""
    id: Optional[int]
    titulo: str
    usuario_id: int
    convocatoria_id: int
    descripcion_texto: Optional[str] = None
    contenido_codigo: Optional[str] = None
    enlace_repositorio: Optional[str] = None
    puntuacion: int = 0
    fecha_creacion: datetime = field(default_factory=datetime.utcnow)
    fecha_actualizacion: datetime = field(default_factory=datetime.utcnow)
