# Drives the project page's questionnaire in Chromium: load a valid instrument, check the pair list, export blocked until
# every pair has a choice, export after choices, check the exported file; then a bad instrument. Records any request
# that leaves 127.0.0.1 (the page says nothing is sent anywhere).
import json, pathlib
from playwright.sync_api import sync_playwright
Q = pathlib.Path("/Users/billyribeiro/.fanout/scratch-E3-d-r8/q")
URL = "http://127.0.0.1:8765/modules/E/E3/project.html"
results = {}
external = []
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page(accept_downloads=True)
    page.on("request", lambda r: external.append(r.url) if not r.url.startswith("http://127.0.0.1:8765") and not r.url.startswith("data:") and not r.url.startswith("blob:") else None)
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(URL, wait_until="domcontentloaded")
    page.wait_for_selector("[data-questionnaire] input[type=file]")
    status = page.locator("[data-questionnaire] [role=status]")
    export = page.get_by_role("button", name="Export responses.json")
    results["export_disabled_initially"] = export.is_disabled()
    page.set_input_files("#q-file", str(Q / "instrument_ok.json"))
    page.wait_for_function("document.querySelector('[data-questionnaire] [role=status]').textContent.includes('pairs loaded')")
    results["status_after_load"] = status.inner_text()
    results["legend_1"] = page.locator("[data-questionnaire] legend").nth(0).inner_text()
    results["legend_2"] = page.locator("[data-questionnaire] legend").nth(1).inner_text()
    results["export_disabled_after_load"] = export.is_disabled()
    export.click()
    results["status_missing_choice"] = status.inner_text()
    page.locator('input[name="q-pair-0"][value="A"]').check()
    export.click()
    results["status_one_choice_missing"] = status.inner_text()
    page.locator('input[name="q-pair-1"][value="B"]').check()
    with page.expect_download() as dl:
        export.click()
    d = dl.value
    results["download_name"] = d.suggested_filename
    out = Q / "responses_export.json"
    d.save_as(str(out))
    results["status_after_export"] = status.inner_text()
    results["export_json"] = json.loads(out.read_text(encoding="utf-8"))
    page.set_input_files("#q-file", str(Q / "instrument_bad.json"))
    page.wait_for_function("document.querySelector('[data-questionnaire] [role=status]').textContent.includes('not loaded')")
    results["status_bad_file"] = status.inner_text()
    results["export_disabled_after_bad_file"] = export.is_disabled()
    results["page_errors"] = errors
    browser.close()
results["non_local_requests"] = external
print(json.dumps(results, indent=1, ensure_ascii=False))
