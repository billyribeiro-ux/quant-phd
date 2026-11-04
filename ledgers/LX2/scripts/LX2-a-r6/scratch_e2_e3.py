"""Scratch copies of the L02 twin for the E2 and E3 problems on the page (never written into the repository).

Usage: python -I scratch_e2_e3.py <repo_root>
E2: P2's tipper benefit set to reputational. E3: P7's source-told flag set to false (P7 then equals P6 in every flag).
Each copy runs under python -I -W error in a fresh temporary directory and prints its decision table.
"""
import pathlib
import subprocess
import sys
import tempfile

root = pathlib.Path(sys.argv[1])
src = (root / "tests/labs/LX2/lab-LX2-L02-1.py").read_text(encoding="utf-8")


def edit(text: str, label: str, old: str, new: str) -> str:
    i = text.index(f'label="{label}"')
    j = text.index('Pattern(', i + 1) if f'label="{label}"' != "P8" else len(text)
    block = text[i:j]
    if old not in block:
        raise SystemExit(f"{label}: expected {old!r} not found")
    return text[:i] + block.replace(old, new, 1) + text[j:]


variants = {
    "E2": edit(src, "P2", 'tipper_benefit="none"', 'tipper_benefit="reputational"'),
    "E3": edit(src, "P7", "source_told_of_trade=True", "source_told_of_trade=False"),
}
for name, text in variants.items():
    with tempfile.TemporaryDirectory() as tmp:
        path = pathlib.Path(tmp) / f"{name.lower()}_copy.py"
        path.write_text(text, encoding="utf-8")
        run = subprocess.run([sys.executable, "-I", "-W", "error", str(path)], capture_output=True, text=True, cwd=tmp)
        print(f"== {name} copy, exit {run.returncode}")
        table = run.stdout[run.stdout.index("\npattern  ") + 1:]
        print(table.rstrip())
