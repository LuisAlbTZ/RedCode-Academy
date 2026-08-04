"""
Blueprint principal: /, /dashboard, /profile
"""
from datetime import datetime
from flask import Blueprint, render_template, request, url_for, flash
from flask_login import login_required, current_user

from src.application.use_cases.usuarios_actions import ObtenerUsuario, ActualizarUsuario
from src.application.use_cases.convocatoria_actions import ListarConvocatorias
from src.application.use_cases.work_group_actions import ListarWorkGroups

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Landing page principal."""
    return render_template('index.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Feed principal tipo Reddit — requiere sesión activa."""
    # Cargar work groups más recientes con su puntuación
    listar_wg = ListarWorkGroups()
    work_groups = listar_wg.execute()

    # Cargar convocatorias activas
    listar_conv = ListarConvocatorias()
    convocatorias_activas = listar_conv.execute(solo_activas=True, solo_publicas=True)[:5]

    return render_template(
        'dashboard.html',
        work_groups=work_groups,
        convocatorias_activas=convocatorias_activas,
    )

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Actualiza el perfil del usuario."""
    
    uc_obtener = ObtenerUsuario()
    usuario = uc_obtener.execute(current_user.id)
    
    if request.method == 'POST':
        try:
            # Extraer los datos del formulario
            nombre = request.form.get('nombre')
            apellido = request.form.get('apellido')
            correo_electronico = request.form.get('correo_electronico')
            fecha_nacimiento_str = request.form.get('fecha_nacimiento')
            
            # Convertir la cadena de fecha del formulario HTML a un objeto de fecha de Python
            fecha_nacimiento = None
            if fecha_nacimiento_str:
                fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()

            # Actualiza el usuario
            uc_actualizar = ActualizarUsuario()
            uc_actualizar.execute(
                usuario_id=current_user.id,
                nombre=nombre,
                apellido=apellido,
                correo_electronico=correo_electronico,
                fecha_nacimiento=fecha_nacimiento
            )
            flash('Perfil actualizado exitosamente.', 'success')
            
            # Actualiza el objeto de usuario para que la plantilla muestre los datos recién actualizados
            usuario = uc_obtener.execute(current_user.id)
            
        except ValueError as ve:
            # Detecta errores específicos de validación (como correo electrónico ya registrado)
            flash(str(ve), 'error')
        except Exception as e:
            # Detecta cualquier otro error
            flash(f'Error al actualizar el perfil: {str(e)}', 'error')
    
    from src.infrastructure.models.models import UsuarioConvocatoria
    mis_convocatorias = UsuarioConvocatoria.query.filter_by(
        usuario_id=current_user.id
    ).all()
    
    # Pasar el objeto 'usuario' junto con 'mis_convocatorias'
    return render_template('profile.html', usuario=usuario, mis_convocatorias=mis_convocatorias)