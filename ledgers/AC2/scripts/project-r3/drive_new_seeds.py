import subprocess, sys
seeds = [5899, 17179, 19590, 20410, 22023, 29803, 35334, 36395, 38882, 44746, 45472, 54979, 55071, 68753, 72476, 74431, 78482, 84177, 87275, 97186]
py = "/tmp/verify-ac2-p/.venv/bin/python"
def run(cand, sds):
    ok = 0; lines = []
    for s in sds:
        out = subprocess.run([py, "harness.py", cand, str(s)], capture_output=True, text=True).stdout
        line = [l for l in out.splitlines() if l.startswith("seed")]
        lines.append(line[0] if line else "NO OUTPUT")
        ok += int(bool(line) and "210 passed" in line[0])
    return ok, lines
ok, lines = run("/tmp/verify-ac2-p/course/modules/AC/AC2/grader/reference.py", seeds)
print("reference on 20 new seeds: 210 passed on", ok, "of", len(seeds))
open("ref_newseeds.txt", "w").write("\n".join(lines) + "\n")
for v in ["V1_svd_1e-8", "V2_svd_1e-12", "V3_condition_1e12", "V4_cholesky_pivot", "V5_strict_bool_rejecting_svd_1e-10"]:
    ok, lines = run(f"cands/{v}.py", seeds[:10])
    print(v, "210 passed on", ok, "of 10 new seeds")
