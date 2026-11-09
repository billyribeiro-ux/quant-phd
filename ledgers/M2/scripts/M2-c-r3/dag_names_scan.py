"""Scan L13-L18 for later-module concept names and links (verifier round 3). Standard library only."""
import re
terms = ["linear map", "linear-map", "vector space", "vector-space", "positive-semidefinite", "Lebesgue", "Riemann-Stieltjes",
         "Stieltjes", "Fubini", "Lagrange", "multiplier", "duration", "convexity", "compact", "measure", "epsilon-delta",
         "Hessian", "Schwarz", "implicit", "envelope", "lagrangian", "bond", "Jacobian", "norm", "metric", "topolog", "Banach",
         "sigma-algebra", "integrable", "Taylor", "mean value"]
for n in range(13, 19):
    p = f"course/modules/M/M2/L{n:02d}.html"
    txt = open(p, encoding="utf-8").read()
    body = re.sub(r"<pre.*?</pre>", "", txt, flags=re.S)
    links = re.findall(r'data-concept="([^"]+)"[^>]*href="([^"]+)"', body) + re.findall(r'href="([^"]+)"[^>]*data-concept="([^"]+)"', body)
    print(f"L{n:02d} concept links:", sorted(set(str(x) for x in links)))
    for t in terms:
        c = len(re.findall(re.escape(t), body, flags=re.I))
        if c:
            print(f"   term '{t}': {c}")
