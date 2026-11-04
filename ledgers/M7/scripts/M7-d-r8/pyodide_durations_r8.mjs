// Round 8 (M7-d): run the M7 suite on the reference solution inside the vendored Pyodide, recording each test's call duration.
// Usage: node pyodide_durations_r8.mjs <checkout-root> <seed>
import { pathToFileURL } from "node:url";
import fs from "node:fs";
import path from "node:path";

const root = process.argv[2];
const seed = process.argv[3] ?? "0";
const vendor = path.join(root, "course/assets/vendor/pyodide");
const grader = path.join(root, "course/modules/M/M7/grader");
const { loadPyodide } = await import(pathToFileURL(path.join(vendor, "pyodide.mjs")).href);
const py = await loadPyodide({ indexURL: vendor + "/" });
await py.loadPackage(["pytest"]);
py.FS.mkdirTree("/work");
for (const [src, dst] of [["instance.py", "instance.py"], ["test_project.py", "test_project.py"], ["reference.py", "constrained_allocator.py"]]) {
  py.FS.writeFile("/work/" + dst, fs.readFileSync(path.join(grader, src), "utf-8"));
}
py.globals.set("__seed", String(seed));
const out = await py.runPythonAsync(`
import os, sys, json, time
os.chdir("/work"); sys.path.insert(0, "/work")
os.environ["QF_SEED"] = __seed
import pytest

class Durations:
    def __init__(self):
        self.rows = []
    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            self.rows.append((report.duration, report.nodeid.split("::")[-1], report.outcome))

d = Durations()
t0 = time.perf_counter()
code = pytest.main(["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"], plugins=[d])
total = time.perf_counter() - t0
slow = sorted(d.rows, reverse=True)[:5]
json.dumps({"exit": int(code), "tests": len(d.rows), "total_s": round(total, 2),
            "max_call_s": round(max(r[0] for r in d.rows), 4),
            "slowest": [[round(s, 4), n, o] for s, n, o in slow],
            "failed": [n for _, n, o in d.rows if o != "passed"]})
`);
console.log(out);
