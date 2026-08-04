"""
Data Transfer Objects para la entidad Usuario.
"""
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class RegistrarUsuarioDTO:
    nombre: str
    apellido: str
    fecha_nacimiento: date
    correo_electronico: str
    password: str
    confirmar_password: str

    def es_valido(self) -> bool:
        return self.password == self.confirmar_password


@dataclass
class LoginDTO:
    correo_electronico: str
    password: str


@dataclass
class UsuarioResponseDTO:
    id: int
    nombre: str
    apellido: str
    correo_electronico: str
    es_admin: bool
    estado_cuenta: str
    nombre_completo: Optional[str] = None

    def __post_init__(self):
        self.nombre_completo = f"{self.nombre} {self.apellido}"
