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