"""Round-33 verifier drive of the five live figures on S7 L05 and L06, independent of tools/page_smoke.py.

Prerequisite (started by the caller): python -I -m http.server 8765 --bind 127.0.0.1, run inside course/.
For each page, in Chromium at 1280 and 360 px, light and dark: loads the page, reads every figure's readout and
description, drives every control (bayes-posterior: all 101 t values; hurdle-growth: all three alpha values;
stepm-steps: both buttons, at 1280 light), compares each readout with the Python recomputation in
figure_readouts.py, and saves element screenshots. Records console errors and requests leaving the origin.

Run: .venv/bin/python -I ledgers/S7/scripts/L05-L06-r33/drive_figures.py <scratch-dir>
"""

from __future__ import annotations

import importlib.util
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

import numpy as np
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
ORIGIN = "http://127.0.0.1:8765"
SWEEP = (ROOT / "tools" / "figure_sweep.js").read_text(encoding="utf-8")
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

spec = importlib.util.spec_from_file_location("figure_readouts", HERE / "figure_readouts.py")
assert spec and spec.loader
fr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fr)

NUM = re.compile(r"-?\d[\d,]*(?:\.\d+)?(?:e-?\d+)?")
problems: list[str] = []
console: list[str] = []
external: list[str] = []
states_log: dict[str, Any] = {}


def shown_numbers(text: str) -> list[float]:
    return [float(m.group(0).replace(",", "")) for m in NUM.finditer(text)]


def sig_tol(x: float, sig: int) -> float:
    return 0.5 * 10 ** (math.floor(math.log10(abs(x))) - sig + 1) if x else 0.5 * 10 ** (-sig + 1)


def compare_tokens(key: str, text: str, expected: list[tuple[str, float, Any]]) -> None:
    """expected: ('d', value, decimals) rounds to decimals; ('s', value, sig) to significant digits; ('x', value, None) exact."""
    shown = shown_numbers(text)
    if len(shown) != len(expected):
        problems.append(f"{key}: {len(shown)} numeric tokens shown, {len(expected)} expected: {text!r}")
        return
    for a, (kind, e, p) in zip(shown, expected, strict=True):
        if kind == "d":
            ok = abs(a - round(e, p)) < 1e-9
        elif kind == "s":
            ok = abs(a - e) <= sig_tol(e, p) + 1e-12
        else:
            ok = abs(a - e) < 1e-9
        if not ok:
            problems.append(f"{key}: shown {a} vs recomputed {e!r} ({kind},{p}) in {text!r}")


def hurdle_tokens(alpha: float) -> list[tuple[str, float, Any]]:
    crossing = math.ceil(alpha / (2 * float(fr.ndtr(-3.0))))
    assert float(fr.ndtri(1 - alpha / (2 * (crossing - 1)))) < 3 <= float(fr.ndtri(1 - alpha / (2 * crossing)))
    out: list[tuple[str, float, Any]] = [("x", 100 * alpha, None)]
    for m in (1, 10, 100, 1000, 10**6):
        out += [("d", float(fr.ndtri(1 - alpha / (2 * m))), 2), ("x", float(m), None)]
    return out + [("d", 3.0, 1), ("x", float(crossing), None)]


def bayes_tokens(t: float) -> list[tuple[str, float, Any]]:
    p = 2 * float(fr.ndtr(-t))
    mbf = math.exp(-t * t / 2)
    out: list[tuple[str, float, Any]] = [("d", t, 2), ("s", p, 3), ("x", 2.0, None), ("s", mbf, 3)]
    for pi0 in (0.5, 0.8, 0.95, 0.99):
        odds = pi0 / (1 - pi0)
        out += [("d", odds * mbf / (1 + odds * mbf), 3), ("x", pi0, None)]
    return out


def forking_tokens() -> list[tuple[str, float, Any]]:
    alpha, c = 0.05, float(fr.ndtri(1 - 0.025))
    z = np.linspace(-9, 9, 1201)
    w = np.ones_like(z)
    w[1:-1:2] = 4
    w[2:-1:2] = 2
    w = w * (18 / 1200) / 3
    phi = np.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)

    def fpr(rho: float) -> float:
        if rho == 0:
            return 1 - (1 - alpha) ** 10
        a, b = math.sqrt(rho), math.sqrt(1 - rho)
        inside = fr.ndtr((c - a * z) / b) - fr.ndtr((-c - a * z) / b)
        return float(1 - np.sum(w * phi * inside**10))

    out: list[tuple[str, float, Any]] = [("x", 10.0, None)]
    for rho in (0, 0.5, 0.8, 0.95):
        out += [("d", fpr(rho), 3), ("x", float(rho), None)]
    return out


