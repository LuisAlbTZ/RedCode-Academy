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
# Cambiar de localhost al nombre del servicio definido en Docker

# ==============================================================================
# Pruebas de Páginas Públicas — Carga y Contenido
# ==============================================================================

class TestBasicE2E:
    """Clase que agrupa tests básicos de End-to-End"""
    # Abrir navegador y ir a la pagina principal
    def test_homepage_loads(self, selenium_driver, e2e_base_url, flask_test_app):
        """Test E2E: La página principal carga correctamente"""
        selenium_driver.get(e2e_base_url)