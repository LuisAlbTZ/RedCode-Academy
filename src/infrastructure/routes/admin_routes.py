"""
Blueprint del Panel de Administración (solo usuarios con es_admin=True).
"""
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from src.application.use_cases.admin_actions import (
    GestionarUsuarios, GestionarConvocatoriasAdmin, ModerarContenido
)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorador que exige es_admin=True."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.es_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@login_required
@admin_required
def panel():
    """Panel principal de administración."""
    usuarios_uc = GestionarUsuarios()
    conv_uc = GestionarConvocatoriasAdmin()

    usuarios = usuarios_uc.listar_todos()
    convocatorias = conv_uc.listar_todas()

    stats = {
        'total_usuarios': len(usuarios),
        'total_convocatorias': len(convocatorias),
        'usuarios_activos': sum(1 for u in usuarios if u.estado_cuenta == 'Activo'),
        'conv_activas': sum(1 for c in convocatorias if c.estado == 'Activa'),
    }

    return render_template('admin_panel.html', usuarios=usuarios, convocatorias=convocatorias, stats=stats)


@admin_bp.route('/usuarios')
@login_required
@admin_required
def usuarios():
    """Gestión de usuarios."""
    uc = GestionarUsuarios()
    todos = uc.listar_todos()
    return render_template('admin_usuarios.html', usuarios=todos)


@admin_bp.route('/usuarios/<int:usuario_id>/estado', methods=['POST'])
@login_required
@admin_required
def cambiar_estado_usuario(usuario_id: int):
    """Cambiar el estado de una cuenta de usuario."""
    nuevo_estado = request.form.get('estado')
    try:
        uc = GestionarUsuarios()
        uc.cambiar_estado(usuario_id, nuevo_estado)
        flash(f'Estado de cuenta actualizado a "{nuevo_estado}".', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    return redirect(url_for('admin.panel'))


@admin_bp.route('/usuarios/<int:usuario_id>/admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(usuario_id: int):
    """Promover o revocar permisos de admin."""
    accion = request.form.get('accion', 'promover')
    try:
        uc = GestionarUsuarios()
        if accion == 'promover':
            uc.promover_a_admin(usuario_id)
            flash('Usuario promovido a Administrador.', 'success')
        else:
            uc.revocar_admin(usuario_id)
            flash('Permisos de administrador revocados.', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    return redirect(url_for('admin.panel'))


@admin_bp.route('/convocatorias/<int:convocatoria_id>/estado', methods=['POST'])
@login_required
@admin_required
def cambiar_estado_convocatoria(convocatoria_id: int):
    """Cambiar estado de una convocatoria."""
    nuevo_estado = request.form.get('estado')
    try:
        uc = GestionarConvocatoriasAdmin()
        uc.cambiar_estado(convocatoria_id, nuevo_estado)
        flash(f'Estado de convocatoria actualizado a "{nuevo_estado}".', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    return redirect(url_for('admin.panel'))


@admin_bp.route('/convocatorias/<int:convocatoria_id>/eliminar', methods=['POST'])
@login_required
@admin_required
def eliminar_convocatoria(convocatoria_id: int):
    """Eliminar una convocatoria."""
    try:
        uc = GestionarConvocatoriasAdmin()
        uc.eliminar(convocatoria_id)
        flash('Convocatoria eliminada.', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    return redirect(url_for('admin.panel'))


@admin_bp.route('/comentarios/<int:comentario_id>/eliminar', methods=['POST'])
@login_required
@admin_required
def eliminar_comentario(comentario_id: int):
    """Moderar: eliminar comentario."""
    try:
        uc = ModerarContenido()
        uc.eliminar_comentario(comentario_id)
        flash('Comentario eliminado.', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    return redirect(url_for('admin.panel'))
