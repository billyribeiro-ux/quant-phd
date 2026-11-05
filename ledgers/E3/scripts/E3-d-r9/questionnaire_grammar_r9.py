# Round 9: drives the project page questionnaire in Chromium. Loads a 3-pair instrument, exports with no choices (2+ missing
# message), records one choice and exports with the remaining one missing (singular message), and checks the probability
# text rules of the page (isProbability) through the file loader for 0, 1, a fraction, and 2 (rejected).
import json, tempfile, pathlib
from playwright.sync_api import sync_playwright
URL = "http://127.0.0.1:8766/modules/E/E3/project.html"
d = pathlib.Path(tempfile.mkdtemp(prefix="e3q-"))
pairs = [
    {"pair_id": 1, "prizes_a": [100, 0], "probs_a": ["1/2", "1/2"], "prizes_b": [50], "probs_b": ["1"]},
    {"pair_id": 2, "prizes_a": [300, -100], "probs_a": ["3/4", "1/4"], "prizes_b": [200], "probs_b": ["1"]},
    {"pair_id": 3, "prizes_a": [500], "probs_a": ["0"], "prizes_b": [700, 0], "probs_b": ["1/2", "1/2"]},
]
good = d / "instrument.json"
good.write_text(json.dumps(pairs), encoding="utf-8")
bad_prob = d / "bad.json"
bad_prob.write_text(json.dumps([{**pairs[0], "probs_a": ["2", "1/2"]}]), encoding="utf-8")
out = {}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    page = b.new_page(accept_downloads=True)
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(URL)
    inp = page.locator("[data-questionnaire] input[type=file]")
    inp.set_input_files(str(good))
    page.wait_for_function("document.querySelector('[data-questionnaire] [role=status]').textContent.includes('pairs loaded')")
    buttons = page.locator("[data-questionnaire] button")
    export = [buttons.nth(i) for i in range(buttons.count()) if "xport" in (buttons.nth(i).text_content() or "")][0]
    export.click()
    out["all_missing"] = page.locator("[data-questionnaire] [role=status]").text_content()
    page.locator('input[name="q-pair-0"][value="A"]').check()
    export.click()
    out["two_missing"] = page.locator("[data-questionnaire] [role=status]").text_content()
    page.locator('input[name="q-pair-1"][value="B"]').check()
    export.click()
    out["one_missing"] = page.locator("[data-questionnaire] [role=status]").text_content()
    page.locator('input[name="q-pair-2"][value="A"]').check()
    with page.expect_download() as dl:
        export.click()
    out["export_file_ok"] = pathlib.Path(dl.value.path()).read_text(encoding="utf-8")[:80]
    inp.set_input_files(str(bad_prob))
    page.wait_for_timeout(300)
    out["bad_probability_status"] = page.locator("[data-questionnaire] [role=status]").text_content()
    b.close()
out["page_errors"] = errors
print(json.dumps(out, indent=1, ensure_ascii=False))
