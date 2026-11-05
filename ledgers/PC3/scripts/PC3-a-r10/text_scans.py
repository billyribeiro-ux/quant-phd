"""Round-10 PC3 slice a: scope words, process words, and forbidden D-terms in the stripped text views of the slice pages."""
import re
import sys

SCOPE = r"\b(every|all|always|never|any|same|only|exactly|drives|none)\b"
PROCESS = r"\b(build|builder|builders|round|verifier|verifiers|REQUESTS|unit report|fixer)\b"
DTERMS = (r"martingale|stopping time|optional stopping|Poisson|Kelly|Markov|CAPM|duration|Gordon|"
          r"binomial distribution|permutation|combination|adverse selection|winner|Nash|common-value|"
          r"probability space|Bayesian inference|probability of informed trading|inventory model|roll")
for path in sys.argv[1:]:
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            for label, pattern in (("SCOPE", SCOPE), ("PROCESS", PROCESS), ("DTERM", DTERMS)):
                hits = re.findall(pattern, line, flags=re.I)
                if hits:
                    print(f"{label} {path.split('/')[-1]} {line.split(':', 1)[0]}: {sorted(set(h.lower() for h in hits))}")
