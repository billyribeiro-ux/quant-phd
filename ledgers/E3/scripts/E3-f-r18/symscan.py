import re, sys, json, collections
# Collect LaTeX control words and single-letter/subscript symbols used in math of the given files.
files = sys.argv[1:]
ctrl = collections.Counter()
per_file = {}
for f in files:
    txt = open(f, encoding="utf-8").read()
    txt = txt.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    c = collections.Counter(re.findall(r"\\([A-Za-z]+)", txt))
    per_file[f] = c
    ctrl.update(c)
print("control words (all files):")
print(sorted(ctrl.items(), key=lambda kv: -kv[1]))
reg = json.load(open("notation/notation.json"))
macros = set(k.lstrip("\\") for k in reg["macros"])
print("registered macros used in these files:", {m: ctrl[m] for m in macros if ctrl.get(m)})
print("unregistered control words that look like symbols:")
greek = set("alpha beta gamma delta epsilon varepsilon zeta eta theta iota kappa lambda mu nu xi pi rho sigma tau phi varphi chi psi omega Gamma Delta Theta Lambda Xi Pi Sigma Phi Psi Omega varsigma tilde check hat bar".split())
print({k: v for k, v in ctrl.items() if k in greek})
