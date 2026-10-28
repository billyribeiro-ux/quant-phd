import json, re, subprocess, sys, pathlib, tempfile
root = pathlib.Path(sys.argv[1])
d = json.load(open("/tmp/fanout-frags/AC4-d.round21.json"))
tw = {t: (root / f"tests/labs/AC4/lab-AC4-{t}-1.py").read_text(encoding="utf-8").split("\n") for t in ("L07", "L08")}
ref = {t: subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/AC4/lab-AC4-{t}-1.py")], capture_output=True, text=True) for t in ("L07", "L08")}
mut_files = {p.name: p for p in root.glob("ledgers/AC4/mutants/AC4-d-r*/*.py")}
for m in d["mutants"]:
    desc = m["description"]
    mm = re.match(r"line: '(.*)' -> '(.*)'$", desc)
    if not mm:
        continue
    old, new = mm.group(1), mm.group(2)
    fname = m["file"].split("/")[-1] if "file" in m else m["id"].split(":", 1)[1]
    if fname not in mut_files:
        print(m["id"], "file not found"); continue
    mlines = mut_files[fname].read_text(encoding="utf-8").split("\n")
    hit = None
    for t in ("L07", "L08"):
        cands = [i for i, l in enumerate(tw[t]) if old.strip() in l]
        if len(cands) == 1:
            hit = (t, cands[0]); break
    if hit is None:
        print(m["id"], "old prefix not unique in either twin"); continue
    t, i = hit
    mcands = [l for l in mlines if new.strip() in l and new.strip() != ""]
    mcands = [l for l in mcands if l.strip() != old.strip()]
    if len(mcands) == 0:
        print(m["id"], "mutant line not found"); continue
    new_line = mcands[0]
    code_lines = list(tw[t]); code_lines[i] = new_line
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, dir="/tmp/AC4-d-v22") as f:
        f.write("\n".join(code_lines))
    r = subprocess.run([sys.executable, "-I", "-W", "error", f.name], capture_output=True, text=True, timeout=120)
    killed = r.returncode != 0 or r.stdout != ref[t].stdout
    print(f"{m['id']} | twin {t} line {i+1} | new line: {new_line.strip()[:110]} | exit {r.returncode} | output_differs {r.stdout != ref[t].stdout} | {'KILLED' if killed else 'SURVIVED'}")
