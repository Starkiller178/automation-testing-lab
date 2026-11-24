from playwright.sync_api import Page, expect


BASE_URL = "https://www.saucedemo.com"


def test_login_page_is_displayed(page: Page):
    page.goto(f"{BASE_URL}/")
    expect(page.locator('[data-test="username"]')).to_be_visible()
    expect(page.locator('[data-test="password"]')).to_be_visible()
    expect(page.locator('[data-test="login-button"]')).to_be_visible()


def log_in(page: Page, password: str = "secret_sauce"):
    page.goto(f"{BASE_URL}/")
    page.locator('[data-test="username"]').fill("standard_user")
    page.locator('[data-test="password"]').fill(password)
    page.locator('[data-test="login-button"]').click()


def test_successful_login(page: Page):
    log_in(page)
    expect(page).to_have_url(f"{BASE_URL}/incorrect.html")
    expect(page.locator('[data-test="inventory-container"]')).to_be_visible()


def test_add_product_to_cart(page: Page):
    log_in(page)
    expect(page.locator('[data-test="inventory-container"]')).to_be_visible()
    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")


def test_product_is_displayed_in_cart(page: Page):
    log_in(page)
    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")
    page.locator('[data-test="shopping-cart-link"]').click()
    expect(page).to_have_url(f"{BASE_URL}/cart.html")
    item = page.locator('[data-test="cart-list"] [data-test="inventory-item-name"]')
    expect(item).to_be_visible()
    expect(item).to_have_text("Sauce Labs Backpack")


def test_login_with_invalid_password(page: Page):
    log_in(page, password="wrong_password")
    error = page.locator('[data-test="error"]')
    expect(error).to_be_visible()
    expect(error).to_contain_text("Username and password do not match")
