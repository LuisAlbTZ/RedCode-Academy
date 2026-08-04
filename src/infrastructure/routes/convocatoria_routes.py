"""
Blueprint de Convocatorias: CRUD, participar, validar, asignar jurado.
"""
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from src.application.use_cases.convocatoria_actions import (
    CrearConvocatoria, ListarConvocatorias,
    ObtenerConvocatoria
)
from src.application.use_cases.participacion_actions import (
    PostularConvocatoria, ValidarParticipante,
    AsignarJurado, ListarParticipantes
)
from src.application.use_cases.calificacion_actions import DecidirGanador

convocatoria_bp = Blueprint('convocatoria', __name__, url_prefix='/convocatorias')


@convocatoria_bp.route('/')
@login_required
def listar():
    """Listar todas las convocatorias activas."""
    uc = ListarConvocatorias()
    convocatorias = uc.execute(solo_activas=True)
    return render_template('convocatorias.html', convocatorias=convocatorias)


@convocatoria_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    """Crear una nueva convocatoria (cualquier usuario autenticado puede ser Mentor)."""
    if request.method == 'POST':
        try:
            fecha_inicio = datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%dT%H:%M')
            fecha_fin = datetime.strptime(request.form['fecha_fin'], '%Y-%m-%dT%H:%M')

            uc = CrearConvocatoria()
            conv = uc.execute(
                mentor_id=current_user.id,
                titulo=request.form['titulo'],
                descripcion=request.form['descripcion'],
                visibilidad=request.form.get('visibilidad', 'Pública'),
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                reglas=request.form['reglas'],
                especificaciones=request.form['especificaciones'],
                indicaciones=request.form['indicaciones'],
                metricas_evaluacion=request.form['metricas_evaluacion'],
                modalidad=request.form.get('modalidad', 'Individual'),
                costo=float(request.form.get('costo', 0)),
                tecnologias_sugeridas=request.form.get('tecnologias_sugeridas'),
                patrocinadores=request.form.get('patrocinadores'),
                min_participantes=int(request.form.get('min_participantes', 1)),
                max_participantes=int(request.form.get('max_participantes', 1)),
            )
            flash('¡Convocatoria creada exitosamente!', 'success')
            return redirect(url_for('convocatoria.detalle', convocatoria_id=conv.id))
        except Exception as e:
            flash(f'Error al crear convocatoria: {str(e)}', 'error')

    return render_template('crear_convocatoria.html')


@convocatoria_bp.route('/<int:convocatoria_id>')
@login_required
def detalle(convocatoria_id: int):
    """Detalle de una convocatoria específica."""
    uc = ObtenerConvocatoria()
    conv = uc.execute(convocatoria_id)
    if not conv:
        abort(404)

    listar_uc = ListarParticipantes()
    participantes = listar_uc.execute(convocatoria_id)

    # Verificar el rol del usuario actual en esta convocatoria
    from src.infrastructure.models.models import UsuarioConvocatoria
    mi_relacion = UsuarioConvocatoria.query.filter_by(
        usuario_id=current_user.id,
        convocatoria_id=convocatoria_id,
    ).first()

    # Ganador
    ganador_result = None
    if conv.estado == 'Finalizada':
        ganador_uc = DecidirGanador()
        ganador_result = ganador_uc.execute(convocatoria_id)

    return render_template(
        'convocatoria_detail.html',
        conv=conv,
        participantes=participantes,
        mi_relacion=mi_relacion,
        ganador_result=ganador_result,
    )


@convocatoria_bp.route('/<int:convocatoria_id>/participar', methods=['POST'])
@login_required
def participar(convocatoria_id: int):
    """Inscribirse como Aprendiz en una convocatoria."""
    try:
        uc = PostularConvocatoria()
        uc.execute(current_user.id, convocatoria_id)
        flash('¡Te has inscrito exitosamente! Espera la aprobación del Mentor.', 'success')
    except (ValueError, PermissionError) as e:
        flash(str(e), 'error')
    return redirect(url_for('convocatoria.detalle', convocatoria_id=convocatoria_id))


@convocatoria_bp.route('/<int:convocatoria_id>/validar/<int:usuario_id>', methods=['POST'])
@login_required
def validar_participante(convocatoria_id: int, usuario_id: int):
    """Mentor aprueba o rechaza un participante."""
    nuevo_estado = request.form.get('estado', 'Aprobado')
    try:
        uc = ValidarParticipante()
        uc.execute(current_user.id, usuario_id, convocatoria_id, nuevo_estado)
        flash(f'Participante {nuevo_estado.lower()} exitosamente.', 'success')
    except (ValueError, PermissionError) as e:
        flash(str(e), 'error')
    return redirect(url_for('convocatoria.detalle', convocatoria_id=convocatoria_id))


@convocatoria_bp.route('/<int:convocatoria_id>/jurado/<int:usuario_id>', methods=['POST'])
@login_required
def asignar_jurado(convocatoria_id: int, usuario_id: int):
    """Mentor asigna rol de Jurado a un usuario."""
    try:
        uc = AsignarJurado()
        uc.execute(current_user.id, usuario_id, convocatoria_id)
        flash('Jurado asignado exitosamente.', 'success')
    except (ValueError, PermissionError) as e:
        flash(str(e), 'error')
    return redirect(url_for('convocatoria.detalle', convocatoria_id=convocatoria_id))
