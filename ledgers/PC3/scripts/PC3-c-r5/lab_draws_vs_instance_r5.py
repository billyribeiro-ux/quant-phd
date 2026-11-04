"""Round-5: the labs' draw_game(0) (from each project lab twin) equals grader make_instance(0), and the seed-0 settlement.
Usage: python3 -I <this> <checkout>. Loads the twins' draw_game by exec of the function source only (no lab main run)."""
import ast
import random
import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "course/modules/PC/PC3/grader"))
import instance  # noqa: E402

for lab in ("lab-PC3-project-1", "lab-PC3-project-3"):
    src = (root / f"tests/labs/PC3/{lab}.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns: dict = {"random": random, "Any": object}
    consts = {n.targets[0].id: n.value for n in tree.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)}
    for name in ("HORIZON", "START_CENTS", "MOVE_CENTS"):
        ns[name] = ast.literal_eval(consts[name])
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "draw_game":
            exec(compile(ast.Module(body=[node], type_ignores=[]), lab, "exec"), ns)
    path, arrivals = ns["draw_game"](0)
    inst = instance.make_instance(0)
    print(lab, "path equal:", path == inst["fair_path_cents"], "arrivals equal:", arrivals == inst["arrivals"],
          "settlement:", path[-1])
