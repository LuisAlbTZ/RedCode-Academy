"""
src/application/use_cases/admin_use_cases.py
Casos de uso para el Administrador: CRUD global sobre usuarios, convocatorias, moderación.
"""
from typing import List
from src.infrastructure.models.models import db, Usuario, Convocatoria, WorkGroup, ComentarioWorkGroup


class GestionarUsuarios:
    """Caso de uso Admin: Gestión de usuarios (banear, reactivar, listar)."""

    def listar_todos(self) -> List[Usuario]:
        return Usuario.query.order_by(Usuario.fecha_registro.desc()).all()

    def cambiar_estado(self, usuario_id: int, nuevo_estado: str) -> Usuario:
        """Banear (Suspendido/Inactivo) o reactivar (Activo) una cuenta."""
        if nuevo_estado not in ('Activo', 'Inactivo', 'Suspendido'):
            raise ValueError("Estado inválido.")
        usuario = db.session.get(Usuario, usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado.")
        usuario.estado_cuenta = nuevo_estado
        db.session.commit()
        return usuario

    def promover_a_admin(self, usuario_id: int) -> Usuario:
        """Otorgar permisos de administrador a un usuario."""
        usuario = db.session.get(Usuario, usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado.")
        usuario.es_admin = True
        db.session.commit()
        return usuario

    def revocar_admin(self, usuario_id: int) -> Usuario:
        """Revocar permisos de administrador."""
        usuario = db.session.get(Usuario, usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado.")
        usuario.es_admin = False
        db.session.commit()
        return usuario

class GestionarConvocatoriasAdmin:
    """Caso de uso Admin: Gestión global de convocatorias."""

    def listar_todas(self) -> List[Convocatoria]:
        return Convocatoria.query.order_by(Convocatoria.fecha_creacion.desc()).all()

    def cambiar_estado(self, convocatoria_id: int, nuevo_estado: str) -> Convocatoria:
        if nuevo_estado not in ('Borrador', 'Activa', 'Finalizada'):
            raise ValueError("Estado inválido.")
        conv = db.session.get(Convocatoria, convocatoria_id)
        if not conv:
            raise ValueError("Convocatoria no encontrada.")
        conv.estado = nuevo_estado
        db.session.commit()
        return conv

    def cambiar_visibilidad(self, convocatoria_id: int, visibilidad: str) -> Convocatoria:
        if visibilidad not in ('Pública', 'Privada'):
            raise ValueError("Visibilidad inválida.")
        conv = db.session.get(Convocatoria, convocatoria_id)
        if not conv:
            raise ValueError("Convocatoria no encontrada.")
        conv.visibilidad = visibilidad
        db.session.commit()
        return conv

    def eliminar(self, convocatoria_id: int) -> bool:
        conv = db.session.get(Convocatoria, convocatoria_id)
        if not conv:
            raise ValueError("Convocatoria no encontrada.")
        db.session.delete(conv)
        db.session.commit()
        return True

class ModerarContenido:
    """Caso de uso Admin: Moderar comentarios y work groups."""

    def eliminar_comentario(self, comentario_id: int) -> bool:
        comentario = db.session.get(ComentarioWorkGroup, comentario_id)
        if not comentario:
            raise ValueError("Comentario no encontrado.")
        db.session.delete(comentario)
        db.session.commit()
        return True

    def eliminar_work_group(self, work_group_id: int) -> bool:
        wg = db.session.get(WorkGroup, work_group_id)
        if not wg:
            raise ValueError("WorkGroup no encontrado.")
        db.session.delete(wg)
        db.session.commit()
        return True
