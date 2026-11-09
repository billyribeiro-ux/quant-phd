"""Round-13 prose scans for E4 slice b (L04, L05, L06): banned phrases, process words, scope words, notation, ordering, counts."""
import html
import json
import re

ROOT = "/Users/billyribeiro/.fanout/wt/verifyF31-E4-b"
LESSONS = ("L04", "L05", "L06")
BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "can be shown", "roughly", "historically", "it is easy to see", "trivially", "of course"]
PROCESS = re.compile(r"\b(agent|fragment|workflow|script|this slice|verifier|builder|ledger|round)\b", re.I)
SCOPE = re.compile(r"\b(only|all|always|every|any|same|drives|exactly)\b", re.I)
REGISTERED = {"T", "Phi", "gamma_3", "gamma_4", "R^\\ast", "R^{e\\ast}", "R_f", "\\mathbb{Q}"}
REG_MACROS = {"\\E", "\\Prob", "\\Var", "\\Cov", "\\Corr", "\\R", "\\N", "\\indic", "\\Normal", "\\iid", "\\dto",
              "\\pto", "\\argmax", "\\argmin", "\\tr", "\\diag", "\\SR", "\\hSR", "\\PSR", "\\DSR", "\\PBO", "\\FWER",
              "\\FDR", "\\FDP", "\\se", "\\emgamma"}
STD_OK = set()

notation = json.load(open(f"{ROOT}/notation/notation.json", encoding="utf-8"))
assert set(REG_MACROS) == set(notation["macros"]), "macro registry drifted from the script's copy"

for L in LESSONS:
    raw = open(f"{ROOT}/course/modules/E/E4/{L}.html", encoding="utf-8").read()
    body = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", " ", raw, flags=re.S)))
    math = [a or b for a, b in re.findall(r"\\\((.+?)\\\)|\\\[(.+?)\\\]", raw, re.S)]
    print(f"== {L}")
    print(" banned hits:", [p for p in BANNED if p.lower() in body.lower()])
    print(" process-word hits:", sorted(set(m.group(0) for m in PROCESS.finditer(body))))
    print(" scope-word count:", len(SCOPE.findall(body)))
    cmds = sorted(set(re.findall(r"\\[A-Za-z]+", " ".join(math))))
    print(" macros used:", " ".join(cmds))
    print(" registered-symbol hits in math:", [m[:60] for m in math if re.search(r"(?<![A-Za-z])T(?![A-Za-z])|R_f|R\^\\ast|R\^\{e|mathbb\{Q\}|\\Phi|\\gamma", m)])
    probs = re.findall(r'<div class="problem" id="([^"]+)"', raw)
    sols = re.findall(r'<details class="solution">(.*?)</details>', raw, re.S)
    words = [len(re.sub(r"<[^>]+>", " ", s).split()) for s in sols]
    print(f" problems {len(probs)} solutions {len(sols)} solution words min {min(words)} max {max(words)}")
    wim = re.search(r'<p class="why-it-matters">(.*?)</p>', raw, re.S).group(1)
    print(f" why-it-matters words {len(html.unescape(re.sub(r'<[^>]+>', ' ', wim)).split())}")
    print(" data-concept links:", len(re.findall(r'data-concept="', raw)))
    print(" B1/B3 hits:", len(re.findall(r"\bB[13]\b", body)))

raw6 = open(f"{ROOT}/course/modules/E/E4/L06.html", encoding="utf-8").read()
first_vu = raw6.find("V_U")
first_b = raw6.find("\\E[v \\mid p] = b\\, p")
print("== L06 ordering: first V_U at char", first_vu, "line", raw6[:first_vu].count("\n") + 1)
print("   first b=... definition at line", raw6[:first_b].count("\n") + 1)
cards = json.load(open(f"{ROOT}/course/modules/E/E4/cards.json", encoding="utf-8"))
pat = PROCESS
print("== cards: process-word hits", [c["id"] for c in cards if c["lesson"] in LESSONS and pat.search(c["front"] + " " + c["back"] + " " + (c.get("basis") or ""))])
