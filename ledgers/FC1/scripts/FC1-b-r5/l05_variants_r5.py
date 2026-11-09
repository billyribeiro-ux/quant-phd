"""FC1-b round 5: run L05 twin variants in a scratch directory (outside the checkout) and diff against the default.

Checks the lesson claims: changing SETTLEMENT_LAG changes only the header, settlement and position-update lines;
changing CLEARING_OFFSET changes the header and clearing line and can make offsets_nondecreasing print False when the
clearing offset exceeds the settlement lag. Also reports the L05 L04-independent batch in the variant runs.
"""

import difflib
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(".").resolve()
TWIN = ROOT / "tests/labs/FC1/lab-FC1-L05-1.py"
src = TWIN.read_text(encoding="utf-8")
scratch = pathlib.Path(tempfile.mkdtemp(prefix="fc1b_r5_", dir="/tmp"))


def run(text: str, name: str) -> list[str]:
    path = scratch / f"{name}.py"
    path.write_text(text, encoding="utf-8")
    res = subprocess.run([sys.executable, "-I", "-W", "error", str(path)], capture_output=True, text=True, check=False)
    assert res.returncode == 0, (name, res.stderr)
    return res.stdout.splitlines()


base = run(src, "default")
print("default offsets line:", [l for l in base if l.startswith("offsets_nondecreasing")])
for name, old, new in [
    ("lag3", "SETTLEMENT_LAG = 2 ", "SETTLEMENT_LAG = 3 "),
    ("clear1", "CLEARING_OFFSET = 0 ", "CLEARING_OFFSET = 1 "),
    ("clear3", "CLEARING_OFFSET = 0 ", "CLEARING_OFFSET = 3 "),
    ("lag0_clear0", "SETTLEMENT_LAG = 2 ", "SETTLEMENT_LAG = 0 "),
]:
    assert src.count(old) == 1, (name, src.count(old))
    out = run(src.replace(old, new), name)
    changed = [d for d in difflib.unified_diff(base, out, lineterm="", n=0) if d[:1] in "+-" and d[:3] not in ("+++", "---")]
    print(f"== {name}: changed lines")
    for d in changed:
        print("  ", d[:150])
    print("   offsets line:", [l for l in out if l.startswith("offsets_nondecreasing")])
    print("   count of differing output lines:", len(changed) // 2)
