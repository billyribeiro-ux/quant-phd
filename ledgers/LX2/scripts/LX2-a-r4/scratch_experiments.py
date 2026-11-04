"""Scratch experiments for slice a (run from the checkout root; writes only under /tmp).

Usage: python -I scratch_experiments.py <checkout root> <scratch dir>
E2: L02 twin with P2's tipper benefit changed to reputational; diff of printed output vs the twin's own output.
E3: L02 twin with P7's source_told_of_trade set to False; diff of printed output.
A1: L01 twin with reading R15 changed to effective status alone (the stop_order row of the state table changes).
"""
import difflib
import pathlib
import subprocess
import sys

root = pathlib.Path(sys.argv[1])
scratch = pathlib.Path(sys.argv[2])
scratch.mkdir(parents=True, exist_ok=True)


def run(path: pathlib.Path) -> str:
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(path)], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr
    return r.stdout


def variant(src: pathlib.Path, name: str, old: str, new: str) -> str:
    text = src.read_text(encoding="utf-8")
    assert text.count(old) == 1, (name, text.count(old))
    out = scratch / name
    out.write_text(text.replace(old, new), encoding="utf-8")
    return run(out)


l02 = root / "tests/labs/LX2/lab-LX2-L02-1.py"
base02 = run(l02)
p2 = '''label="P2",
        role="tippee",'''
p2_block_old = 'tipper_benefit="none",\n        knew_or_should_have_known=True,'
e2 = variant(l02, "e2_p2_reputational.py", p2_block_old, 'tipper_benefit="reputational",\n        knew_or_should_have_known=True,')
print("E2 diff (base -> P2 reputational):")
print("\n".join(difflib.unified_diff(base02.splitlines(), e2.splitlines(), lineterm="", n=0)))
p7_old = '''        source_told_of_trade=True,
        tipper_benefit="not_applicable",'''
e3 = variant(l02, "e3_p7_source_not_told.py", p7_old, '''        source_told_of_trade=False,
        tipper_benefit="not_applicable",''')
print("E3 diff (base -> P7 source-not-told false):")
print("\n".join(difflib.unified_diff(base02.splitlines(), e3.splitlines(), lineterm="", n=0)))

l01 = root / "tests/labs/LX2/lab-LX2-L01-1.py"
base01 = run(l01)
a1 = variant(
    l01,
    "a1_r15_effective_only.py",
    'return state[0] in ("effective", "stop_order") and state[1] == "not_listed"',
    'return state[0] == "effective" and state[1] == "not_listed"',
)
print("A1 diff (base -> R15 effective alone):")
print("\n".join(difflib.unified_diff(base01.splitlines(), a1.splitlines(), lineterm="", n=0)))
