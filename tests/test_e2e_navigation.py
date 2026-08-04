"""
Pruebas E2E de navegación con Selenium WebDriver.

Estas pruebas verifican la navegación real del usuario en el navegador,
incluyendo clics en enlaces, redirecciones y contenido visible en las páginas.

Requisitos:
    - selenium
    - Un navegador compatible (Chrome) con su driver (chromedriver)
    - La aplicación Flask corriendo (por defecto en http://localhost:5000)

Ejecución:
    pytest tests/test_e2e_navigation.py -v
"""
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ==============================================================================
# Configuración y Fixtures
# ==============================================================================

BASE_URL = "http://localhost:5000"


@pytest.fixture(scope="module")
def driver():
    """
    Inicializa y cierra el navegador Chrome en modo headless para las pruebas.
    Se usa scope='module' para reutilizar la misma instancia del navegador
    en todas las pruebas de este módulo (más rápido).
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    browser = webdriver.Chrome(options=chrome_options)
    browser.implicitly_wait(5)  # Espera implícita de 5 segundos

    yield browser

    browser.quit()


# ==============================================================================
# Pruebas de Páginas Públicas — Carga y Contenido
# ==============================================================================

class TestPublicPagesLoad:
    """Verifica que las páginas públicas cargan correctamente y muestran el contenido esperado."""

    def test_index_page_loads(self, driver):
        """La página principal (landing) carga y muestra el título de RedCode Academy."""
        driver.get(f"{BASE_URL}/")
        assert "RedCode" in driver.title
        # Verificar que el encabezado principal está presente
        heading = driver.find_element(By.TAG_NAME, "h1")
        assert heading.is_displayed()

    def test_index_page_has_login_link(self, driver):
        """La landing page contiene un enlace/botón de 'Iniciar Sesión'."""
        driver.get(f"{BASE_URL}/")
        links = driver.find_elements(By.TAG_NAME, "a")
        login_texts = [link.text for link in links]
        assert any("Iniciar" in text for text in login_texts), (
            "No se encontró un enlace de 'Iniciar Sesión' en la página principal"
        )

    def test_index_page_has_register_link(self, driver):
        """La landing page contiene un enlace/botón de 'Registrarte'."""
        driver.get(f"{BASE_URL}/")
        links = driver.find_elements(By.TAG_NAME, "a")
        register_texts = [link.text for link in links]
        assert any("Regist" in text for text in register_texts), (
            "No se encontró un enlace de 'Registrarte' en la página principal"
        )

    def test_login_page_loads(self, driver):
        """La página de login carga y muestra el formulario."""
        driver.get(f"{BASE_URL}/login")
        assert "Iniciar" in driver.title or "login" in driver.current_url.lower()
        # Verificar que el formulario de login está presente
        form = driver.find_element(By.TAG_NAME, "form")
        assert form.is_displayed()

    def test_login_page_has_email_field(self, driver):
        """La página de login tiene un campo de correo electrónico."""
        driver.get(f"{BASE_URL}/login")
        email_input = driver.find_element(By.ID, "email")
        assert email_input.is_displayed()
        assert email_input.get_attribute("type") == "email"

    def test_login_page_has_password_field(self, driver):
        """La página de login tiene un campo de contraseña."""
        driver.get(f"{BASE_URL}/login")
        password_input = driver.find_element(By.ID, "password")
        assert password_input.is_displayed()
        assert password_input.get_attribute("type") == "password"

    def test_register_page_loads(self, driver):
        """La página de registro carga correctamente."""
        driver.get(f"{BASE_URL}/register")
        # Verificar que estamos en la página de registro
        assert "register" in driver.current_url.lower() or "Regist" in driver.page_source
        form = driver.find_element(By.TAG_NAME, "form")
        assert form.is_displayed()


# ==============================================================================
# Pruebas de Navegación entre Páginas
# ==============================================================================

class TestNavigation:
    """Verifica que los enlaces de navegación funcionan correctamente."""

    def test_navigate_from_index_to_login(self, driver):
        """Desde la landing, hacer clic en 'Iniciar Sesión' lleva a /login."""
        driver.get(f"{BASE_URL}/")
        # Buscar el enlace de Iniciar Sesión
        links = driver.find_elements(By.TAG_NAME, "a")
        login_link = None
        for link in links:
            if "Iniciar" in link.text:
                login_link = link
                break

        assert login_link is not None, "No se encontró el enlace de 'Iniciar Sesión'"
        login_link.click()

        WebDriverWait(driver, 10).until(EC.url_contains("/login"))
        assert "/login" in driver.current_url

    def test_navigate_from_index_to_register(self, driver):
        """Desde la landing, hacer clic en 'Registrarte' lleva a /register."""
        driver.get(f"{BASE_URL}/")
        links = driver.find_elements(By.TAG_NAME, "a")
        register_link = None
        for link in links:
            if "Regist" in link.text:
                register_link = link
                break

        assert register_link is not None, "No se encontró el enlace de 'Registrarte'"
        register_link.click()

        WebDriverWait(driver, 10).until(EC.url_contains("/register"))
        assert "/register" in driver.current_url

    def test_navigate_from_login_to_register(self, driver):
        """Desde la página de login, el enlace '¿No tienes cuenta?' lleva a /register."""
        driver.get(f"{BASE_URL}/login")
        # Buscar el enlace de registro en el formulario de login
        links = driver.find_elements(By.TAG_NAME, "a")
        register_link = None
        for link in links:
            if "Regístrate" in link.text or "Registr" in link.text:
                register_link = link
                break

        assert register_link is not None, "No se encontró el enlace de registro en la página de login"
        register_link.click()

        WebDriverWait(driver, 10).until(EC.url_contains("/register"))
        assert "/register" in driver.current_url

    def test_navigate_from_login_to_index_via_logo(self, driver):
        """Desde login, hacer clic en el logo 'RedCode Academy' regresa a la landing (/)."""
        driver.get(f"{BASE_URL}/login")
        # El logo es un enlace con texto 'RedCode Academy'
        logo_links = driver.find_elements(By.TAG_NAME, "a")
        logo_link = None
        for link in logo_links:
            if "RedCode" in link.text:
                logo_link = link
                break

        assert logo_link is not None, "No se encontró el logo/enlace de 'RedCode Academy'"
        logo_link.click()

        WebDriverWait(driver, 10).until(
            lambda d: d.current_url.rstrip("/") == BASE_URL or d.current_url == f"{BASE_URL}/"
        )
        assert driver.current_url.rstrip("/") == BASE_URL or driver.current_url == f"{BASE_URL}/"


# ==============================================================================
# Pruebas de Rutas Protegidas — Redirección
# ==============================================================================

class TestProtectedRouteRedirects:
    """Verifica que las rutas protegidas redirigen al login cuando no hay sesión activa."""

    @pytest.mark.parametrize("protected_route", [
        "/dashboard",
        "/profile",
        "/convocatorias/",
    ])
    def test_protected_route_redirects_to_login(self, driver, protected_route):
        """
        Al intentar acceder a una ruta protegida sin autenticación,
        el navegador debe redirigir a la página de login o mostrar un 401.
        """
        driver.get(f"{BASE_URL}{protected_route}")
        # Después de la redirección, verificar que estamos en login o en una página de error
        current_url = driver.current_url.lower()
        page_source = driver.page_source.lower()

        is_on_login = "/login" in current_url
        is_on_error = "401" in page_source or "no autorizado" in page_source or "302" in page_source

        assert is_on_login or is_on_error, (
            f"Se esperaba redirección a login o error 401 para {protected_route}, "
            f"pero la URL actual es: {driver.current_url}"
        )

    @pytest.mark.parametrize("admin_route", [
        "/admin",
        "/admin/usuarios",
        "/admin/convocatorias",
    ])
    def test_admin_routes_not_accessible_unauthenticated(self, driver, admin_route):
        """
        Las rutas de administración no deben ser accesibles sin autenticación.
        Se espera redirección al login o un error 401/403.
        """
        driver.get(f"{BASE_URL}{admin_route}")
        current_url = driver.current_url.lower()
        page_source = driver.page_source.lower()

        is_on_login = "/login" in current_url
        is_on_error = (
            "401" in page_source
            or "403" in page_source
            or "no autorizado" in page_source
            or "prohibido" in page_source
        )

        assert is_on_login or is_on_error, (
            f"Se esperaba restricción de acceso para {admin_route}, "
            f"pero la URL actual es: {driver.current_url}"
        )


# ==============================================================================
# Pruebas de Interacción con Formularios
# ==============================================================================

class TestLoginFormInteraction:
    """Verifica la interacción básica con el formulario de login."""

    def test_login_form_empty_submission(self, driver):
        """
        Enviar el formulario de login vacío no debe llevar al dashboard.
        El navegador valida los campos required del HTML.
        """
        driver.get(f"{BASE_URL}/login")
        # Intentar enviar sin datos — el navegador bloqueará por los campos 'required'
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # Debemos seguir en la página de login
        assert "/login" in driver.current_url or "Iniciar" in driver.page_source

    def test_login_form_can_type_email(self, driver):
        """Se puede escribir en el campo de correo electrónico."""
        driver.get(f"{BASE_URL}/login")
        email_input = driver.find_element(By.ID, "email")
        email_input.clear()
        email_input.send_keys("test@example.com")
        assert email_input.get_attribute("value") == "test@example.com"

    def test_login_form_can_type_password(self, driver):
        """Se puede escribir en el campo de contraseña."""
        driver.get(f"{BASE_URL}/login")
        password_input = driver.find_element(By.ID, "password")
        password_input.clear()
        password_input.send_keys("mi_password_123")
        assert password_input.get_attribute("value") == "mi_password_123"

    def test_login_with_invalid_credentials(self, driver):
        """
        Al enviar credenciales inválidas, el usuario permanece en login
        y no llega al dashboard.
        """
        driver.get(f"{BASE_URL}/login")

        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        email_input.clear()
        email_input.send_keys("usuario_inexistente@test.com")
        password_input.clear()
        password_input.send_keys("contraseña_incorrecta")
        submit_button.click()

        # Esperar a que la página procese
        WebDriverWait(driver, 10).until(
            lambda d: "/login" in d.current_url or "/dashboard" not in d.current_url
        )

        # No debe haber llegado al dashboard
        assert "/dashboard" not in driver.current_url, (
            "El usuario con credenciales inválidas no debería acceder al dashboard"
        )


# ==============================================================================
# Pruebas de Contenido de Página
# ==============================================================================

class TestPageContent:
    """Verifica que el contenido esperado está presente en las páginas."""

    def test_index_has_academy_branding(self, driver):
        """La página principal muestra el branding de 'RedCode Academy'."""
        driver.get(f"{BASE_URL}/")
        assert "RedCode" in driver.page_source
        assert "Academy" in driver.page_source

    def test_index_has_philosophy_section(self, driver):
        """La landing page muestra la sección de 'Filosofía'."""
        driver.get(f"{BASE_URL}/")
        assert "Filosof" in driver.page_source

    def test_index_has_community_section(self, driver):
        """La landing page muestra la sección de comunidad."""
        driver.get(f"{BASE_URL}/")
        assert "comunidad" in driver.page_source.lower()

    def test_index_has_footer(self, driver):
        """La landing page tiene un footer con derechos reservados."""
        driver.get(f"{BASE_URL}/")
        footer = driver.find_element(By.TAG_NAME, "footer")
        assert footer.is_displayed()
        assert "RedCode Academy" in footer.text

    def test_404_page_for_nonexistent_route(self, driver):
        """Navegar a una ruta inexistente muestra una página 404."""
        driver.get(f"{BASE_URL}/ruta-que-no-existe-xyz")
        page_source = driver.page_source.lower()
        assert "404" in page_source or "no encontrad" in page_source, (
            "No se encontró indicador de error 404 en la página"
        )
