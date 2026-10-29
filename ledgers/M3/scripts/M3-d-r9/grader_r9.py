import sys, pathlib, re, subprocess, os
sys.path.insert(0, 'tools')
from coursekit import unit
from run_graders import panel, workspace, run_suite, parse_seeds
u = unit('M3')
cfg = panel(u)
mode = sys.argv[1]
if mode == 'collect':
    work = workspace(u, (u.directory/'grader'/'reference.py').resolve(), cfg)
    r = subprocess.run([sys.executable, '-m', 'pytest', '--collect-only', '-q', cfg['suite']], cwd=work, capture_output=True, text=True, env={'PATH': os.environ['PATH'], 'QF_SEED': '0', 'PYTHONHASHSEED': '0'})
    print(r.stdout[-300:], r.stderr[-300:])
elif mode == 'alts':
    root = pathlib.Path('ledgers/M3/alternatives')
    for alt in sorted(root.glob('*.py')):
        work = workspace(u, alt.resolve(), cfg)
        fails = []
        for seed in parse_seeds('0-49'):
            ok, out, _ = run_suite(work, cfg['suite'], seed)
            if not ok:
                fails.append((seed, re.findall(r'FAILED \S+::(\S+)', out)[:3]))
        print(alt.name, 'PASS all 50 seeds' if not fails else f'FAIL {len(fails)} seeds e.g. {fails[:3]}', flush=True)
