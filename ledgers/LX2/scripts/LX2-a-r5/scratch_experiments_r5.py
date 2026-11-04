"""Scratch copies of the lab twins for the student experiments the lesson describes (run in a scratch dir, not the repo).

Usage: python3 -I scratch_experiments_r5.py <repo_root> <empty scratch dir>
E2: L02 twin with P2's tipper benefit changed to reputational (L02 problem E2).
E3: L02 twin with P7's source-told flag set to false (L02 problem E3).
A1: L01 twin with R15 requiring status effective alone (L01 section 5, last limit).
Each copy is run under python -I -W error; the decision rows are compared with the untouched twin.
"""
import pathlib
import subprocess
import sys

root = pathlib.Path(sys.argv[1])
scratch = pathlib.Path(sys.argv[2])
scratch.mkdir(parents=True, exist_ok=True)
twin_l02 = (root / "tests/labs/LX2/lab-LX2-L02-1.py").read_text(encoding="utf-8")
twin_l01 = (root / "tests/labs/LX2/lab-LX2-L01-1.py").read_text(encoding="utf-8")


def run(path: pathlib.Path) -> list[str]:
    proc = subprocess.run([sys.executable, "-I", "-W", "error", str(path)], capture_output=True, text=True, check=True)
    return proc.stdout.splitlines()


def replace_once(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, (old, text.count(old))
    return text.replace(old, new)


base = run(root / "tests/labs/LX2/lab-LX2-L02-1.py")
e2_text = replace_once(
    twin_l02,
    'tipper_benefit="none",',
    'tipper_benefit="reputational",',
)
e3_idx = twin_l02.index('label="P7"')
j = twin_l02.index("source_told_of_trade=True,", e3_idx)
e3_text = twin_l02[:j] + "source_told_of_trade=False," + twin_l02[j + len("source_told_of_trade=True,") :]
(scratch / "e2.py").write_text(e2_text, encoding="utf-8")
(scratch / "e3.py").write_text(e3_text, encoding="utf-8")
e2 = run(scratch / "e2.py")
e3 = run(scratch / "e3.py")
for name, out in (("E2 (P2 reputational)", e2), ("E3 (P7 source-told false)", e3)):
    rows = [(x, y) for x, y in zip(base, out) if x != y]
    print(f"{name}: lines that differ from the twin: {len(rows)}")
    for x, y in rows:
        print("  twin:", x)
        print("  copy:", y)
    print(f"{name}: summary:", [line for line in out if line.startswith("fired:")])

base1 = run(root / "tests/labs/LX2/lab-LX2-L01-1.py")
a1_text = replace_once(
    twin_l01,
    'return state[0] in ("effective", "stop_order") and state[1] == "not_listed"',
    'return state[0] == "effective" and state[1] == "not_listed"',
)
(scratch / "a1.py").write_text(a1_text, encoding="utf-8")
a1 = run(scratch / "a1.py")
changed = [(x, y) for x, y in zip(base1, a1) if x != y]
print("A1 (R15 effective alone): lines that differ from the L01 twin:", len(changed))
for x, y in changed:
    print("  twin:", x)
    print("  copy:", y)
