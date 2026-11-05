"""Make the three scratch copies of the L02 twin named in E2, E3 and M3, run each under python -I -W error.

usage: python3 -I scratch_r10.py <checkout> <scratch-dir>   (scratch-dir must be empty and new)
"""
import pathlib
import subprocess
import sys

checkout = pathlib.Path(sys.argv[1])
scratch = pathlib.Path(sys.argv[2])
twin = checkout / "tests/labs/LX2/lab-LX2-L02-1.py"
py = checkout / ".venv/bin/python"
EDITS = {
    "e2": ("P2", "tipper_benefit", 'tipper_benefit="none"', 'tipper_benefit="reputational"'),
    "e3": ("P7", "source_told_of_trade", "source_told_of_trade=True", "source_told_of_trade=False"),
    "m3": ("P3", "tipper_benefit", 'tipper_benefit="pecuniary"', 'tipper_benefit="none"'),
}
for name, (label, field, old, new) in EDITS.items():
    text = twin.read_text(encoding="utf-8")
    i = text.index(f'label="{label}"')
    k = text.index(f"{field}=", i)
    end = text.index("\n", k)
    line = text[k:end]
    assert line.count(old) == 1, line
    (scratch / f"{name}.py").write_text(text[:k] + line.replace(old, new, 1) + text[end:], encoding="utf-8")
    r = subprocess.run([str(py), "-I", "-W", "error", str(scratch / f"{name}.py")], capture_output=True, text=True, cwd=scratch)
    print(f"== {name}: {label} {old} -> {new} exit={r.returncode} stderr_bytes={len(r.stderr.encode())}")
    print("\n".join(line for line in r.stdout.splitlines() if line[:2] == "P" and " fired " in line or line.startswith(("fired", "not fired")) ))
