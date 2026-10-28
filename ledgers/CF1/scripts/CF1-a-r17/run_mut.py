"""Run lab mutants against the L01 and L02 twins (python -I -W error); KILLED when rc differs or stdout differs."""
import subprocess, sys, pathlib, difflib

ROOT = pathlib.Path('/tmp/verify17-CF1-a')
PY = str(ROOT / '.venv/bin/python')
TWINS = {'L01': ROOT / 'tests/labs/CF1/lab-CF1-L01-1.py', 'L02': ROOT / 'tests/labs/CF1/lab-CF1-L02-1.py'}


def run(path):
    p = subprocess.run([PY, '-I', '-W', 'error', str(path)], capture_output=True, text=True, timeout=60)
    return p.returncode, p.stdout


base = {k: run(v) for k, v in TWINS.items()}
for k, (rc, _) in base.items():
    assert rc == 0, (k, rc)
killed = survived = 0
for f in sys.argv[1:]:
    src = pathlib.Path(f).read_text().splitlines()
    best = min(TWINS, key=lambda k: sum(1 for d in difflib.ndiff(TWINS[k].read_text().splitlines(), src) if d[:1] in '+-'))
    rc, out = run(f)
    verdict = 'KILLED' if (rc != 0 or out != base[best][1]) else 'SURVIVED'
    killed += verdict == 'KILLED'
    survived += verdict == 'SURVIVED'
    print(verdict, best, pathlib.Path(f).name, 'rc=%d' % rc)
print('killed', killed, 'survived', survived, 'total', len(sys.argv) - 1)
