"""
application/use_cases/participacion_use_cases.py
Casos de uso para la gestión de participación en convocatorias.
- Aprendiz: Participar (inscribirse)
- Mentor: Validar participantes, Decidir jurado
"""
from typing import List
from src.infrastructure.models.models import db, UsuarioConvocatoria, Convocatoria, Usuario


class PostularConvocatoria:
    """
    Caso de uso: Inscribirse en una convocatoria como Aprendiz.
    Genera un registro en usuario_convocatoria con rol='Aprendiz' y estado='Pendiente'.
    """

    def execute(self, usuario_id: int, convocatoria_id: int) -> UsuarioConvocatoria:
        # Verificar que no esté ya inscrito
        ya_inscrito = UsuarioConvocatoria.query.filter_by(
            usuario_id=usuario_id,
            convocatoria_id=convocatoria_id,
        ).first()
        if ya_inscrito:
            raise ValueError("Ya estás inscrito en esta convocatoria.")

        convocatoria = db.session.get(Convocatoria, convocatoria_id)
        if not convocatoria or convocatoria.estado != 'Activa':
            raise ValueError("La convocatoria no está disponible para participación.")

        relacion = UsuarioConvocatoria(
            usuario_id=usuario_id,
            convocatoria_id=convocatoria_id,
            rol_en_convocatoria='Aprendiz',
            estado_validacion='Pendiente',
        )
        db.session.add(relacion)
        db.session.commit()
        return relacion

class ValidarParticipante:
    """
    Caso de uso: Mentor aprueba o rechaza la postulación de un Aprendiz.
    Actualiza estado_validacion en usuario_convocatoria.
    """

    def execute(
        self,
        mentor_id: int,
        participante_id: int,
        convocatoria_id: int,
        nuevo_estado: str,  # 'Aprobado' | 'Rechazado'
    ) -> UsuarioConvocatoria:
        # Verificar que el que ejecuta es Mentor de esta convocatoria
        es_mentor = UsuarioConvocatoria.query.filter_by(
            usuario_id=mentor_id,
            convocatoria_id=convocatoria_id,
            rol_en_convocatoria='Mentor',
        ).first()
        if not es_mentor:
            raise PermissionError("Solo los mentores pueden validar participantes.")

        relacion = UsuarioConvocatoria.query.filter_by(
            usuario_id=participante_id,
            convocatoria_id=convocatoria_id,
            rol_en_convocatoria='Aprendiz',
        ).first()
        if not relacion:
            raise ValueError("El participante no está inscrito en esta convocatoria.")

        if nuevo_estado not in ('Aprobado', 'Rechazado'):
            raise ValueError("Estado inválido. Use 'Aprobado' o 'Rechazado'.")

        relacion.estado_validacion = nuevo_estado
        db.session.commit()
        return relacion

class AsignarJurado:
    """
    Caso de uso: Mentor asigna rol de Jurado a otro usuario en la convocatoria.
    """

    def execute(
        self,
        mentor_id: int,
        jurado_id: int,
        convocatoria_id: int,
    ) -> UsuarioConvocatoria:
        # Verificar que el que ejecuta es Mentor
        es_mentor = UsuarioConvocatoria.query.filter_by(
            usuario_id=mentor_id,
            convocatoria_id=convocatoria_id,
            rol_en_convocatoria='Mentor',
        ).first()
        if not es_mentor:
            raise PermissionError("Solo los mentores pueden asignar jurado.")

        # Verificar que el usuario existe
        jurado = db.session.get(Usuario, jurado_id)
        if not jurado:
            raise ValueError("El usuario no existe.")

        # Verificar si ya tiene un rol en esta convocatoria
        ya_en_conv = UsuarioConvocatoria.query.filter_by(
            usuario_id=jurado_id,
            convocatoria_id=convocatoria_id,
        ).first()
        if ya_en_conv:
            # Actualizar a Jurado si ya estaba como Aprendiz u otro
            ya_en_conv.rol_en_convocatoria = 'Jurado'
            ya_en_conv.estado_validacion = 'Aprobado'
            db.session.commit()
            return ya_en_conv

        relacion = UsuarioConvocatoria(
            usuario_id=jurado_id,
            convocatoria_id=convocatoria_id,
            rol_en_convocatoria='Jurado',
            estado_validacion='Aprobado',
        )
        db.session.add(relacion)
        db.session.commit()
        return relacion

class ListarParticipantes:
    """Caso de uso: Listar todos los participantes de una convocatoria."""

    def execute(self, convocatoria_id: int) -> List[UsuarioConvocatoria]:
        return UsuarioConvocatoria.query.filter_by(convocatoria_id=convocatoria_id).all()
