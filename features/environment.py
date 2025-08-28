from appium.options.android import UiAutomator2Options
from appium import webdriver
import os

def before_scenario(context, scenario):
    caps = {
        "sessionName": "Prueba Chrome en Kobiton2",
        "sessionDescription": "Ejecutando Behave con Appium en Chrome",
        "deviceGroup": "KOBITON",
        "deviceName": "*",  # cualquier dispositivo disponible
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "browserName": "Chrome",  # navegador en vez de apk
        "noReset": True,

        # 🔧 Extras recomendados para estabilidad
        "chromedriverAutodownload": True,      # que baje el chromedriver correcto
        "newCommandTimeout": 300,              # tiempo de vida de sesión
        "uiautomator2ServerLaunchTimeout": 60000,
        "adbExecTimeout": 60000,
        "autoGrantPermissions": True,          # permisos automáticos

        # 🔧 Configuración de Chrome
        "goog:chromeOptions": {
            "args": [
                "--disable-fre",               # evitar pantalla de primera vez
                "--no-first-run",
                "--disable-popup-blocking",
                "--disable-notifications",
                "--lang=en-US"                 # forzar idioma consistente
            ]
        }
    }

    print("=== Capabilities que se envían a Kobiton ===")
    print(caps)

    kobiton_url = "https://{username}:{apiKey}@api.kobiton.com/wd/hub".format(
        username=os.getenv("KOBITON_USERNAME", "gmpc91"),
        apiKey=os.getenv("KOBITON_API_KEY", "82f6c035-11a0-4288-a228-cb0bcc36d2ad")
    )

    options = UiAutomator2Options().load_capabilities(caps)

    try:
        context.driver = webdriver.Remote(
            command_executor=kobiton_url,
            options=options
        )
        print("🚀 Sesión iniciada en Kobiton")
    except Exception as e:
        print(f"❌ Error al iniciar sesión en Kobiton: {e}")
        context.driver = None


def after_scenario(context, scenario):
    if getattr(context, "driver", None):
        if scenario.status == "failed":
            try:
                os.makedirs("artifacts", exist_ok=True)
                name = scenario.name.replace(" ", "_")
                # URL y título
                try:
                    print(f"❗ current_url: {context.driver.current_url}")
                    print(f"❗ title: {context.driver.title}")
                except Exception:
                    pass
                # captura
                context.driver.save_screenshot(f"artifacts/{name}.png")
                with open(f"artifacts/{name}.html", "w", encoding="utf-8") as f:
                    f.write(context.driver.page_source)
                print(f"📸 artifacts/{name}.png")
                print(f"📄 artifacts/{name}.html")
            except Exception as e:
                print(f"⚠️ No se pudieron guardar artefactos: {e}")
        try:
            context.driver.quit()
            print("✅ Sesión en Kobiton cerrada correctamente")
        except Exception as e:
            print(f"⚠️ Error al cerrar la sesión: {e}")