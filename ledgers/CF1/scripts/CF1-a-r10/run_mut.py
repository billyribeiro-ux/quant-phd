import subprocess, sys, pathlib, difflib
root = pathlib.Path('/tmp/verify10-CF1-a')
py = str(root / '.venv/bin/python')
twins = {'L01': root/'tests/labs/CF1/lab-CF1-L01-1.py', 'L02': root/'tests/labs/CF1/lab-CF1-L02-1.py'}
def run(path):
    p = subprocess.run([py, '-I', '-W', 'error', str(path)], capture_output=True, text=True, timeout=60)
    return p.returncode, p.stdout
base = {k: run(v) for k, v in twins.items()}
for k, (rc, out) in base.items():
    assert rc == 0, (k, rc)
files = sys.argv[1:]
killed = survived = 0
for f in files:
    src = pathlib.Path(f).read_text().splitlines()
    best = min(twins, key=lambda k: sum(1 for d in difflib.ndiff(twins[k].read_text().splitlines(), src) if d[:1] in '+-'))
    rc, out = run(f)
    verdict = 'KILLED' if (rc != 0 or out != base[best][1]) else 'SURVIVED'
    if verdict == 'KILLED': killed += 1
    else: survived += 1
    print(verdict, best, pathlib.Path(f).name, 'rc=%d' % rc)
print('killed', killed, 'survived', survived, 'total', len(files))
