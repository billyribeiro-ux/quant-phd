import json, re, subprocess, sys, pathlib, tempfile
root = pathlib.Path(sys.argv[1])
d = json.load(open("/tmp/fanout-frags/AC4-d.round21.json"))
twin = {t: (root / f"tests/labs/AC4/lab-AC4-{t}-1.py").read_text(encoding="utf-8") for t in ("L07", "L08")}
ref = {t: subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/AC4/lab-AC4-{t}-1.py")], capture_output=True, text=True) for t in ("L07", "L08")}
extra = {  # hand transplants for round-17/18 files named in the ledger but absent from the round-21 list
    "r17_L08_m04_discord_ignores_ties": ("L08", "if (by_ri > 0) != (by_ratio > 0) and by_ri != 0 and by_ratio != 0:", "if (by_ri > 0) != (by_ratio > 0):"),
    "L08_n09_discord_pairs_same_name_order": ("L08", "if (by_ri > 0) != (by_ratio > 0) and by_ri != 0 and by_ratio != 0:", "if (by_ri > 0) != (by_ratio > 0):"),
}
for m in d["mutants"]:
    name = m["id"]
    desc = m["description"]
    mm = re.match(r"line: '(.*)' -> '(.*)'$", desc)
    if not mm:
        print(f"{name} | no line-pair description | skipped (see prior round)")
        continue
    old, new = mm.group(1), mm.group(2)
    tw = next(t for t in ("L07", "L08") if old in twin[t]) if any(old in twin[t] for t in ("L07", "L08")) else None
    if tw is None or twin[tw].count(old) != 1:
        print(f"{name} | old text found in no twin exactly once | NOT-TRANSPLANTABLE"); continue
    code = twin[tw].replace(old, new, 1)
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, dir="/tmp/AC4-d-v22") as f:
        f.write(code)
    r = subprocess.run([sys.executable, "-I", "-W", "error", f.name], capture_output=True, text=True, timeout=120)
    diff = r.returncode != 0 or r.stdout != ref[tw].stdout
    print(f"{name} | twin {tw} | exit {r.returncode} | output_differs {r.stdout != ref[tw].stdout} | {'KILLED' if diff else 'SURVIVED'}")
for name, (tw, old, new) in extra.items():
    f = next(root.glob(f"ledgers/AC4/mutants/AC4-d-r*/{name}.py"))
    print(f"{name} | file {f.name} | hand-transplant of the single changed line: old text in twin {twin[tw].count(old)} time(s)")
    code = twin[tw].replace(old, new, 1)
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, dir="/tmp/AC4-d-v22") as g:
        g.write(code)
    r = subprocess.run([sys.executable, "-I", "-W", "error", g.name], capture_output=True, text=True, timeout=120)
    print(f"   exit {r.returncode} output_differs {r.stdout != ref[tw].stdout} -> {'KILLED' if (r.returncode or r.stdout != ref[tw].stdout) else 'SURVIVED (equivalent on shipped seed?)'}")
    print("   ties in shipped seed (pairs with by_ri==0 or by_ratio==0):", "see ties check below")
