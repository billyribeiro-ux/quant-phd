import subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]); out = Path(sys.argv[2])
L07 = (root/"tests/labs/AC1/lab-AC1-L07-1.py").read_text(encoding="utf-8")
L08 = (root/"tests/labs/AC1/lab-AC1-L08-1.py").read_text(encoding="utf-8")
cases = [
 ("m19a-L08-tax-dep-uses-previous-year-percent", "L08", "        tax_dep = cost * TAX_PERCENT[index] // 100\n",
  "        tax_dep = cost * TAX_PERCENT[index - 1 if index else 0] // 100\n", "FAIL-or-PASS?"),
 ("m19b-L08-current-tax-on-pretax", "L08", "        current = RATE_PERCENT * taxable // 100\n",
  "        current = RATE_PERCENT * pretax[index] // 100\n", "FAIL"),
 ("m19c-L07-cfo-subtracts-sbc", "L07", "        cfo = net_income + expense\n", "        cfo = net_income - expense\n", "FAIL"),
 ("m19d-L08-tax-rate-off-by-one-percent", "L08", "RATE_PERCENT = 21 ", "RATE_PERCENT = 20 ", "FAIL-or-PASS?"),
]
for cid, lab, old, new, exp in cases:
    src = L07 if lab == "L07" else L08
    assert src.count(old) == 1, (cid, src.count(old))
    p = out/f"{cid}.py"
    p.write_text(src.replace(old, new), encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", str(p)], capture_output=True, text=True)
    print(cid, "exit", r.returncode, "expected", exp, "|", (r.stderr.strip().splitlines() or ["-"])[-1][:120])
