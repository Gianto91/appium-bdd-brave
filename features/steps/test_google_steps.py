# features/steps/google_steps.py
from behave import given, when, then
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.google_page import GooglePage

@given('abro Google en el navegador')
def step_open_google(context):
    context.google = GooglePage(context.driver)
    context.google.open()  # maneja consentimiento si aparece

@when('busco "{texto}"')
def step_search(context, texto):
    context.query = texto
    context.google.search(texto)
    print("🔎 URL tras búsqueda:", context.driver.current_url)
    print("🔎 Título:", context.driver.title)


@then('veo resultados relacionados con "{texto}"')
def step_results(context, texto):
    # Verificación robusta: título y contenedor de resultados
    WebDriverWait(context.driver, 20).until(EC.title_contains(texto))
    assert context.google.results_loaded(), "No se cargó el contenedor de resultados"
    assert texto.lower() in context.driver.title.lower(), f'El título no contiene "{texto}"'
