"""
Blueprint de autenticación: /login, /register, /logout
"""
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from src.application.use_cases.usuarios_actions import RegistrarUsuario, LoginUsuario

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        correo = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not correo or not password:
            flash('Por favor completa todos los campos.', 'error')
            return render_template('login.html')

        try:
            use_case = LoginUsuario()
            usuario = use_case.execute(correo, password)

            if usuario:
                login_user(usuario, remember=True)
                next_page = request.args.get('next')
                flash(f'¡Bienvenido de vuelta, {usuario.nombre}!', 'success')
                return redirect(next_page or url_for('main.dashboard'))
            else:
                flash('Correo o contraseña incorrectos.', 'error')
        except ValueError as e:
            flash(str(e), 'error')
        except Exception as e:
            flash('Error al iniciar sesión. Inténtalo de nuevo.', 'error')

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro de nuevo usuario."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        apellido = request.form.get('apellido', '').strip()
        fecha_nac_str = request.form.get('fecha_nacimiento', '')
        correo = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirmar = request.form.get('confirm_password', '')

        # Validaciones básicas
        if not all([nombre, apellido, fecha_nac_str, correo, password, confirmar]):
            flash('Por favor completa todos los campos.', 'error')
            return render_template('register.html')

        if password != confirmar:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('register.html')

        if len(password) < 8:
            flash('La contraseña debe tener al menos 8 caracteres.', 'error')
            return render_template('register.html')

        try:
            fecha_nacimiento = datetime.strptime(fecha_nac_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Fecha de nacimiento inválida.', 'error')
            return render_template('register.html')

        try:
            use_case = RegistrarUsuario()
            nuevo = use_case.execute(
                nombre=nombre,
                apellido=apellido,
                fecha_nacimiento=fecha_nacimiento,
                correo_electronico=correo,
                password=password,
            )
            flash('¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        except ValueError as e:
            flash(str(e), 'error')
        except Exception as e:
            flash('Error al crear la cuenta. Inténtalo de nuevo.', 'error')

    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Cerrar sesión."""
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('main.index'))
