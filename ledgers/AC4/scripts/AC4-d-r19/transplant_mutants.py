"""Transplant each one-line AC4-d mutant onto the CURRENT twin and run it.

Each mutant is a full copy of the twin at its round pin (r17: fefbf8b, r18: 7143726) with one changed line.
The single differing line is taken from the diff against that pin, and the same substitution is applied to the
current twin (51fa336). If the old line is absent from the current twin, the mutant is reported as not transplantable.
A transplanted mutant is killed when it exits non-zero or its output differs from the current embedded expected block.
Usage: python -I transplant_mutants.py <checkout> <scratch_dir>.
"""

import difflib
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
scratch = Path(sys.argv[2])
scratch.mkdir(parents=True, exist_ok=True)
pins = {"r17": "fefbf8b", "r18": "7143726"}
expected = {}
for page in ("L07", "L08"):
    text = (root / f"course/modules/AC/AC4/{page}.html").read_text(encoding="utf-8")
    expected[page] = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1)).strip()
current = {p: (root / f"tests/labs/AC4/lab-AC4-{p}-1.py").read_text(encoding="utf-8") for p in ("L07", "L08")}

import subprocess as sp

for rnd, pin in pins.items():
    base = {p: sp.run(["git", "-C", str(root), "show", f"{pin}:tests/labs/AC4/lab-AC4-{p}-1.py"],
                      capture_output=True, text=True, check=True).stdout for p in ("L07", "L08")}
    d = root / f"ledgers/AC4/mutants/AC4-d-{rnd}"
    for f in sorted(d.glob("*.py")):
        page = "L08" if "L08" in f.name else "L07"
        mut = f.read_text(encoding="utf-8").splitlines(keepends=True)
        old = base[page].splitlines(keepends=True)
        ops = [o for o in difflib.SequenceMatcher(None, old, mut, autojunk=False).get_opcodes() if o[0] != "equal"]
        if len(ops) != 1 or ops[0][0] != "replace" or ops[0][2] - ops[0][1] != 1 or ops[0][4] - ops[0][3] != 1:
            print(f"{rnd} {f.name}: NOT-A-ONE-LINE-MUTATION ops={[o[0] for o in ops]}")
            continue
        _, i1, i2, j1, j2 = ops[0]
        old_line, new_line = old[i1], mut[j1]
        cur = current[page].splitlines(keepends=True)
        hits = [k for k, line in enumerate(cur) if line == old_line]
        if len(hits) != 1:
            print(f"{rnd} {f.name}: NOT-TRANSPLANTABLE (old line found {len(hits)} times in current twin): {old_line.strip()[:100]}")
            continue
        new_src = "".join(cur[: hits[0]]) + new_line + "".join(cur[hits[0] + 1 :])
        out_file = scratch / f"t_{f.name}"
        out_file.write_text(new_src, encoding="utf-8")
        proc = sp.run([sys.executable, "-I", "-W", "error", str(out_file)], capture_output=True, text=True, timeout=60)
        out = proc.stdout.strip()
        if proc.returncode != 0:
            verdict = f"KILLED rc={proc.returncode} {proc.stderr.strip().splitlines()[-1][:80] if proc.stderr.strip() else ''}"
        elif out != expected[page]:
            verdict = "KILLED output-differs"
        else:
            verdict = "SURVIVED"
        print(f"{rnd} {f.name}: {verdict} | line: {old_line.strip()[:60]!r} -> {new_line.strip()[:60]!r}")
