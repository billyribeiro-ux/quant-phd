"""Run the in-browser E3 grader (the page's own runPytest, grader/reference.py as elicit.py) for given seeds.

Usage: browser_grader_seed.py <checkout> <seed> [<seed> ...]. Serves course/ the way tools/page_smoke.py does, opens
project.html in Chromium, and calls the page's python.js runPytest with the grader files and QF_SEED=<seed>.
Prints one line per test with its outcome and the message of any failure.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

checkout = Path(sys.argv[1]).resolve()
seeds = sys.argv[2:]
sys.path.insert(0, str(checkout / "tools"))

from playwright.sync_api import sync_playwright  # noqa: E402

import page_smoke  # noqa: E402

grader = checkout / "course/modules/E/E3/grader"
server, origin = page_smoke.serve()
JS = """async ([seed]) => {
  const panel = document.querySelector('section.grader-panel');
  const base = panel.dataset.grader;
  const text = async (u) => { const r = await fetch(u); if (!r.ok) throw new Error(u + ' ' + r.status); return r.text(); };
  const files = [
    { path: panel.dataset.suite, text: await text(base + panel.dataset.suite) },
    { path: 'instance.py', text: await text(base + 'instance.py') },
    { path: 'elicit.py', text: await text(base + 'reference.py') },
  ];
  const m = await import('/assets/js/python.js');
  const t0 = performance.now();
  const out = await m.runPytest({ files, test: panel.dataset.suite, env: { QF_SEED: seed }, packages: [] });
  const ms = performance.now() - t0;
  if (out.error) return { error: out.error, ms };
  return { exit: out.exit, ms, results: out.results.map(r => ({ test: r.test, outcome: r.outcome, when: r.when, message: r.message || '' })) };
}"""
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for seed in seeds:
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            page.goto(f"{origin}/modules/E/E3/project.html")
            page.wait_for_selector("html[data-ready='true']", timeout=90000)
            page.wait_for_selector("section.grader-panel", state="attached", timeout=30000)
            result = page.evaluate(JS, [seed])
            if "error" in result:
                print(f"seed {seed}: ERROR {result['error']}")
            else:
                failed = [r for r in result["results"] if r["outcome"] != "passed"]
                passed = sum(1 for r in result["results"] if r["outcome"] == "passed")
                print(f"seed {seed}: exit {result['exit']} passed {passed}/{len(result['results'])} ({result['ms']/1000:.1f} s)")
                for r in failed:
                    print(f"  FAIL {r['outcome']} {r['when']} {r['test']}: {r['message'][:600]}")
            page.close()
        browser.close()
finally:
    server.shutdown()
