import sys, pathlib, ast, shutil
ROOT = pathlib.Path("/tmp/verify42-AC4-e")
sys.path.insert(0, str(ROOT / "tools"))
from coursekit import unit
from run_graders import panel, workspace, run_suite, parse_seeds
u = unit("AC4"); cfg = panel(u)
seeds = parse_seeds("0-49")
for path in sorted(pathlib.Path(p) for p in sys.argv[1:]):
    desc = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8"))) or "(no description)"
    killed = None
    work = workspace(u, path, cfg)
    try:
        for seed in seeds:
            ok, output, _ = run_suite(work, cfg["suite"], seed)
            if not ok:
                killed = f"seed {seed}"
                break
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"{'KILLED' if killed else 'SURVIVED'} {path.name}: {desc.splitlines()[0]} -> {killed}")
