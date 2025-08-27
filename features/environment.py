from appium.options.android import UiAutomator2Options
from appium import webdriver

def before_scenario(context, scenario):
    caps = {
        "sessionName": "Prueba Chrome en Kobiton2",
        "sessionDescription": "Ejecutando Behave con Appium en Chrome",
        "deviceGroup": "KOBITON",
        "deviceName": "*",  # cualquier dispositivo disponible
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "browserName": "Chrome",  # usar navegador en lugar de apk
        "noReset": True
    }

    print("=== Capabilities que se envían a Kobiton ===")
    print(caps)

    kobiton_url = "https://{username}:{apiKey}@api.kobiton.com/wd/hub".format(
        username="gmpc91",
        apiKey="82f6c035-11a0-4288-a228-cb0bcc36d2ad"
    )

    options = UiAutomator2Options()
    for key, value in caps.items():
        options.set_capability(key, value)

    context.driver = webdriver.Remote(
        command_executor=kobiton_url,
        options=options
    )

def after_scenario(context, scenario):
    """Cerrar sesión en Kobiton después de cada escenario"""
    if hasattr(context, "driver"):
        try:
            context.driver.quit()
            print("✅ Sesión en Kobiton cerrada correctamente")
        except Exception as e:
            print(f"⚠️ Error al cerrar la sesión: {e}")
