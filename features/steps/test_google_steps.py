from behave import given, when, then

@given('abro Google en el navegador')
def step_impl(context):
    context.driver.get("https://www.google.com")

@when('busco "{texto}"')
def step_impl(context, texto):
    search_box = context.driver.find_element("name", "q")
    search_box.send_keys(texto)
    search_box.submit()

@then('veo resultados relacionados con "{texto}"')
def step_impl(context, texto):
    assert texto.lower() in context.driver.page_source.lower()
