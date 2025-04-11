from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import os

app = Flask(__name__)

def handle_captcha(page, retries=3):
    print("CAPTCHA handling not implemented yet.")
    # Add your solving logic here
    return

def login_with_google(page):
    try:
        buttons = page.query_selector_all("button")
        for button in buttons:
            text = button.inner_text().lower()
            if "sign in with google" in text or "google" in text:
                button.click()
                print("Clicked on Google sign-in button.")
                page.wait_for_timeout(10000)  # Wait for user to complete login
                return True
    except Exception as e:
        print(f"Error during Google login: {e}")
    return False

def fill_form(page, form_data):
    for field in form_data:
        try:
            selector = field.get("selector")
            value = field.get("value")
            if selector and value is not None:
                page.fill(selector, value)
        except Exception as e:
            print(f"Error filling {selector}: {e}")

def navigate_to_company_site(page):
    try:
        possible_keywords = ["apply", "continue", "company", "website", "site"]
        links = page.query_selector_all("a, button")
        for link in links:
            try:
                text = link.inner_text().lower()
                href = link.get_attribute("href")
                if any(kw in text for kw in possible_keywords) or (href and any(kw in href for kw in possible_keywords)):
                    print(f"Navigating to company site via: {text or href}")
                    link.click()
                    page.wait_for_load_state("load")
                    return True
            except Exception as e:
                continue
    except Exception as e:
        print(f"Error navigating to company site: {e}")
    return False

@app.route("/apply", methods=["POST"])
def apply():
    data = request.get_json()
    jobs = data.get("jobs", [])

    if not jobs:
        return jsonify({"error": "No jobs provided"}), 400

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        for job in jobs:
            url = job.get("url")
            form_data = job.get("formData", [])
            follow_company_site = job.get("followCompanySite", False)
            captcha_retry_attempts = job.get("captchaRetryAttempts", 3)

            result = {"url": url, "status": "unknown"}

            try:
                page.goto(url, timeout=15000)
                print(f"Navigated to {url}")

                login_with_google(page)

                if follow_company_site:
                    success = navigate_to_company_site(page)
                    if not success:
                        result["status"] = "company_site_not_found"
                        results.append(result)
                        continue

                fill_form(page, form_data)
                handle_captcha(page, retries=captcha_retry_attempts)

                page.keyboard.press("Enter")
                result["status"] = "applied"

            except PlaywrightTimeout:
                result["status"] = "timeout"
            except Exception as e:
                result["status"] = "error"
                result["errorMessage"] = str(e)

            results.append(result)

        browser.close()

    return jsonify({"results": results})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, host="0.0.0.0", port=port)
