// Python runtime worker. Runs lab code and autograder suites in Pyodide off the
// main thread, so a long computation never freezes the page. The runtime is
// vendored (course/assets/vendor/pyodide, locked by SHA-256); nothing is fetched
// from a CDN.
//
// Protocol: {id, type: "run", code, packages, files}     -> {id, stdout, stderr, error, ms}
//           {id, type: "pytest", files, test, env, packages, workdir} -> {id, exit, results, stdout, error, ms}
// A run's files are [{name, bytes}], the embedded market data its lab names in data-files (labs.js).

import { loadPyodide } from "../vendor/pyodide/pyodide.mjs";

let runtime = null;
let out = [];
let err = [];

function boot() {
  if (!runtime) {
    runtime = loadPyodide({ indexURL: new URL("../vendor/pyodide/", import.meta.url).href }).then((py) => {
      py.setStdout({ batched: (line) => out.push(line) });
      py.setStderr({ batched: (line) => err.push(line) });
      return py;
    });
  }
  return runtime;
}

async function prepare(py, packages, code) {
  if (packages && packages.length) await py.loadPackage(packages, { messageCallback: () => {} });
  if (code) await py.loadPackagesFromImports(code, { messageCallback: () => {} });
}

// Every lab runs in a fresh LAB_DIR whose data/ holds exactly the files its section names in data-files, so
// open("data/<file>") reads the same bytes here as in the lab's local twin (tools/coursekit.py twin_workdir).
const LAB_DIR = "/home/pyodide/lab";

function remove(py, path) {
  if (!py.FS.analyzePath(path).exists) return;
  if (py.FS.isDir(py.FS.stat(path).mode)) {
    for (const name of py.FS.readdir(path)) {
      if (name !== "." && name !== "..") remove(py, `${path}/${name}`);
    }
    py.FS.rmdir(path);
  } else {
    py.FS.unlink(path);
  }
}

function stage(py, files) {
  const os = py.pyimport("os");
  try {
    os.chdir("/");
    remove(py, LAB_DIR);
    py.FS.mkdirTree(`${LAB_DIR}/data`);
    for (const file of files || []) {
      if (!/^[A-Za-z0-9_.-]+$/.test(file.name)) throw new Error(`bad data file name ${JSON.stringify(file.name)}`);
      py.FS.writeFile(`${LAB_DIR}/data/${file.name}`, file.bytes);
    }
    os.chdir(LAB_DIR);
  } finally {
    os.destroy();
  }
}

async function run({ code, packages, files }) {
  const py = await boot();
  await prepare(py, packages, code);
  stage(py, files);
  out = [];
  err = [];
  const namespace = py.globals.get("dict")();
  try {
    await py.runPythonAsync(code, { globals: namespace });
    return { stdout: out.join("\n"), stderr: err.join("\n"), error: null };
  } catch (error) {
    return { stdout: out.join("\n"), stderr: err.join("\n"), error: String(error.message || error) };
  } finally {
    namespace.destroy();
  }
}

const PYTEST_DRIVER = `
import json, os, sys, importlib
import pytest

workdir = __qf_workdir
for name in list(sys.modules):
    root = name.split(".")[0]
    if root in __qf_purge:
        del sys.modules[name]
if workdir in sys.path:
    sys.path.remove(workdir)
sys.path.insert(0, workdir)
os.chdir(workdir)
os.environ.update(__qf_env)
importlib.invalidate_caches()

class Collector:
    def __init__(self):
        self.results = []

    def pytest_runtest_logreport(self, report):
        if report.when == "call" or report.outcome != "passed":
            message = ""
            if report.failed:
                crash = getattr(report.longrepr, "reprcrash", None)
                message = crash.message if crash is not None else str(report.longrepr)
            self.results.append({"test": report.nodeid.split("::")[-1], "when": report.when,
                                 "outcome": report.outcome, "message": message})

collector = Collector()
exit_code = pytest.main(["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", __qf_test],
                        plugins=[collector])
json.dumps({"exit": int(exit_code), "results": collector.results})
`;

async function pytest({ files, test, env, packages, workdir }) {
  const py = await boot();
  await prepare(py, ["pytest", ...(packages || [])], null);
  out = [];
  err = [];
  const roots = new Set();
  for (const file of files) {
    const path = `${workdir}/${file.path}`;
    py.FS.mkdirTree(path.slice(0, path.lastIndexOf("/")));
    py.FS.writeFile(path, file.text);
    roots.add(file.path.split("/")[0].replace(/\.py$/, ""));
  }
  const namespace = py.globals.get("dict")();
  namespace.set("__qf_workdir", workdir);
  namespace.set("__qf_test", test);
  namespace.set("__qf_env", py.toPy(env || {}));
  namespace.set("__qf_purge", py.toPy([...roots]));
  try {
    const payload = JSON.parse(await py.runPythonAsync(PYTEST_DRIVER, { globals: namespace }));
    return { ...payload, stdout: out.join("\n"), error: null };
  } catch (error) {
    return { exit: 3, results: [], stdout: out.join("\n"), error: String(error.message || error) };
  } finally {
    namespace.destroy();
  }
}

self.onmessage = async (event) => {
  const { id, type } = event.data;
  const started = performance.now();
  try {
    const result = type === "pytest" ? await pytest(event.data) : await run(event.data);
    self.postMessage({ id, ...result, ms: performance.now() - started });
  } catch (error) {
    self.postMessage({ id, error: String(error.message || error), ms: performance.now() - started });
  }
};
