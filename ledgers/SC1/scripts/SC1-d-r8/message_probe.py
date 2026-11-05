"""Round-8 probe: collect the failure messages the suite prints for several wrong engines (-rf short summary)."""
import os, re, subprocess, sys, tempfile, shutil
ROOT = "/Users/billyribeiro/.fanout/wt/verifyE8-SC1-d"
G = os.path.join(ROOT, "course/modules/SC/SC1/grader")
PY = os.path.join(ROOT, ".venv/bin/python")
ref = open(os.path.join(G, "reference.py"), encoding="utf-8").read()
variants = {
    "srw_zero": ref.replace("return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)", "return 0")
                   .replace("    return sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= a)", "    return 0"),
    "tail_zero": ref.replace("    return math.erfc(a / math.sqrt(2.0 * t))", "    return 0.0")
                    .replace('    if t <= 0:\n        raise ValueError("the time t must be positive for the reflection tail")\n', ""),
    "tail_half": ref.replace("    return math.erfc(a / math.sqrt(2.0 * t))", "    return 0.5 * math.erfc(a / math.sqrt(2.0 * t))"),
    "est_zero": ref.replace("    return mean, math.sqrt(variance) / math.sqrt(count)", "    return 0.0, 0.0"),
    "nested_zero": ref.replace("    return fine, coarse", "    return 0, 0"),
    "srw_plus_one": ref.replace("    return sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= a)", "    return sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= a) + 1"),
}
seen = {}
for name, src in variants.items():
    w = tempfile.mkdtemp(prefix="sc1d-r8-probe-")
    shutil.copy(os.path.join(G, "test_project.py"), w)
    shutil.copy(os.path.join(G, "instance.py"), w)
    open(os.path.join(w, "bm_checks.py"), "w", encoding="utf-8").write(src)
    for seed in ("0", "7"):
        r = subprocess.run([PY, "-I", "-m", "pytest", "-q", "--tb=line", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                           cwd=w, capture_output=True, text=True, env={"QF_SEED": seed, "PATH": os.environ["PATH"]})
        for line in r.stdout.splitlines():
            m = re.search(r"test_project\.py:(\d+): (.*)$", line)
            if m:
                msg = m.group(2)
                seen.setdefault(msg, set()).add((name, m.group(1)))
    shutil.rmtree(w, ignore_errors=True)
for msg in sorted(seen):
    names = sorted(seen[msg])
    print(f"MSG: {msg}\n    e.g. {names[0]} (n={len(names)})")
print("distinct messages:", len(seen))
