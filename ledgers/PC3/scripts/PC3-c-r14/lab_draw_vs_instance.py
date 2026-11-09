"""Check that each project lab's own draw_game(0) equals grader/instance.py make_instance(0) (fair path and arrivals)."""
import importlib.util
import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "course/modules/PC/PC3/grader"))
import instance  # noqa: E402

ref = instance.make_instance(0)
for n in (1, 2, 3):
    spec = importlib.util.spec_from_file_location(f"lab{n}", root / f"tests/labs/PC3/lab-PC3-project-{n}.py")
    mod = importlib.util.module_from_spec(spec)
    src = (root / f"tests/labs/PC3/lab-PC3-project-{n}.py").read_text(encoding="utf-8").replace("\nmain()", "\n")
    code = compile(src, "lab", "exec")
    ns: dict = {"__name__": f"lab{n}"}
    exec(code, ns)
    path, arr = ns["draw_game"](0)
    print(f"lab {n}: path equal={path == ref['fair_path_cents']} arrivals equal={arr == ref['arrivals']}")
print("instance seed 0 settlement", ref["settlement_cents"], "fills of fixed rule not computed here")
