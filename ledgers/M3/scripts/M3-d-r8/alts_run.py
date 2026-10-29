import sys, pathlib
sys.path.insert(0, 'tools')
from coursekit import unit
from run_graders import panel, workspace, run_suite, parse_seeds
u = unit('M3')
cfg = panel(u)
root = pathlib.Path('ledgers/M3/alternatives')
for alt in sorted(root.glob('*.py')):
    work = workspace(u, alt.resolve(), cfg)
    fails = []
    for seed in parse_seeds('0-49'):
        ok, out, _ = run_suite(work, cfg['suite'], seed)
        if not ok:
            import re
            m = re.findall(r'FAILED \S+::(\S+)', out)
            fails.append((seed, m[:3]))
    print(alt.name, 'PASS all 50 seeds' if not fails else f'FAIL {len(fails)} seeds e.g. {fails[:3]}')
