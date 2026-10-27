"""Round 28 browser drive of the two S7 live figures (L07 dsr-explorer, L08 cscv-explorer).

For each page, width (1280, 360 px) and theme (light, dark) the drive sets every control: every value of each range
control one at a time with the others at default, 120 random joint states (L07), and for L08 every split 1-70 with
the edge off and on under each of the four seeds (501-504, reached with the button). After each state it reads the
readout and the SVG descriptions, runs the page's own geometry checks (tools/figure_sweep.js collisions) and compares
the readout with figure_expect.py, a Python recomputation. Screenshots of the default state are saved.
Usage: .venv/bin/python -I drive_figs.py <checkout> <out_dir>   (a static server must serve <checkout>/course on :8765)
"""

from __future__ import annotations

import json
import os
import random
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import figure_expect as fe  # noqa: E402

CHECKOUT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
SWEEP = (CHECKOUT / "tools/figure_sweep.js").read_text(encoding="utf-8")
BASE = os.environ.get("DRIVE_BASE", "http://127.0.0.1:8765/modules/S/S7/")


def grid(c: dict) -> list[float]:
    n = round((c["max"] - c["min"]) / c["step"])
    return [round(c["min"] + k * c["step"], 10) for k in range(n + 1)]


def js_state(chart) -> list[dict]:
    return chart.evaluate("(el) => window.__figureSweep.controls(el)")


def set_ctrl(chart, i: int, v) -> None:
    chart.evaluate("(el, [i, v]) => window.__figureSweep.set(el, i, v)", [i, v])


def readouts(chart) -> dict:
    return chart.evaluate(
        """(el) => ({
            readout: (el.querySelector('.figure-readout') || {}).textContent ?? null,
            readoutHidden: (el.querySelector('.figure-readout') || {hidden: null}).hidden,
            descs: [...el.querySelectorAll('svg > desc')].map((d) => d.textContent),
            notes: [...el.querySelectorAll('.figure-note')].map((n) => n.textContent),
            labels: [...el.querySelectorAll('svg text')].map((t) => t.textContent),
        })"""
    )


def collisions(chart) -> list[str]:
    return chart.evaluate("(el) => window.__figureSweep.collisions(el)")


def run_l07(page, chart, tag: str, results: dict) -> None:
    controls = js_state(chart)
    assert [c["label"] for c in controls][:6] == [
        "Estimated Sharpe ratio (per day)", "Days T", "Skewness γ3", "Kurtosis γ4", "Trials N", "s.d. of trial Sharpe ratios",
    ], [c["label"] for c in controls]
    defaults = [c["value"] for c in controls]
    ranges = [c for c in controls]
    mismatches, n_states, n_refused, geometry = [], 0, 0, []

    def check_state(label: str, vals: list) -> None:
        nonlocal n_states, n_refused
        n_states += 1
        sr, ti, skew, kurt, ni, disp = vals[0], int(vals[1]), vals[2], vals[3], int(vals[4]), vals[5]
        exp = fe.l07_readout(sr, ti, skew, kurt, ni, disp)
        got = readouts(chart)
        if exp["refused"]:
            n_refused += 1
            want_note = (
                f"No distribution has kurtosis below 1 + skewness² = {exp['bound']} (Problem P1); "
                "raise the kurtosis or move the skewness toward zero."
            )
            ok = got["readoutHidden"] is True and got["readout"] == "" and want_note in got["notes"]
        else:
            ok = got["readout"] == exp["readout"] and got["readoutHidden"] is False and len(got["descs"]) >= 1 and got["descs"][0] == exp["desc"]
        if not ok:
            mismatches.append({"state": label, "values": vals, "expected": exp, "got": got})
        geo = collisions(chart)
        if geo:
            geometry.append({"state": label, "problems": geo})

    check_state("default", defaults)
    # one control at a time across its whole range
    for i, c in enumerate(controls):
        for v in grid(c):
            set_ctrl(chart, i, v)
            vals = [x["value"] for x in js_state(chart)]
            check_state(f"{c['label']}={v}", vals)
            set_ctrl(chart, i, c["value"])
    # random joint states
    rnd = random.Random(2028)
    for k in range(120):
        for i, c in enumerate(controls):
            set_ctrl(chart, i, rnd.choice(grid(c)))
        vals = [x["value"] for x in js_state(chart)]
        check_state(f"joint {k}", vals)
    for i, c in enumerate(controls):
        set_ctrl(chart, i, c["value"])
    results[tag] = {"states": n_states, "refused_states": n_refused, "mismatches": mismatches[:20], "n_mismatch": len(mismatches), "geometry_states": len(geometry), "geometry_examples": geometry[:5]}


