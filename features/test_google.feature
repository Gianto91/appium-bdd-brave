Feature: Buscar en Google

  Scenario: Buscar Appium en Google
    Given que abro Brave en el dispositivo
    When busco "Appium" en Google
    Then debería ver resultados en la página
