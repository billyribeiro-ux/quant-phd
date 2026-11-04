"""LX1-c round 2 verifier harness for the three project labs (project.html and its twins).

Run as: python3 -I -W error ledgers/LX1/scripts/LX1-c-r2/labs_r2.py  (from the repo root; paths are derived from __file__).

Checks, in order:
  A. page code (unescaped) equals the twin, line for line, except rung-2 blanks (___) which may replace a twin line
  B. twin under python -I -W error in a scratch dir whose data/ holds fx_monthly.csv; stdout equals the page's
     expected block exactly; exit 0 and empty stderr
  C. mutants (student errors, generated from the current twin text) are each killed: stdout differs or exit != 0
  D. alternative correct completions (rung 2) and alternative correct computations of Lab 3 pass
  E. loud-failure input tests for Lab 3: a blank GBP cell and a skipped month must raise
"""
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
PAGE = os.path.join(ROOT, "course/modules/LX/LX1/project.html")
TWIN = {
    "lab-LX1-project-1": os.path.join(ROOT, "tests/labs/LX1/lab-LX1-project-1.py"),
    "lab-LX1-project-2": os.path.join(ROOT, "tests/labs/LX1/lab-LX1-project-2.py"),
    "lab-LX1-project-3": os.path.join(ROOT, "tests/labs/LX1/lab-LX1-project-3.py"),
}
CSV = os.path.join(ROOT, "course/assets/data/market/fx_monthly.csv")
ENV = {"PATH": "/usr/bin:/bin", "PYTHONHASHSEED": "0"}


def page_labs():
    text = Path(PAGE).read_text(encoding="utf-8")
    out = {}
    for lab_id in TWIN:
        start = text.index(f'id="{lab_id}"')
        end = text.index("</section>", start)
        chunk = text[start:end]
        code = re.search(r'<code class="language-python" data-run>(.*?)</code>', chunk, re.S).group(1)
        expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', chunk, re.S).group(1)
        out[lab_id] = (html.unescape(code), html.unescape(expected), "class=\"lab completion\"" in text[text.rfind("<section", 0, start):start + 40])
    return out


def run(src_text, workdir, csv_text=None):
    os.makedirs(os.path.join(workdir, "data"), exist_ok=True)
    if csv_text is None:
        shutil.copy(CSV, os.path.join(workdir, "data", "fx_monthly.csv"))
    else:
        with open(os.path.join(workdir, "data", "fx_monthly.csv"), "w", encoding="utf-8") as fh:
            fh.write(csv_text)
    script = os.path.join(workdir, "lab.py")
    with open(script, "w", encoding="utf-8") as fh:
        fh.write(src_text)
    p = subprocess.run([sys.executable, "-I", "-W", "error", script], cwd=workdir, capture_output=True, text=True,
                       timeout=60, env=ENV, check=False)
    return p.returncode, p.stdout, p.stderr


def twin_text(lab_id):
    return Path(TWIN[lab_id]).read_text(encoding="utf-8")


def replace_once(src, old, new):
    assert src.count(old) == 1, (src.count(old), old)
    return src.replace(old, new)


