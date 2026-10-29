import html, re, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1])
for n in ["L04", "L05", "L06"]:
    page = (root / f"course/modules/M/M3/{n}.html").read_text(encoding="utf-8")
    raw = re.findall(r'<pre([^>]*)>(.*?)</pre>', page, flags=re.S)
    blocks = [html.unescape(re.sub(r"<[^>]+>", "", b)) for _, b in raw]
    code_idx = [i for i, b in enumerate(blocks) if b.lstrip().startswith('"""')]
    assert len(code_idx) == 1, (n, code_idx)
    code = blocks[code_idx[0]]
    expected = blocks[code_idx[0] + 1]
    twin = root / f"tests/labs/M3/lab-M3-{n}-1.py"
    tcode = twin.read_text(encoding="utf-8")
    same = code.strip("\n") == tcode.strip("\n")
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, env={"PATH": "/usr/bin:/bin", "PYTHONHASHSEED": "0"})
    got = out.stdout.strip().splitlines()
    exp = expected.strip().splitlines()
    print(n, "code==twin:", same, "exit:", out.returncode, "stderr:", repr(out.stderr.strip()[:200]), "out==expected:", got == exp, len(got), len(exp))
    if got != exp:
        print("GOT", got); print("EXP", exp)
