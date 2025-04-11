from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import time

app = Flask(__name__)

@app.route("/")
def health_check():
    return jsonify({"status": "ok", "message": "Job apply service is running."})

@app.route('/apply', methods=['POST'])
def apply_jobs():
    data = request.json

    job_links = data.get("job_links", [])
    follow_to_company_site = data.get("followToCompanySite", False)
    form_data = data.get("formData", {})
    max_captcha_retries = data.get("captchaRetries", 3)

    if not job_links:
        return jsonify({"status": "error", "message": "No job links provided."}), 400

    results = []

    for url in job_links:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()
                page.goto(url, timeout=60000)

                status = "unknown"

                # Attempt Google login
                try:
                    login_with_google(page)
                    print("Google login attempted.")
                except Exception as e:
                    print("Google login failed:", str(e))

                # Captcha handling
                for attempt in range(max_captcha_retries):
                    if handle_captcha(page):
                        print("Captcha solved.")
                        break
                    print(f"Captcha attempt {attempt+1} failed.")
                else:
                    status = "captcha_failed"
                    browser.close()
                    results.append({"url": url, "status": status})
                    continue

                # Optional navigation to external company site
                if follow_to_company_site:
                    try:
                        navigate_to_company_site(page)
                        print("Navigated to company site.")
                    except Exception as e:
                        print("Failed to navigate to company site:", str(e))

                # Form filling
                try:
                    fill_form(page, form_data)
                    status = "applied"
                except Exception as e:
                    print("Form filling failed:", str(e))
                    status = "submission_failed"

                browser.close()
                results.append({"url": url, "status": status})

        except Exception as e:
            results.append({"url": url, "status": "error", "error": str(e)})

    return jsonify({"results": results})

def login_with_google(page):
    google_buttons = page.locator("text=/.*(Sign in with Google|Continue with Google).*/i")
    if google_buttons.count() > 0:
        google_buttons.first.click()
        time.sleep(5)
        # TODO: Handle Google login popup if needed

def handle_captcha(page):
    if page.locator("iframe[src*='recaptcha']").count() > 0:
        print("Captcha found.")
        return False  # Placeholder for real solver
    return True

def navigate_to_company_site(page):
    selectors = [
        "text=Apply on company site",
        "text=Apply externally",
        "text=Company Website",
        "text=Apply >> a",
        "a[href*='company']",
        "a[href*='careers']",
    ]
    for sel in selectors:
        buttons = page.locator(sel)
        if buttons.count() > 0:
            buttons.first.click()
            time.sleep(3)
            break

def fill_form(page, form_data):
    for selector, value in form_data.items():
        element = page.locator(selector)
        if element.count() > 0:
            element.first.fill(value)
            print(f"Filled {selector} with {value}")
        else:
            print(f"Selector not found: {selector}")

    submit_buttons = page.locator("button[type='submit'], input[type='submit'], text=Submit")
    if submit_buttons.count() > 0:
        submit_buttons.first.click()
        time.sleep(2)
    else:
        print("No submit button found.")
