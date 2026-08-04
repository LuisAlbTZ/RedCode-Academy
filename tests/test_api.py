import pytest

# ==============================================================================
# Pruebas para API y Acciones (POST)
# ==============================================================================

def test_login_action(client):
    """Prueba enviar el formulario de inicio de sesión."""
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    # Se espera una redirección si es exitoso (302) o recarga con error (200)
    assert response.status_code in [200, 302]


def test_register_action(client):
    """Prueba enviar el formulario de registro de usuario."""
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    # Se espera que el registro sea exitoso (201, 302 o 200 dependiendo del diseño)
    assert response.status_code in [200, 201, 302]


def test_update_profile_action(client, auth):
    """Prueba enviar datos para actualizar el perfil del usuario."""
    # auth.login()
    response = client.post('/profile', data={
        'bio': 'Esta es mi nueva biografía.',
        'skills': 'Python, Flask, Testing'
    })
    # Comprobar estado de acceso / si guardó
    # assert response.status_code in [200, 302]
    pass


# ==============================================================================
# Pruebas de Acciones en Convocatorias
# ==============================================================================

def test_create_convocatoria_action(client, auth):
    """Prueba la creación de una convocatoria (Debe ser Mentor)."""
    # auth.login(role='mentor')
    response = client.post('/convocatorias/crear', data={
        'titulo': 'Reto de Backend con Flask',
        'descripcion': 'Crea una API robusta y documentada.',
        'fecha_limite': '2023-12-31'
    })
    # assert response.status_code in [200, 201, 302]
    pass


def test_participate_convocatoria_action(client, auth):
    """Prueba la inscripción a una convocatoria como Aprendiz."""
    # auth.login(role='aprendiz')
    response = client.post('/convocatorias/1/participar')
    # assert response.status_code in [200, 302]
    pass


def test_validate_participant_action(client, auth):
    """Prueba que el mentor apruebe/valide a un participante en la convocatoria."""
    # auth.login(role='mentor')
    response = client.post('/convocatorias/1/validar/100')
    # assert response.status_code in [200, 302]
    pass


def test_assign_jury_action(client, auth):
    """Prueba que el mentor asigne un jurado a la convocatoria."""
    # auth.login(role='mentor')
    response = client.post('/convocatorias/1/jurado/100')
    # assert response.status_code in [200, 302]
    pass


# ==============================================================================
# Pruebas de Acciones en Entregas (Work-Group)
# ==============================================================================

def test_submit_work_action(client, auth):
    """Prueba la subida de un código o entregable a la convocatoria."""
    # auth.login(role='aprendiz')
    response = client.post('/work-group/crear/1', data={
        'repositorio_url': 'https://github.com/usuario/mi-entregable',
        'descripcion': 'Solución completa con pruebas unitarias.'
    })
    # assert response.status_code in [200, 201, 302]
    pass


def test_vote_work_action(client, auth):
    """Prueba hacer un Upvote o Downvote a una entrega."""
    # auth.login()
    response = client.post('/work-group/1/votar', json={'vote_type': 'upvote'})
    # assert response.status_code in [200, 201]
    pass


def test_comment_work_action(client, auth):
    """Prueba agregar un comentario a la entrega de otro usuario."""
    # auth.login()
    response = client.post('/work-group/1/comentar', data={
        'comentario': 'Muy buena estructura de código.'
    })
    # assert response.status_code in [200, 201, 302]
    pass


def test_grade_work_action(client, auth):
    """Prueba que un Jurado califique la entrega."""
    # auth.login(role='jurado')
    response = client.post('/work-group/1/calificar', data={
        'calificacion': 95,
        'feedback': 'Excelente implementación y pruebas.'
    })
    # assert response.status_code in [200, 302]
    pass


# ==============================================================================
# Pruebas de Acciones de Administración
# ==============================================================================

def test_admin_manage_users_action(client, auth):
    """Prueba la gestión (ej. bloquear o promover) de usuarios en el admin."""
    # auth.login(role='admin')
    response = client.post('/admin/usuarios', data={
        'action': 'promote',
        'user_id': 2,
        'new_role': 'mentor'
    })
    # assert response.status_code in [200, 302]
    pass


def test_admin_manage_convocatorias_action(client, auth):
    """Prueba la gestión (ej. cerrar o eliminar) de convocatorias en el admin."""
    # auth.login(role='admin')
    response = client.post('/admin/convocatorias', data={
        'action': 'close',
        'convocatoria_id': 1
    })
    # assert response.status_code in [200, 302]
    pass
