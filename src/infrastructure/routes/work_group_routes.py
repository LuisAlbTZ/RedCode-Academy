"""
Blueprint de WorkGroups: subir código, ver, votar, comentar, calificar.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, jsonify
from flask_login import login_required, current_user

from src.application.use_cases.work_group_actions import (
    CrearWorkGroup, ListarWorkGroups ,
    ObtenerWorkGroup, VotarWorkGroup
)
from src.application.use_cases.comentario_actions import CrearComentario, ListarComentarios
from src.application.use_cases.calificacion_actions import CalificarWorkGroup

work_group_bp = Blueprint('work_group', __name__, url_prefix='/work-group')

@work_group_bp.route('/')
@login_required
def listar():
    """Listar todas las mesas de trabajo (WorkGroups)."""
    uc = ListarWorkGroups()
    work_groups = uc.execute()
    return render_template('work_groups.html', work_groups=work_groups)


@work_group_bp.route('/crear/<int:convocatoria_id>', methods=['GET', 'POST'])
@login_required
def crear(convocatoria_id: int):
    """Aprendiz sube su entregable/código."""
    if request.method == 'POST':
        try:
            uc = CrearWorkGroup()
            wg = uc.execute(
                usuario_id=current_user.id,
                convocatoria_id=convocatoria_id,
                titulo=request.form['titulo'],
                descripcion_texto=request.form.get('descripcion_texto'),
                contenido_codigo=request.form.get('contenido_codigo'),
                enlace_repositorio=request.form.get('enlace_repositorio'),
            )
            flash('¡Entregable publicado exitosamente!', 'success')
            return redirect(url_for('work_group.detalle', work_group_id=wg.id))
        except (ValueError, PermissionError) as e:
            flash(str(e), 'error')

    from src.application.use_cases.convocatoria_actions import ObtenerConvocatoria
    conv = ObtenerConvocatoria().execute(convocatoria_id)
    if not conv:
        abort(404)
    return render_template('crear_work_group.html', conv=conv)


@work_group_bp.route('/<int:work_group_id>')
@login_required
def detalle(work_group_id: int):
    """Ver detalle de un WorkGroup con comentarios y calificaciones."""
    uc = ObtenerWorkGroup()
    wg = uc.execute(work_group_id)
    if not wg:
        abort(404)

    comentarios = ListarComentarios().execute(work_group_id)

    # Rol del usuario actual en la convocatoria de este WG
    from src.infrastructure.models.models import UsuarioConvocatoria
    mi_relacion = UsuarioConvocatoria.query.filter_by(
        usuario_id=current_user.id,
        convocatoria_id=wg.convocatoria_id,
    ).first()

    return render_template(
        'work_group_detail.html',
        wg=wg,
        comentarios=comentarios,
        mi_relacion=mi_relacion,
    )


@work_group_bp.route('/<int:work_group_id>/votar', methods=['POST'])
@login_required
def votar(work_group_id: int):
    """Votar upvote o downvote en un WorkGroup (responde JSON para AJAX)."""
    direccion = request.json.get('direccion', 'up') if request.is_json else request.form.get('direccion', 'up')
    try:
        uc = VotarWorkGroup()
        wg = uc.execute(work_group_id, direccion)
        if request.is_json:
            return jsonify({'puntuacion': wg.puntuacion, 'ok': True})
        flash('Voto registrado.', 'success')
    except (ValueError, PermissionError) as e:
        if request.is_json:
            return jsonify({'error': str(e), 'ok': False}), 400
        flash(str(e), 'error')
    return redirect(url_for('work_group.detalle', work_group_id=work_group_id))


@work_group_bp.route('/<int:work_group_id>/comentar', methods=['POST'])
@login_required
def comentar(work_group_id: int):
    """Agregar un comentario a un WorkGroup."""
    contenido = request.form.get('contenido', '').strip()
    if not contenido:
        flash('El comentario no puede estar vacío.', 'error')
        return redirect(url_for('work_group.detalle', work_group_id=work_group_id))

    try:
        uc = CrearComentario()
        uc.execute(current_user.id, work_group_id, contenido)
        flash('Comentario publicado.', 'success')
    except ValueError as e:
        flash(str(e), 'error')

    return redirect(url_for('work_group.detalle', work_group_id=work_group_id))


@work_group_bp.route('/<int:work_group_id>/calificar', methods=['POST'])
@login_required
def calificar(work_group_id: int):
    """Jurado califica una entrega."""
    try:
        calificacion = int(request.form.get('calificacion', 0))
        uc = CalificarWorkGroup()
        uc.execute(current_user.id, work_group_id, calificacion)
        flash('Calificación registrada exitosamente.', 'success')
    except (ValueError, PermissionError) as e:
        flash(str(e), 'error')

    return redirect(url_for('work_group.detalle', work_group_id=work_group_id))
