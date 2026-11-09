"""Verifier (FC1-b r3): numerical check of the directional claims about L05 Lab 1 parameters.

Writes parameter-changed copies of the twin into a scratch dir and diffs stdout against the default run.
"""
import difflib
import pathlib
import re
import subprocess
import sys
import tempfile

TWIN = pathlib.Path(sys.argv[1]) / "tests/labs/FC1/lab-FC1-L05-1.py"
src = TWIN.read_text(encoding="utf-8")
scratch = pathlib.Path(tempfile.mkdtemp(prefix="fc1b_l05_"))


def run(text, name):
    p = scratch / f"{name}.py"
    p.write_text(text, encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(p)], capture_output=True, text=True, cwd=scratch, timeout=60)
    assert r.returncode == 0 and not r.stderr, (name, r.stderr)
    return r.stdout.splitlines()


def sub(text, pattern, repl):
    new, n = re.subn(pattern, repl, text, count=1)
    assert n == 1, pattern
    return new


base = run(src, "base")
variants = {
    "settlement3": sub(src, r"SETTLEMENT_LAG = 2 ", "SETTLEMENT_LAG = 3 "),
    "clearing1": sub(src, r"CLEARING_OFFSET = 0 ", "CLEARING_OFFSET = 1 "),
    "clearing3": sub(src, r"CLEARING_OFFSET = 0 ", "CLEARING_OFFSET = 3 "),
}
print("base offsets line:", [l for l in base if l.startswith("offsets_nondecreasing")])
for name, text in variants.items():
    out = run(text, name)
    changed = [l for l in difflib.unified_diff(base, out, lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
    print(f"== {name}: {len(changed)} changed lines")
    for l in changed:
        print("  ", l[:150])
    print("   offsets line:", [l for l in out if l.startswith("offsets_nondecreasing")])
    batch_same = [l for l in out if l.startswith(("batch_trades", "net ", "sum_of", "net_"))] == [l for l in base if l.startswith(("batch_trades", "net ", "sum_of", "net_"))]
    print("   batch and netting lines identical to base:", batch_same)
