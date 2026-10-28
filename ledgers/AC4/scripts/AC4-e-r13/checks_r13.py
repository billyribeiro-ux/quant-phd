"""Round-13 checks for AC4-e: every mutant has a non-empty first docstring line; no bare assert in test_project.py."""
import ast, glob, pathlib, sys
ROOT = pathlib.Path(sys.argv[1])
bad = []
mut = sorted(glob.glob(str(ROOT / "ledgers/AC4/mutants/*.py")))
for f in mut:
    d = ast.get_docstring(ast.parse(pathlib.Path(f).read_text()))
    if not d or not d.split("\n")[0].strip():
        bad.append(f)
print("mutants checked:", len(mut), "without a description:", bad)
t = ast.parse((ROOT / "course/modules/AC/AC4/grader/test_project.py").read_text())
bare = [a.lineno for a in ast.walk(t) if isinstance(a, ast.Assert) and a.msg is None]
print("bare asserts in test_project.py:", bare)
