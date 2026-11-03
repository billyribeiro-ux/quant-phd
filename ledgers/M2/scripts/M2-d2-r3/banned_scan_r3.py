# Scan slice pages and twins for banned strings, scope words and concept names outside the closure. Usage: python -I <script> <root>
import html, os, re, sys
root = os.path.abspath(sys.argv[1])
files = ["course/modules/M/M2/L22.html", "course/modules/M/M2/L23.html", "course/modules/M/M2/L24.html",
         "tests/labs/M2/lab-M2-L22-1.py", "tests/labs/M2/lab-M2-L23-1.py", "tests/labs/M2/lab-M2-L24-1.py"]
terms = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
         "you can add more", "important to note", "studies show", "experts agree", "well known", "obviously", "clearly",
         "in practice", "typically", "most", "fast", "smooth", "small", "always", "every", "only", "exactly", "drives",
         "any", "same", "multiplier", "Lagrang", "Fubini", "Lebesgue", "Stieltjes", "epsilon-delta", "continuity",
         "duration", "convexity", "Jacobian", "Hessian", "linear map", "vector space", "positive-semidefinite", "matrix",
         "bond", "mathbb", "builder", "verifier", "ledger", "twin", "fragment", "architect", "planner", "REQUEST", "agent",
         "orchestrat", "campaign", "...", "…", "Riemann", "variance", "covariance", "expected", "Cauchy", "Taylor"]
for f in files:
    raw = open(os.path.join(root, f), encoding="utf-8").read()
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw)) if f.endswith(".html") else raw
    print("==", f, "chars", len(text))
    for t in terms:
        for m in re.finditer(re.escape(t), text, flags=re.I):
            s = text[max(0, m.start() - 60): m.end() + 40].replace("\n", " ")
            ln = text.count("\n", 0, m.start()) + 1
            print("  [%s] line~%d: ...%s..." % (t, ln, s))
