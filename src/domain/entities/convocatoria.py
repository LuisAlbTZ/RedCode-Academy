"""
domain/entities/convocatoria.py
Entidad de dominio puro para la Convocatoria.
"""
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class ConvocatoriaEntity:
    """Representación pura del dominio para una Convocatoria."""
    id: Optional[int]
    titulo: str
    descripcion: str
    visibilidad: str  # Pública | Privada
    fecha_inicio: datetime
    fecha_fin: datetime
    reglas: str
    especificaciones: str
    indicaciones: str
    metricas_evaluacion: str
    modalidad: str = 'Individual'  # Individual | Equipo
    costo: Decimal = Decimal('0.00')
    tecnologias_sugeridas: Optional[str] = None
    patrocinadores: Optional[str] = None
    min_participantes: int = 1
    max_participantes: int = 1
    estado: str = 'Activa'  # Borrador | Activa | Finalizada
    fecha_creacion: datetime = field(default_factory=datetime.utcnow)

    def esta_activa(self) -> bool:
        return self.estado == 'Activa'

    def es_publica(self) -> bool:
        return self.visibilidad == 'Pública'
