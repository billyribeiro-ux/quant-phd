"""FC2-a round 2 verifier scan (pin 9294b914).

Checks, for the hub and lessons L01-L03:
  1. the <pre><code data-run> block on each lesson page equals the twin file tests/labs/FC2/<twin>.py;
  2. the <pre class="expected"> block equals the stdout of the twin run as `python -I -W error <twin>`;
  3. banned phrases of BUILDER_RULES 1.2-1.4 and process words are absent from learner text;
  4. every internal href and in-page anchor in the slice resolves;
  5. every data-cite key is in references/references.json.
Run from the checkout root: python3 -I ledgers/FC2/scripts/FC2-a-r2/page_scan.py
"""

from __future__ import annotations

import html
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
MOD = os.path.join(ROOT, "course", "modules", "FC", "FC2")
TWINS = os.path.join(ROOT, "tests", "labs", "FC2")
PAGES = {"L01": "lab-FC2-L01-1.py", "L02": "lab-FC2-L02-1.py", "L03": "lab-FC2-L03-1.py"}
SLICE_FILES = ["index.html", "L01.html", "L02.html", "L03.html"]

BANNED = [
    "TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
    "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
    "obviously", "clearly", "It can be shown", "roughly", "historically", "About 6", "not trivia", "builder",
    "verifier", "round 2", "round 1", "Round ", "...", "…",
]

failures: list[str] = []


def check(cond: bool, msg: str) -> None:
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        failures.append(msg)


def extract(text: str, pattern: str) -> list[str]:
    return [m.group(1) for m in re.finditer(pattern, text, flags=re.S)]


def main() -> int:
    for lesson, twin in PAGES.items():
        page = open(os.path.join(MOD, lesson + ".html"), encoding="utf-8").read()
        code_blocks = extract(page, r'<pre><code class="language-python" data-run>(.*?)</code></pre>')
        expected_blocks = extract(page, r'<pre class="expected"[^>]*>(.*?)</pre>')
        check(len(code_blocks) == 1 and len(expected_blocks) == 1, f"{lesson}: one data-run block and one expected block")
        code = html.unescape(code_blocks[0])
        twin_text = open(os.path.join(TWINS, twin), encoding="utf-8").read()
        check(code.strip() == twin_text.strip(), f"{lesson}: page code equals twin {twin} (after unescape, strip)")
        with tempfile.TemporaryDirectory() as scratch:
            proc = subprocess.run(
                [sys.executable, "-I", "-W", "error", os.path.join(TWINS, twin)],
                cwd=scratch, capture_output=True, text=True, timeout=120,
            )
        check(proc.returncode == 0 and proc.stderr == "", f"{lesson}: twin exits 0 under -I -W error, stderr empty")
        expected = html.unescape(expected_blocks[0]).rstrip("\n")
        actual = proc.stdout.rstrip("\n")
        check(expected == actual, f"{lesson}: expected block equals twin stdout (lines={len(actual.splitlines())})")

    for name in SLICE_FILES:
        text = open(os.path.join(MOD, name), encoding="utf-8").read()
        visible = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<pre.*?</pre>", " ", text, flags=re.S)))
        for word in BANNED:
            hits = [m.start() for m in re.finditer(re.escape(word), visible)]
            check(not hits, f"{name}: banned/process string {word!r} absent (hits={len(hits)})")
        for m in re.finditer(r'href="([^"#][^"]*)"', text):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:")):
                check(False, f"{name}: external href {target}")
                continue
            path = os.path.normpath(os.path.join(MOD, target.split("#")[0]))
            check(os.path.exists(path), f"{name}: href {target} resolves")
        ids = set(re.findall(r'\sid="([^"]+)"', text))
        for frag in set(re.findall(r'href="#([^"]+)"', text)):
            check(frag in ids, f"{name}: in-page anchor #{frag} exists")

    refs = {e["key"] for e in json.load(open(os.path.join(ROOT, "references", "references.json")))["entries"]}
    for name in SLICE_FILES:
        text = open(os.path.join(MOD, name), encoding="utf-8").read()
        for key in re.findall(r'data-cite="([^"]+)"', text):
            check(key in refs, f"{name}: data-cite {key} in registry")

    print(f"SUMMARY failures={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