def run_l08(page, chart, tag: str, results: dict) -> None:
    controls = js_state(chart)
    assert controls[0]["label"] == "Split" and controls[1]["label"] == "Give configuration 1 a true edge", controls
    cache: dict = {}
    mismatches, n_states, geometry = [], 0, []
    for press in range(4):
        if press > 0:
            set_ctrl(chart, 2, None)  # the button: seed + 1
        seed = 501 + press
        for edge in (False, True):
            set_ctrl(chart, 1, edge)
            key = (seed, edge)
            if key not in cache:
                cache[key] = fe.cscv(fe.simulate(seed, edge), 8)
            result = cache[key]
            for split in range(1, 71):
                set_ctrl(chart, 0, split)
                n_states += 1
                exp = fe.l08_readout(seed, edge, split, result)
                got = readouts(chart)
                ok = got["readout"] == exp["readout"]
                ok = ok and any(d.startswith("Histogram of the 70 logits") and d == exp["hist_desc"] for d in got["descs"])
                ok = ok and exp["split_logit_label"] in got["labels"]
                if not ok:
                    mismatches.append({"seed": seed, "edge": edge, "split": split, "expected": exp, "got": got["readout"]})
                geo = collisions(chart)
                if geo:
                    geometry.append({"seed": seed, "edge": edge, "split": split, "problems": geo})
    results[tag] = {"states": n_states, "mismatches": mismatches[:20], "n_mismatch": len(mismatches), "geometry_states": len(geometry), "geometry_examples": geometry[:5], "pbo_by_seed_edge": {f"{k[0]}-{k[1]}": round(v["pbo"], 6) for k, v in cache.items()}}


def main() -> None:
    summary: dict = {}
    console: list[str] = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        only_light_1280 = os.environ.get("DRIVE_ONLY_LIGHT_1280") == "1"
        for width in ((1280,) if only_light_1280 else (1280, 360)):
            for theme in (("light",) if only_light_1280 else ("light", "dark")):
                ctx = browser.new_context(viewport={"width": width, "height": 900}, color_scheme=theme)
                ctx.add_init_script(f"try{{localStorage.setItem('qf-theme','{theme}')}}catch(e){{}}")
                for page_name, figure, runner in (("L07", "dsr-explorer", run_l07), ("L08", "cscv-explorer", run_l08)):
                    page = ctx.new_page()
                    page.on("console", lambda m: console.append(f"{page_name} {width} {theme} {m.type}: {m.text}") if m.type in ("error", "warning") else None)
                    page.on("pageerror", lambda e: console.append(f"{page_name} {width} {theme} pageerror: {e}"))
                    page.goto(f"{BASE}{page_name}.html", wait_until="load")
                    page.wait_for_selector('html[data-ready="true"]', timeout=60000)
                    page.evaluate(SWEEP)
                    chart = page.locator(f'[data-chart="{figure}"]')
                    chart.wait_for()
                    chart.scroll_into_view_if_needed()
                    tag = f"{page_name}-{width}-{theme}"
                    if width == 1280 and theme == "light" or width == 360 and theme == "dark":
                        pass
                    runner(page, chart, tag, summary)
                    chart.screenshot(path=str(OUT / f"{tag}-default.png"))
                    page.close()
                ctx.close()
        browser.close()
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
    (OUT / "console.txt").write_text("\n".join(console) + ("\n" if console else ""), encoding="utf-8")
    for tag, r in summary.items():
        print(tag, "states", r["states"], "mismatches", r.get("n_mismatch"), "geometry states", r.get("geometry_states"))
    print("console errors/warnings:", len(console))


if __name__ == "__main__":
    main()
