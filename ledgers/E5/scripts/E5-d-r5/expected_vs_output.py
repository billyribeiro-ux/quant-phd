"""Exact comparison of each project expected block with its twin's stdout (lab 1 and 3), and lab 2 twin with expected."""
import html, os, re, subprocess, sys
root = sys.argv[1]
page = open(os.path.join(root, "course/modules/E/E5/project.html"), encoding="utf-8").read()
expected = [html.unescape(e) for e in re.findall(r'<pre class="expected" data-tolerance="1e-6">(.*?)</pre>', page, re.S)]
twins = ["lab-E5-project-1.py", "lab-E5-project-2.py", "lab-E5-project-3.py"]
for name, exp in zip(twins, expected):
    cwd = "/tmp/e5d5run3" if "3" in name else "/tmp/e5d5run"
    os.makedirs(cwd + "/data", exist_ok=True)
    if "3" in name:
        import shutil
        shutil.copy(os.path.join(root, "course/assets/data/market/ust_daily.csv"), cwd + "/data/ust_daily.csv")
    out = subprocess.run([os.path.join(root, ".venv/bin/python"), "-I", "-W", "error", os.path.join(root, "tests/labs/E5", name)], capture_output=True, text=True, cwd=cwd).stdout
    print(name, "exact_line_equal:", out.strip().splitlines() == exp.strip().splitlines(), "lines", len(out.strip().splitlines()))
