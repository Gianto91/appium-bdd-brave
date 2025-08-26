from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

@given("que abro Brave en el dispositivo")
def step_open_brave(context):
    # Brave ya se abre en before_scenario
    time.sleep(2)

@when('busco "Appium" en Google')
def step_search_google(context):
    search_box = context.driver.find_element(By.NAME, "q")
    search_box.send_keys("Appium")
    search_box.send_keys(Keys.ENTER)
    time.sleep(3)

@then("debería ver resultados en la página")
def step_validate_results(context):
    results = context.driver.find_elements(By.CSS_SELECTOR, "h3")
    assert len(results) > 0, "No se encontraron resultados en Google"
