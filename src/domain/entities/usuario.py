"""
domain/entities/usuario.py
Entidad de dominio puro para el Usuario (sin dependencias de SQLAlchemy).
"""
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional


@dataclass
class UsuarioEntity:
    """Representación pura del dominio para un Usuario."""
    id: Optional[int]
    nombre: str
    apellido: str
    fecha_nacimiento: date
    correo_electronico: str
    password_hash: str
    es_admin: bool = False
    estado_cuenta: str = 'Activo'  # Activo | Inactivo | Suspendido
    fecha_registro: datetime = field(default_factory=datetime.utcnow)

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"

    def esta_activo(self) -> bool:
        return self.estado_cuenta == 'Activo'
