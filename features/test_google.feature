Feature: Buscar Appium en Google

  Scenario: Buscar Appium en Chrome
    Given abro Google en el navegador
    When busco "Appium"
    Then veo resultados relacionados con "Appium"