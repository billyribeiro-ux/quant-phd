"""Run scratch copies of the L02 twin for problems E2 and E3 and print the changed rows.

Usage: python -I ledgers/LX2/scripts/LX2-a-r7/scratch_e2_e3.py <twin.py> <scratch_dir>
Writes two modified copies into <scratch_dir> (outside the repository), runs each under python -I -W error,
and prints the P2 row (E2) and the P7 row (E3) plus the fired summary line.
"""
import pathlib
import subprocess
import sys

twin = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
scratch = pathlib.Path(sys.argv[2])
scratch.mkdir(parents=True, exist_ok=True)
e2_src = twin.replace('tipper_benefit="none",', 'tipper_benefit="reputational",', 1)
assert e2_src != twin
e3_src = twin.replace("source_told_of_trade=True,", "source_told_of_trade=False,", 1)
assert e3_src != twin
for name, src in (("e2.py", e2_src), ("e3.py", e3_src)):
    p = scratch / name
    p.write_text(src, encoding="utf-8")
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(p)], capture_output=True, text=True, timeout=60)
    print(f"== {name} exit={out.returncode} stderr_bytes={len(out.stderr)}")
    for line in out.stdout.splitlines():
        if line.startswith(("P2 ", "P7 ", "fired:", "not fired:")):
            print(line)
