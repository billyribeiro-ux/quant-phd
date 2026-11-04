"""Scan the four slice pages' visible text for process words, banned strings and out-of-closure concept names."""
import re, sys
from pathlib import Path
terms = [r"\bround\b", r"\bbuild\w*", r"\bverifier\w*", r"REQUESTS", r"unit report", r"\bfutures?\b",
         r"variation margin", r"\brepo\b", r"haircut", r"bank reserves?", r"central bank", r"value.at.risk",
         r"expected shortfall", r"stress.test", r"monte.carlo", r"\bvariance\b", r"covariance", r"correlation",
         r"liquidity coverage", r"net stable", r"safe asset", r"model risk", r"credit default", r"recovery waterfall",
         r"bank run", r"run on", r"liquidity spiral", r"tokeni[sz]", r"Basel", r"Duffie", r"CPMI", r"\bSEC\b",
         r"T\+1", r"\bGaussian\b", r"\bnormal\b", r"volatil", r"procyclic", r"\bstress\b", r"\bmutual\w*",
         r"\bwidely\b", r"\bstudies\b", r"\bexperts?\b", r"\bobviously\b", r"\bclearly\b", r"\.\.\.", r"\bTODO\b",
         r"\bTBD\b", r"\bcurriculum\b", r"\bsnapshot\b", r"\bdataset\b", r"\breal\b"]
for name in sys.argv[1:]:
    text = Path(name).read_text(encoding="utf-8")
    for pat in terms:
        for m in re.finditer(pat, text, re.I):
            line = text.count("\n", 0, m.start()) + 1
            ctx = text[max(0, m.start() - 60): m.end() + 40].replace("\n", " ")
            print(f"{Path(name).name}:{line} [{m.group()}] ...{ctx}...")
