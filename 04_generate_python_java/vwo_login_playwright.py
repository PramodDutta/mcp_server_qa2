from pathlib import Path
import random
import time

from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    """Open VWO login, try invalid creds, capture error, screenshot, and close."""

    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://app.vwo.com/#/login", wait_until="domcontentloaded")

    # Generate random credentials
    rand = random.randint(10000, 99999)
    email = f"random.user.{rand}@example.com"
    password = f"P@ssw0rd!{rand}"

    # Fill the form and submit
    page.get_by_role("textbox", name="Email address").fill(email)
    page.get_by_role("textbox", name="Password").fill(password)
    page.get_by_role("button", name="Sign in", exact=True).click()

    # Wait for error message to appear
    locator = page.get_by_text("Your email, password, IP address or location did not match")
    locator.wait_for(timeout=15000)
    error_text = locator.inner_text().strip()

    # Prepare screenshot path: 01_module_playwright/screenshots/vwo-login-error.png
    project_root = Path(__file__).resolve().parent
    screenshots_dir = project_root / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = screenshots_dir / "vwo-login-error.png"

    page.screenshot(path=str(screenshot_path), full_page=False)

    print(f"Captured error: {error_text}")
    print(f"Screenshot saved to: {screenshot_path}")

    # Clean up
    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
