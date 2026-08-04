"""
domain/entities/calificacion.py
Entidad de dominio puro para CalificacionWorkGroup.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class CalificacionEntity:
    """Representación pura del dominio para una Calificación en un WorkGroup."""
    id: Optional[int]
    calificacion: int  # 1-10
    usuario_id: int
    work_group_id: int
    fecha_calificacion: datetime = field(default_factory=datetime.utcnow)
