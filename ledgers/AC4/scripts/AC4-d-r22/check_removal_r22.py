import re, subprocess, sys, tempfile, pathlib
root = pathlib.Path(sys.argv[1])
def run(src):
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, dir="/tmp/AC4-d-v22") as f:
        f.write(src)
    r = subprocess.run([sys.executable, "-I", "-W", "error", f.name], capture_output=True, text=True, timeout=120)
    return r.returncode, r.stdout
def mutate(src, name, new_rhs):
    # replace the right-hand side of the single assignment 'name = ...' (one logical statement ending at the line that closes it)
    lines = src.split("\n")
    idx = [i for i, l in enumerate(lines) if re.match(rf"\s*{name} = ", l)]
    assert len(idx) == 1, (name, idx)
    i = idx[0]
    indent = re.match(r"\s*", lines[i]).group(0)
    depth = 0; j = i
    while True:
        depth += lines[j].count("(") + lines[j].count("[") - lines[j].count(")") - lines[j].count("]")
        if depth <= 0 and (j > i or lines[j].rstrip().endswith(("]", ")"))):
            break
        j += 1
    lines[i:j + 1] = [f"{indent}{name} = {new_rhs}"]
    return "\n".join(lines)
cases = {
 "L07": [("supplier_zero", "len(fits)"), ("sign_match", "len(fits)"), ("midpoint_inside", "len(feasible)"), ("sum_identity", "len(feasible)")],
 "L08": [("sign_ok", "[True] * (N_DIVISIONS + 1)"), ("gap_ok", "[True] * N_DIVISIONS")],
}
for t, lst in cases.items():
    src = (root / f"tests/labs/AC4/lab-AC4-{t}-1.py").read_text(encoding="utf-8")
    rc0, out0 = run(src)
    for name, rhs in lst:
        try:
            m = mutate(src, name, rhs)
        except AssertionError as e:
            print(t, name, "not found", e); continue
        rc, out = run(m)
        print(f"{t} check-removal '{name} = {rhs}': exit {rc}, output_differs {out != out0}, {'KILLED' if (rc or out != out0) else 'SURVIVED (identical output)'}")
