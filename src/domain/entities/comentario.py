"""
domain/entities/comentario.py
Entidad de dominio puro para ComentarioWorkGroup.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class ComentarioEntity:
    """Representación pura del dominio para un Comentario en un WorkGroup."""
    id: Optional[int]
    contenido: str
    usuario_id: int
    work_group_id: int
    fecha_comentario: datetime = field(default_factory=datetime.utcnow)
