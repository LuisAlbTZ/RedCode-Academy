"""
Casos de uso para la gestión de Convocatorias (Mentor).
"""
from datetime import datetime
from typing import List, Optional

from src.infrastructure.models.models import db, Convocatoria, UsuarioConvocatoria, Usuario

class CrearConvocatoria:
    """
    Caso de uso: Crear y configurar una nueva convocatoria (Mentor).
    El mentor creador se vincula automáticamente con rol 'Mentor' y estado 'Aprobado'.
    """

    def execute(
        self,
        mentor_id: int,
        titulo: str,
        descripcion: str,
        visibilidad: str,
        fecha_inicio: datetime,
        fecha_fin: datetime,
        reglas: str,
        especificaciones: str,
        indicaciones: str,
        metricas_evaluacion: str,
        modalidad: str = 'Individual',
        costo: float = 0.00,
        tecnologias_sugeridas: Optional[str] = None,
        patrocinadores: Optional[str] = None,
        min_participantes: int = 1,
        max_participantes: int = 1,
    ) -> Convocatoria:
        nueva = Convocatoria(
            titulo=titulo,
            descripcion=descripcion,
            visibilidad=visibilidad,
            costo=costo,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            reglas=reglas,
            especificaciones=especificaciones,
            indicaciones=indicaciones,
            metricas_evaluacion=metricas_evaluacion,
            modalidad=modalidad,
            tecnologias_sugeridas=tecnologias_sugeridas,
            patrocinadores=patrocinadores,
            min_participantes=min_participantes,
            max_participantes=max_participantes,
            estado='Activa',
        )
        db.session.add(nueva)
        db.session.flush()  # Para obtener el ID antes del commit

        # Vincular al mentor creador automáticamente
        relacion = UsuarioConvocatoria(
            usuario_id=mentor_id,
            convocatoria_id=nueva.id,
            rol_en_convocatoria='Mentor',
            estado_validacion='Aprobado',
        )
        db.session.add(relacion)
        db.session.commit()
        return nueva

class ListarConvocatorias:
    """Caso de uso: Listar convocatorias (con filtros opcionales)."""

    def execute(self, solo_activas: bool = False, solo_publicas: bool = False) -> List[Convocatoria]:
        query = Convocatoria.query
        if solo_activas:
            query = query.filter_by(estado='Activa')
        if solo_publicas:
            query = query.filter_by(visibilidad='Pública')
        return query.order_by(Convocatoria.fecha_creacion.desc()).all()

class ObtenerConvocatoria:
    """Caso de uso: Obtener detalle de una convocatoria por ID."""

    def execute(self, convocatoria_id: int) -> Optional[Convocatoria]:
        return db.session.get(Convocatoria, convocatoria_id)

class EditarConvocatoria:
    """Caso de uso: Editar una convocatoria existente (solo el Mentor creador o Admin)."""

    def execute(self, convocatoria_id: int, usuario_id: int, es_admin: bool, **kwargs) -> Convocatoria:
        convocatoria = db.session.get(Convocatoria, convocatoria_id)
        if not convocatoria:
            raise ValueError("Convocatoria no encontrada.")

        # Verificar permisos: solo mentores de la convocatoria o admins
        if not es_admin:
            relacion = UsuarioConvocatoria.query.filter_by(
                usuario_id=usuario_id,
                convocatoria_id=convocatoria_id,
                rol_en_convocatoria='Mentor',
            ).first()
            if not relacion:
                raise PermissionError("No tienes permisos para editar esta convocatoria.")

        for campo, valor in kwargs.items():
            if hasattr(convocatoria, campo) and valor is not None:
                setattr(convocatoria, campo, valor)

        db.session.commit()
        return convocatoria

class EliminarConvocatoria:
    """Caso de uso: Eliminar una convocatoria (solo Admin)."""

    def execute(self, convocatoria_id: int, es_admin: bool) -> bool:
        if not es_admin:
            raise PermissionError("Solo los administradores pueden eliminar convocatorias.")
        convocatoria = db.session.get(Convocatoria, convocatoria_id)
        if not convocatoria:
            raise ValueError("Convocatoria no encontrada.")
        db.session.delete(convocatoria)
        db.session.commit()
        return True
