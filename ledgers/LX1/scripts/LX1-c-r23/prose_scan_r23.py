"""Round 23 (LX1-c): scope words, process words and banned strings in the learner prose of project.html, for the
current file and for the pin 6d22ff56 version (git show), with the matches per line. A delta check: the two lists
must differ only at the changed line. Usage: python -I prose_scan_r23.py <repo_root>"""
import re
import subprocess
import sys

root = sys.argv[1]
SCOPE = re.compile(r"\b(only|all|always|every|any|same|drives|exactly)\b", re.I)
PROCESS = re.compile(r"\b(verifier|verified|round|pin|ledger|fragment|builder|mutant|mutants|agent|reviewer|slice)\b", re.I)
BANNED = re.compile(r"TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|obviously|clearly|studies show|experts agree|it is well known|About \d+%|roughly half|historically", re.I)


def learner_lines(text):
    text = re.sub(r"<pre[\s\S]*?</pre>", " ", text)
    text = re.sub(r"<script[\s\S]*?</script>", " ", text)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text)
    out = {}
    for i, line in enumerate(text.splitlines(), 1):
        plain = re.sub(r"<[^>]+>", " ", line)
        out[i] = plain
    return out


def scan(lines):
    res = {"scope": [], "process": [], "banned": []}
    for n, s in lines.items():
        for name, pat in (("scope", SCOPE), ("process", PROCESS), ("banned", BANNED)):
            for m in pat.finditer(s):
                res[name].append((n, m.group(0)))
    return res


cur = learner_lines(open(f"{root}/course/modules/LX/LX1/project.html", encoding="utf-8").read())
old_text = subprocess.run(["git", "-C", root, "show", "6d22ff56:course/modules/LX/LX1/project.html"], capture_output=True, text=True, check=True).stdout
old = learner_lines(old_text)
rc, ro = scan(cur), scan(old)
for k in ("scope", "process", "banned"):
    print(f"{k}: current {len(rc[k])} matches {rc[k]}")
    print(f"{k}: pin 6d22ff56 {len(ro[k])} matches {ro[k]}")
    print(f"{k}: differ {sorted(set(rc[k]) ^ set(ro[k]))}")
