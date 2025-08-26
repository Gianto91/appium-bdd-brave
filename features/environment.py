from appium import webdriver
from appium.options.android import UiAutomator2Options

def before_scenario(context, scenario):
    caps = {
        "platformName": "Android",
        "platformVersion": "15",
        "deviceName": "R5CX11BALPY",
        "automationName": "UiAutomator2",
        "appPackage": "com.brave.browser",
        "appActivity": "org.chromium.chrome.browser.ChromeTabbedActivity",
        "appWaitPackage": "com.brave.browser",
        "appWaitActivity": "org.chromium.chrome.browser.ChromeTabbedActivity",
        "noReset": True
    }

    options = UiAutomator2Options().load_capabilities(caps)

    context.driver = webdriver.Remote(
        command_executor="http://127.0.0.1:4723",
        options=options
    )

def after_scenario(context, scenario):
    if hasattr(context, "driver"):
        context.driver.quit()
