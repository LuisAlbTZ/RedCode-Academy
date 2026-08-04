"""
Casos de uso para publicaciones WorkGroup (Código/Entregables) y Calificaciones.
"""
from typing import List, Optional
from src.infrastructure.models.models import db, WorkGroup, UsuarioConvocatoria, CalificacionWorkGroup

class CrearWorkGroup:
    """
    Caso de uso: Aprendiz sube su entregable/código a la convocatoria.
    Solo usuarios con estado_validacion='Aprobado' pueden crear WorkGroups.
    """

    def execute(
        self,
        usuario_id: int,
        convocatoria_id: int,
        titulo: str,
        descripcion_texto: Optional[str] = None,
        contenido_codigo: Optional[str] = None,
        enlace_repositorio: Optional[str] = None,
    ) -> WorkGroup:
        # Verificar que el usuario está aprobado en la convocatoria
        relacion = UsuarioConvocatoria.query.filter_by(
            usuario_id=usuario_id,
            convocatoria_id=convocatoria_id,
        ).first()

        if not relacion:
            raise PermissionError("No estás inscrito en esta convocatoria.")

        if relacion.estado_validacion != 'Aprobado':
            raise PermissionError("Tu participación aún no ha sido aprobada por el mentor.")

        work_group = WorkGroup(
            titulo=titulo,
            descripcion_texto=descripcion_texto,
            contenido_codigo=contenido_codigo,
            enlace_repositorio=enlace_repositorio,
            usuario_id=usuario_id,
            convocatoria_id=convocatoria_id,
            puntuacion=0,
        )
        db.session.add(work_group)
        db.session.commit()
        return work_group

class ListarWorkGroups:
    """Caso de uso: Listar WorkGroups de una convocatoria, ordenados por puntuación."""

    def execute(self, convocatoria_id: Optional[int] = None) -> List[WorkGroup]:
        query = WorkGroup.query
        if convocatoria_id:
            query = query.filter_by(convocatoria_id=convocatoria_id)
        return query.order_by(WorkGroup.puntuacion.desc(), WorkGroup.fecha_creacion.desc()).all()

class ObtenerWorkGroup:
    """Caso de uso: Obtener detalle de un WorkGroup."""

    def execute(self, work_group_id: int) -> Optional[WorkGroup]:
        return db.session.get(WorkGroup, work_group_id)

class VotarWorkGroup:
    """
    Caso de uso: Votar (upvote/downvote) en un WorkGroup, estilo Reddit.
    """

    def execute(self, work_group_id: int, direccion: str) -> WorkGroup:
        work_group = db.session.get(WorkGroup, work_group_id)
        if not work_group:
            raise ValueError("WorkGroup no encontrado.")

        if direccion == 'up':
            work_group.puntuacion += 1
        elif direccion == 'down':
            work_group.puntuacion -= 1
        else:
            raise ValueError("Dirección inválida. Use 'up' o 'down'.")

        db.session.commit()
        return work_group

class ActualizarWorkGroup:
    """Caso de uso: Actualizar el entregable de un WorkGroup (solo el autor)."""

    def execute(self, work_group_id: int, usuario_id: int, **kwargs) -> WorkGroup:
        wg = db.session.get(WorkGroup, work_group_id)
        if not wg:
            raise ValueError("WorkGroup no encontrado.")
        if wg.usuario_id != usuario_id:
            raise PermissionError("Solo el autor puede editar este WorkGroup.")

        for campo, valor in kwargs.items():
            if hasattr(wg, campo) and valor is not None:
                setattr(wg, campo, valor)

        db.session.commit()
        return wg
