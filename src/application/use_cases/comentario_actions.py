"""
Casos de uso para comentarios en WorkGroups (retroalimentación de Mentor/Jurado).
"""
from typing import List
from src.infrastructure.models.models import db, ComentarioWorkGroup, WorkGroup, UsuarioConvocatoria

class CrearComentario:
    """
    Caso de uso: Mentor o Jurado deja feedback en una entrega (WorkGroup).
    """

    def execute(
        self,
        usuario_id: int,
        work_group_id: int,
        contenido: str,
    ) -> ComentarioWorkGroup:
        work_group = db.session.get(WorkGroup, work_group_id)
        if not work_group:
            raise ValueError("WorkGroup no encontrado.")

        comentario = ComentarioWorkGroup(
            contenido=contenido,
            usuario_id=usuario_id,
            work_group_id=work_group_id,
        )
        db.session.add(comentario)
        db.session.commit()
        return comentario

class ListarComentarios:
    """Caso de uso: Listar todos los comentarios de un WorkGroup."""

    def execute(self, work_group_id: int) -> List[ComentarioWorkGroup]:
        return ComentarioWorkGroup.query.filter_by(
            work_group_id=work_group_id
        ).order_by(ComentarioWorkGroup.fecha_comentario.asc()).all()
