# features/pages/google_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GooglePage:
    # ncr = no country redirect; hl=en para uniformidad
    URL = "https://www.google.com/ncr?hl=en"

    # posibles señales de resultados en mobile
    POSSIBLE_RESULTS = [
        (By.ID, "search"),
        (By.ID, "rcnt"),
        (By.CSS_SELECTOR, "a h3"),
        (By.CSS_SELECTOR, "[role='main'] a h3"),
        (By.CSS_SELECTOR, "div[role='heading'] h3"),
        (By.CSS_SELECTOR, "div[data-snhf='0'] h3"),
    ]

    SEARCH_LOCATORS = [
        (By.NAME, "q"),                 # input o textarea con name=q
        (By.CSS_SELECTOR, "textarea[name='q']"),
        (By.CSS_SELECTOR, "input[name='q']"),
    ]

    def __init__(self, driver, timeout=30):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url=None):
        self.driver.get(url or self.URL)
        self._dismiss_consent()

    def _dismiss_consent(self):
        """
        Intenta cerrar consentimiento si aparece:
        - variante iframe
        - variante página completa (top-level)
        - varios idiomas
        Best-effort: si no está, no rompe.
        """
        texts = [
            "I agree", "Accept all", "Agree to all",
            "Acepto", "Acepto todo", "Estoy de acuerdo",
            "J'accepte", "Ich stimme zu", "Akzeptieren",
            "Aceptar todo", "Aceptar"
        ]

        # 1) Intento en iframes
        try:
            iframes = self.driver.find_elements(By.CSS_SELECTOR, "iframe[src*='consent']")
            for iframe in iframes:
                self.driver.switch_to.frame(iframe)
                if self._click_any_text_button(texts):
                    self.driver.switch_to.default_content()
                    return
                self.driver.switch_to.default_content()
        except Exception:
            self.driver.switch_to.default_content()

        # 2) Intento top-level (página completa)
        try:
            if "consent" in self.driver.current_url or "consent.google" in self.driver.current_url:
                self._click_any_text_button(texts)
        except Exception:
            pass

    def _click_any_text_button(self, texts):
        # prueba botones y elementos clicables con esos textos
        candidates = []
        # botones comunes
        candidates += [(By.ID, "L2AGLb")]  # id frecuente “I agree”
        # botones por texto
        for t in texts:
            candidates += [
                (By.XPATH, f"//button[normalize-space()='{t}']"),
                (By.XPATH, f"//span[normalize-space()='{t}']/ancestor::button"),
                (By.XPATH, f"//div[normalize-space()='{t}']/ancestor::button"),
                (By.XPATH, f"//*[self::button or self::div or self::span][contains(., '{t}')]")
            ]
        for how, sel in candidates:
            els = self.driver.find_elements(how, sel)
            if els:
                try:
                    els[0].click()
                    return True
                except Exception:
                    continue
        return False

    def _wait_any_present(self, locators, timeout=30):
        w = WebDriverWait(self.driver, timeout)
        return w.until(lambda d: any(d.find_elements(*loc) for loc in locators))

    def _get_search_box(self):
        for loc in self.SEARCH_LOCATORS:
            found = self.driver.find_elements(*loc)
            if found:
                return found[0]
        # si aún no aparece, espera clickable por el primero
        return self.wait.until(EC.element_to_be_clickable(self.SEARCH_LOCATORS[0]))

    def search(self, text):
        box = self._get_search_box()
        try:
            box.clear()
        except Exception:
            pass
        box.send_keys(text)
        box.send_keys(Keys.ENTER)

        # 1) URL de resultados
        self.wait.until(lambda d: "/search" in d.current_url and "q=" in d.current_url)

        # 2) Título con la query (si tarda, no falla)
        try:
            self.wait.until(EC.title_contains(text))
        except Exception:
            pass

        # 3) Alguna señal de resultados en DOM
        self._wait_any_present(self.POSSIBLE_RESULTS, timeout=30)

    # Helpers de depuración (opcionales)
    def debug_snapshot(self, prefix="debug"):
        try:
            self.driver.save_screenshot(f"{prefix}.png")
            with open(f"{prefix}.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
        except Exception:
            pass
