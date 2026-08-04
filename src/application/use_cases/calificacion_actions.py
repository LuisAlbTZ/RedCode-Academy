"""
Casos de uso para calificaciones de WorkGroups (Jurado evalúa entregas).
"""
from typing import List, Optional, Tuple
from src.infrastructure.models.models import db, CalificacionWorkGroup, WorkGroup, UsuarioConvocatoria


class CalificarWorkGroup:
    """
    Caso de uso: Jurado califica una entrega.
    Solo usuarios con rol 'Jurado' o 'Mentor' pueden calificar.
    """

    def execute(
        self,
        jurado_id: int,
        work_group_id: int,
        calificacion: int,
    ) -> CalificacionWorkGroup:
        if not (1 <= calificacion <= 10):
            raise ValueError("La calificación debe ser entre 1 y 10.")

        work_group = db.session.get(WorkGroup, work_group_id)
        if not work_group:
            raise ValueError("WorkGroup no encontrado.")

        # Verificar rol de jurado o mentor en la convocatoria
        relacion = UsuarioConvocatoria.query.filter(
            UsuarioConvocatoria.usuario_id == jurado_id,
            UsuarioConvocatoria.convocatoria_id == work_group.convocatoria_id,
            UsuarioConvocatoria.rol_en_convocatoria.in_(['Jurado', 'Mentor']),
        ).first()

        if not relacion:
            raise PermissionError("Solo el Jurado o Mentor puede calificar entregas.")

        # Verificar si ya calificó este WorkGroup
        ya_califico = CalificacionWorkGroup.query.filter_by(
            usuario_id=jurado_id,
            work_group_id=work_group_id,
        ).first()

        if ya_califico:
            ya_califico.calificacion = calificacion
            db.session.commit()
            return ya_califico

        nueva = CalificacionWorkGroup(
            calificacion=calificacion,
            usuario_id=jurado_id,
            work_group_id=work_group_id,
        )
        db.session.add(nueva)
        db.session.commit()
        return nueva

class DecidirGanador:
    """
    Caso de uso: Obtener el ganador de una convocatoria basado en calificaciones.
    Devuelve el WorkGroup con mayor promedio de calificación.
    """

    def execute(self, convocatoria_id: int) -> Optional[Tuple[WorkGroup, float]]:
        work_groups = WorkGroup.query.filter_by(convocatoria_id=convocatoria_id).all()
        if not work_groups:
            return None

        ganador = None
        mayor_promedio = -1.0

        for wg in work_groups:
            promedio = wg.promedio_calificacion
            if promedio > mayor_promedio:
                mayor_promedio = promedio
                ganador = wg

        if ganador:
            return ganador, mayor_promedio
        return None