def run_page(browser: Any, page_name: str) -> None:
    url = f"{ORIGIN}/modules/S/S7/{page_name}.html"
    for scheme in ("light", "dark"):
        for width, height in ((1280, 900), (360, 800)):
            ctx = browser.new_context(viewport={"width": width, "height": height}, color_scheme=scheme)
            page = ctx.new_page()
            tag = f"{page_name} {scheme} {width}"
            page.on("console", lambda m, tag=tag: console.append(f"{tag}: {m.text}") if m.type == "error" else None)
            page.on("pageerror", lambda e, tag=tag: console.append(f"{tag} pageerror: {e}"))
            page.on(
                "request",
                lambda r, tag=tag: external.append(f"{tag}: {r.url}")
                if not r.url.startswith(ORIGIN) and not r.url.startswith("data:")
                else None,
            )
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_selector('html[data-ready="true"]', timeout=60000)
            page.evaluate(SWEEP)
            charts = page.locator("[data-chart]")
            for ci in range(charts.count()):
                chart = charts.nth(ci)
                name = chart.get_attribute("data-chart") or ""
                key = f"{page_name}/{name}/{scheme}/{width}"
                readout = chart.locator(".figure-readout")
                default_text = readout.inner_text()
                desc = chart.locator("svg > desc").first.text_content() or ""
                states_log[key] = {"default_readout": default_text, "desc": desc}
                set_ctl = "(el, [i, v]) => window.__figureSweep.set(el, i, v)"
                if name == "bayes-posterior":
                    compare_tokens(f"{key} default", default_text, bayes_tokens(3.0))
                    if scheme == "light" and width == 1280:
                        for i in range(101):
                            t = round(0.05 * i, 2)
                            chart.evaluate(set_ctl, [0, t])
                            compare_tokens(f"{key} t={t}", readout.inner_text(), bayes_tokens(t))
                        chart.evaluate(set_ctl, [0, 3])
                if name == "hurdle-growth":
                    compare_tokens(f"{key} default", default_text, hurdle_tokens(0.05))
                    if scheme == "light" and width == 1280:
                        for a in (0.01, 0.1, 0.05):
                            chart.evaluate(set_ctl, [0, a])
                            compare_tokens(f"{key} alpha={a}", readout.inner_text(), hurdle_tokens(a))
                if name == "forking-paths":
                    compare_tokens(f"{key} default", default_text, forking_tokens())
                    if "reach 0.40 at K = 10" not in desc or "reach 0.10." not in desc:
                        problems.append(f"{key}: desc numbers differ: {desc[-260:]!r}")
                if name == "joint-vs-independent":
                    d = fr.joint_vs_independent()
                    expected = (
                        f"Correlation of the two bootstrap statistics: {d['corr_joint']:.2f} joint, "
                        f"{d['corr_indep']:.2f} separate. 95% critical value of the maximum over ten strategies: "
                        f"{d['crit_joint']:.2f} joint, {d['crit_indep']:.2f} separate."
                    )
                    if default_text != expected:
                        problems.append(f"{key}: readout {default_text!r} != recomputed {expected!r}")
                    if f"from {d['crit_joint']:.2f} to {d['crit_indep']:.2f}" not in desc:
                        problems.append(f"{key}: desc critical values differ")
                if name == "stepm-steps":
                    text101, _t, res101 = fr.stepm_readout(101)
                    want = text101.replace("Study 101:", "Study 101 (a median study):", 1)
                    if default_text != want:
                        problems.append(f"{key}: default readout {default_text!r} != recomputed {want!r}")
                    if scheme == "light" and width == 1280:
                        chart.locator("button", has_text="Simulate a new study").click()
                        text102 = fr.stepm_readout(102)[0]
                        if readout.inner_text() != text102:
                            problems.append(f"{key}: after simulate {readout.inner_text()!r} != {text102!r}")
                        chart.locator("button", has_text="Show a study where a later step rejects").click()
                        seed, draws = 102, 0
                        while True:
                            seed += 1
                            draws += 1
                            text, _t, res = fr.stepm_readout(seed)
                            if sum(res["mask"]) != len(res["steps"][0]["rejected"]) or draws >= 500:
                                break
                        plural = "y" if draws == 1 else "ies"
                        body = text.split(": ", 1)[1]
                        want_search = f"Study {seed}, found after drawing {draws} new stud{plural}: {body}"
                        if readout.inner_text() != want_search:
                            problems.append(f"{key}: after search {readout.inner_text()!r} != {want_search!r}")
                        states_log[key]["search_seed"] = seed
                        states_log[key]["search_draws"] = draws
                if scheme == "light" and width == 1280:
                    chart.screenshot(path=str(OUT / f"{page_name}-{name}-light-1280.png"))
                if scheme == "dark" and width == 360:
                    chart.screenshot(path=str(OUT / f"{page_name}-{name}-dark-360.png"))
            ctx.close()


with sync_playwright() as pw:
    browser = pw.chromium.launch()
    run_page(browser, "L05")
    run_page(browser, "L06")
    browser.close()

summary = {
    "problems": problems,
    "n_problems": len(problems),
    "console_errors": console,
    "external_requests": external,
    "states": states_log,
}
(OUT / "drive_results.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"problems={len(problems)} console_errors={len(console)} external={len(external)} states={len(states_log)}")
for p in problems[:40]:
    print("PROBLEM", p)
for c in console[:10] + external[:10]:
    print("LOG", c)