def main():
    labs = page_labs()
    failures = []
    print("== A. page code equals twin")
    for lab_id, (code, expected, completion) in labs.items():
        twin = twin_text(lab_id)
        if completion:
            tl = twin.rstrip("\n").split("\n")
            pl = code.rstrip("\n").split("\n")
            ok = len(tl) == len(pl) and all(p == t or "___" in p for p, t in zip(pl, tl))
            blanks = [p for p in pl if "___" in p]
            print(lab_id, "completion; blank lines:", len(blanks), "line-match:", ok)
        else:
            ok = code.rstrip("\n") == twin.rstrip("\n")
            print(lab_id, "byte-identical to twin:", ok)
        if not ok:
            failures.append("A " + lab_id)
    print("== B. twin output equals page expected block")
    for lab_id, (code, expected, completion) in labs.items():
        if completion:
            # the completed twin is the solution; its output must equal the expected block
            pass
        with tempfile.TemporaryDirectory(prefix="lx1c-r2-b-") as wd:
            rc, out, err = run(twin_text(lab_id), wd)
        same = out.rstrip("\n") == expected.rstrip("\n")
        print(lab_id, "rc", rc, "stderr-empty", err == "", "stdout==expected", same)
        if rc != 0 or err or not same:
            failures.append("B " + lab_id)
            print("   stdout:", out[:300].replace("\n", "|"))
    # ---- C. mutants generated from the current twin text
    print("== C. mutants (generated from current twin)")
    p2 = twin_text("lab-LX1-project-2")
    p3 = twin_text("lab-LX1-project-3")
    e2 = labs["lab-LX1-project-2"][1]
    e3 = labs["lab-LX1-project-3"][1]
    mutants = [
        ("m01 real value without division", "lab-LX1-project-2",
         lambda s: replace_once(s, "return Fraction(nominal_cents) / price_level", "return Fraction(nominal_cents)")),
        ("m02 burden ratio inverted", "lab-LX1-project-2",
         lambda s: replace_once(s, "return 100 * (start_price / end_price - 1)", "return 100 * (end_price / start_price - 1)")),
        ("m03 real value multiplied by price", "lab-LX1-project-2",
         lambda s: replace_once(s, "return Fraction(nominal_cents) / price_level", "return Fraction(nominal_cents) * price_level")),
        ("m04 burden as ratio without percent", "lab-LX1-project-2",
         lambda s: replace_once(s, "return 100 * (start_price / end_price - 1)", "return start_price / end_price - 1")),
        ("m06 period-0 price used for every real value", "lab-LX1-project-2",
         lambda s: replace_once(s, "return Fraction(nominal_cents) / price_level", "return Fraction(nominal_cents) / PATH[0]")),
        ("n01 (new) real value truncated, not rounded half up", "lab-LX1-project-2",
         lambda s: replace_once(s, "cents = round_half_up(real_debt_cents(NOMINAL_DEBT_CENTS, price))",
                                "cents = int(real_debt_cents(NOMINAL_DEBT_CENTS, price))")),
        ("n02 (new) real value uses the previous period's price", "lab-LX1-project-2",
         lambda s: replace_once(s, "cents = round_half_up(real_debt_cents(NOMINAL_DEBT_CENTS, price))",
                                "cents = round_half_up(real_debt_cents(NOMINAL_DEBT_CENTS, PATH[max(t - 1, 0)]))")),
        ("m07 population sd (denominator n)", "lab-LX1-project-3",
         lambda s: replace_once(s, "/ (n - 1))", "/ n)")),
        ("m08 window two starts 2000-02", "lab-LX1-project-3",
         lambda s: replace_once(s, 'WINDOW_TWO_FROM = "2000-01"', 'WINDOW_TWO_FROM = "2000-02"')),
        ("m09 simple return instead of log change", "lab-LX1-project-3",
         lambda s: replace_once(s, "math.log(float(rate / previous))", "float(rate / previous) - 1")),
        ("n03 (new) window three drops its last change", "lab-LX1-project-3",
         lambda s: replace_once(s, "item[0] >= WINDOW_THREE_FROM]", "WINDOW_THREE_FROM <= item[0] < \"2026-09\"]")),
        ("n04 (new) log change sign flipped", "lab-LX1-project-3",
         lambda s: replace_once(s, "math.log(float(rate / previous))", "math.log(float(previous / rate))")),
    ]
    killed = 0
    for name, lab_id, fn in mutants:
        src = fn(p2 if lab_id == "lab-LX1-project-2" else p3)
        expected = e2 if lab_id == "lab-LX1-project-2" else e3
        with tempfile.TemporaryDirectory(prefix="lx1c-r2-c-") as wd:
            rc, out, err = run(src, wd)
        k = (rc != 0) or (out.rstrip("\n") != expected.rstrip("\n"))
        killed += k
        print(f"{name}: rc={rc} killed={k}", ("first-diff: " + repr(next((a for a, b in zip(out.splitlines(), expected.splitlines()) if a != b), '')))[:160] if k else "")
    print(f"mutants killed: {killed}/{len(mutants)}")
    if killed != len(mutants):
        failures.append("C survivor")
    print("== D. alternative correct completions and computations must pass")
    alts = [
        ("alt-a rung2 real value via reciprocal", "lab-LX1-project-2",
         [("return Fraction(nominal_cents) / price_level", "return Fraction(nominal_cents) * (Fraction(1) / price_level)")]),
        ("alt-b rung2 burden via difference over end", "lab-LX1-project-2",
         [("return 100 * (start_price / end_price - 1)", "return 100 * (start_price - end_price) / end_price")]),
        ("alt-c rung2 burden via subtraction of hundred", "lab-LX1-project-2",
         [("return 100 * (start_price / end_price - 1)", "return 100 * (start_price / end_price) - 100")]),
        ("alt-d lab3 sd via statistics.stdev only", "lab-LX1-project-3",
         [("    sd = sample_sd_two_pass(values)", "    sd = statistics.stdev(values)")]),
        ("alt-e lab3 log change via log1p", "lab-LX1-project-3",
         [("math.log(float(rate / previous))", "math.log1p(float(rate / previous) - 1)")]),
    ]
    alt_pass = 0
    for name, lab_id, reps in alts:
        src = p2 if lab_id == "lab-LX1-project-2" else p3
        for old, new in reps:
            src = replace_once(src, old, new)
        expected = e2 if lab_id == "lab-LX1-project-2" else e3
        with tempfile.TemporaryDirectory(prefix="lx1c-r2-d-") as wd:
            rc, out, err = run(src, wd)
        ok = rc == 0 and out.rstrip("\n") == expected.rstrip("\n") and err == ""
        alt_pass += ok
        print(f"{name}: rc={rc} passes={ok}")
    print(f"alternatives passing: {alt_pass}/{len(alts)}")
    if alt_pass != len(alts):
        failures.append("D alternative rejected")
    print("== E. Lab 3 loud failure on bad data")
    lines = Path(CSV).read_text(encoding="utf-8").splitlines()
    header = lines[0].split(",")
    gi = header.index("GBP")
    # E1: blank the last GBP cell
    rows = [ln.split(",") for ln in lines]
    rows1 = [list(r) for r in rows]
    rows1[-1][gi] = ""
    csv1 = "\n".join(",".join(r) for r in rows1) + "\n"
    # E2: drop one month in the middle (gap)
    csv2 = "\n".join(lines[:300] + lines[301:]) + "\n"
    for name, csv_text in (("E1 blank GBP in last row", csv1), ("E2 month gap", csv2)):
        with tempfile.TemporaryDirectory(prefix="lx1c-r2-e-") as wd:
            rc, out, err = run(p3, wd, csv_text=csv_text)
        raised = rc != 0 and "ValueError" in err
        print(f"{name}: rc={rc} ValueError={raised} stdout-lines={len(out.splitlines())}")
        if not raised:
            failures.append("E " + name)
    print("FAILURES:", failures if failures else "none")


if __name__ == "__main__":
    main()
