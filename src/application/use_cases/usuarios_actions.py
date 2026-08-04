"""
Casos de uso para Autenticación: Registro, Login, Logout.
"""
import bcrypt
from datetime import date
from typing import Optional

from src.infrastructure.models.models import db, Usuario


class RegistrarUsuario:
    """
    Caso de uso: Registrar un nuevo usuario en la plataforma.
    Genera un registro en tabla usuario con es_admin=FALSE y estado_cuenta='Activo'.
    """

    def execute(
        self,
        nombre: str,
        apellido: str,
        fecha_nacimiento: date,
        correo_electronico: str,
        password: str,
    ) -> Usuario:
        # Verificar si el correo ya existe
        existe = Usuario.query.filter_by(correo_electronico=correo_electronico).first()
        if existe:
            raise ValueError("El correo electrónico ya está registrado.")

        # Hash de la contraseña con bcrypt
        password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            fecha_nacimiento=fecha_nacimiento,
            correo_electronico=correo_electronico,
            password_hash=password_hash,
            es_admin=False,
            estado_cuenta='Activo',
        )

        db.session.add(nuevo_usuario)
        db.session.commit()
        return nuevo_usuario

class LoginUsuario:
    """
    Caso de uso: Autenticar un usuario con correo y contraseña.
    """

    def execute(self, correo_electronico: str, password: str) -> Optional[Usuario]:
        usuario = Usuario.query.filter_by(correo_electronico=correo_electronico).first()

        if not usuario:
            return None

        if usuario.estado_cuenta != 'Activo':
            raise ValueError(f"Tu cuenta está {usuario.estado_cuenta}. Contacta al administrador.")

        if not bcrypt.checkpw(password.encode('utf-8'), usuario.password_hash.encode('utf-8')):
            return None

        return usuario

class CambiarCont:
    """
    Caso de uso: Cambiar la contraseña de un usuario.
    """

    def execute(self, usuario: Usuario, password_actual: str, nueva_password: str) -> bool:
        if not bcrypt.checkpw(password_actual.encode('utf-8'), usuario.password_hash.encode('utf-8')):
            raise ValueError("La contraseña actual es incorrecta.")

        usuario.password_hash = bcrypt.hashpw(
            nueva_password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        db.session.commit()
        return True

class ObtenerUsuario:
    """
    Caso de Uso: Obtener un usuario por su ID.
    """

    def execute(self, usuario_id: int) -> Optional[Usuario]:
        usuario = Usuario.query.get(usuario_id)
        
        return usuario


class ActualizarUsuario:
    """
    Caso de Uso: Actualizar los datos de un usuario existente.
    """

    def execute(
        self,
        usuario_id: int,
        nombre: Optional[str] = None,
        apellido: Optional[str] = None,
        fecha_nacimiento: Optional[date] = None,
        correo_electronico: Optional[str] = None
    ) -> Optional[Usuario]:
        
        # Obtener el usuario a actualizar
        usuario = Usuario.query.get(usuario_id)
        
        if not usuario:
            raise ValueError("Usuario no encontrado.")

        # Validar y actualizar el correo electrónico si se proporciona uno nuevo
        if correo_electronico and correo_electronico != usuario.correo_electronico:
            existe = Usuario.query.filter_by(correo_electronico=correo_electronico).first()
            if existe:
                raise ValueError("El correo electrónico solicitado ya está registrado.")
            usuario.correo_electronico = correo_electronico

        # Actualizar otros campos si se proporcionan nuevos valores
        if nombre:
            usuario.nombre = nombre
        if apellido:
            usuario.apellido = apellido
        if fecha_nacimiento:
            usuario.fecha_nacimiento = fecha_nacimiento

        # Confirmar los cambios en la base de datos
        db.session.commit()
        return usuario