import pytest

# ==============================================================================
# Pruebas para Rutas Públicas
# ==============================================================================

@pytest.mark.parametrize("route", [
    "/",
    "/login",
    "/register",
])
def test_public_routes_status_code(client, route):
    """Prueba que las rutas públicas devuelvan un 200 OK y sean accesibles sin login."""
    response = client.get(route)
    assert response.status_code == 200


# ==============================================================================
# Pruebas para Rutas Protegidas (Requieren Autenticación)
# ==============================================================================

@pytest.mark.parametrize("route", [
    "/dashboard",
    "/profile",
    "/convocatorias/",
    "/convocatorias/1",
    "/work-group/1",
])
def test_protected_routes_unauthenticated(client, route):
    """
    Prueba que las rutas protegidas no sean accesibles sin estar autenticado.
    Se espera una redirección (302) al login o un error de no autorizado (401).
    """
    response = client.get(route)
    # Por lo general, Flask-Login redirige con 302 a /login
    assert response.status_code in [302, 401]


def test_protected_routes_authenticated(client, auth):
    """Ejemplo de prueba de rutas autenticadas."""
    # Nota: Descomentar esto cuando la lógica de la base de datos y usuarios esté mockeada
    # auth.login()
    # response = client.get('/dashboard')
    # assert response.status_code == 200
    pass


def test_logout_redirects(client):
    """Prueba que cerrar sesión redirige correctamente (por ejemplo, al Home)."""
    response = client.get('/logout')
    assert response.status_code == 302
