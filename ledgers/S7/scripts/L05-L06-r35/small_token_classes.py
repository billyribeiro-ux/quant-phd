"""Round-35 context classification of the small numeric tokens of S7 L05 and L06 (integers below 10 and values with
at most one decimal place), which round 34 left unclassed by value.

Rule (applied in this order to every token; the first rule that matches sets the class):
  code          the token is inside a <pre> or <code> element (a parameter or a line of code)
  year          a four-digit year (not reached for values below 10; kept for completeness)
  index         the token is a set, subscript or label: preceded by _ { ( , [ or a set brace, or within 25 characters
                after Strategy|Strategies|Rule|Predictor|Step|Problem|Lesson|Lab|Section|Remark|Definition|Theorem|
                Proposition|Lemma|Table|Figure|Item|item|card|line|lines|Algorithm|Equation|Chapter|Part|Exercise|
                Problems|M|E|P|R|F|k-|k|(n)|Solution
  locator       preceded by a page or line word: p., pp., line, lines, §, Section number, or a (n) equation label
  design        a stated design constant: preceded by a symbol and = or a comparison (rho = 0.3, T = 250, n = 20, K = 36,
                q = 0.10, alpha = 0.05) or followed by a unit noun (periods, strategies, replications, draws, blocks,
                worlds, currencies, rules, studies, specifications, variants, tests, assets, predictors, days, months,
                strategies, true, real, null, effects, digits)
  count         followed within 20 characters by a plural count noun (steps, rejections, rules, cases, items, tests,
                hypotheses, bets, columns, rows, quiz items, numbers, questions, cards, days, terms, parts)
  claim         none of the above: printed for reading (a result, probability, threshold or rate may be carried)
Writes one line per token: class<TAB>page<TAB>line<TAB>token<TAB>context.
Run: .venv/bin/python -I ledgers/S7/scripts/L05-L06-r35/small_token_classes.py > out.tsv
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
NUM = re.compile(r"(?<![\w.\-–])(\d+(?:\.\d+)?)(?![\w])(?![\-–]\d)")
INDEX_WORDS = re.compile(
    r"(Strateg(y|ies)|Rules?|Predictors?|Steps?|Problems?|Lessons?|Labs?|Sections?|Remarks?|Definitions?|Theorems?|"
    r"Propositions?|Lemmas?|Tables?|Figures?|[Ii]tems?|cards?|lines?|Algorithm|Equation|Chapter|Part|Exercise|Solution|"
    r"Questions?|Problem|k-|M|E|P|R|F|\bS)\s*[\\(]*\s*$",
    re.I,
)
LOCATOR = re.compile(r"(p\.|pp\.|§|line|lines|\(\s*$|\\\(\s*$|\bn\s*=\s*$)$", re.I)
DESIGN_BEFORE = re.compile(r"(\\?[A-Za-z]+(_\{?[\w\\]+\}?)?|\\[a-z]+|[A-Za-z]|\\pi_1|\\rho|\\alpha|\\gamma|\\phi|\\varepsilon|\\tau)\s*(=|\\le|\\ge|<|>|\\lt|\\gt|\\approx|\\in)\s*$")
DESIGN_AFTER = re.compile(r"^\s*(%|periods?|strateg(y|ies)|replications?|draws?|blocks?|worlds?|currenc(y|ies)|rules?|studies|study|specifications?|variants?|tests?|assets?|predictors?|days?|months?|effects?|real|null|true|digits?|decimals?|simulations?|observations?|dates?|bootstrap|resamples?|resamplings?|studentizations?|hypotheses|factors?|rejections?|points?)\b", re.I)
COUNT_AFTER = re.compile(r"^\s*(steps?|rejections?|cases?|items?|tests?|hypotheses|bets|columns?|rows?|numbers?|questions?|cards?|terms?|parts?|lines?|times?|ways?|rule-days|rates?|decimals?)\b", re.I)


def page_tokens(path: Path):
    in_code = False
    for i, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        code_here = in_code or bool(re.search(r"<(pre|code)\b", raw))
        if re.search(r"<pre\b", raw) and not re.search(r"</pre>", raw):
            in_code = True
        if re.search(r"</pre>", raw):
            in_code = False
        src = re.sub(r"<script.*?</script>|<style.*?</style>", "", raw, flags=re.S)
        src = re.sub(r"(?<=\d),(?=\d{3})", "", src)  # 1,000 -> 1000 (thousands separators)
        text = html.unescape(re.sub(r"<[^>]+>", " ", src))
        text = re.sub(r"\s+", " ", text)
        if not text.strip():
            continue
        for m in NUM.finditer(text):
            tok = m.group(1)
            dec = len(tok.split(".")[1]) if "." in tok else 0
            v = float(tok)
            if not (dec < 2 and v < 10):
                continue
            before = text[max(0, m.start() - 40): m.start()]
            after = text[m.end(): m.end() + 40]
            if code_here:
                cls = "code"
            elif re.fullmatch(r"(19|20)\d\d", tok):
                cls = "year"
            elif INDEX_WORDS.search(before) or re.search(r"[_{(,\[]\s*$", before) and re.search(r"\\\{|\{|_", before[-12:]):
                cls = "index"
            elif LOCATOR.search(before):
                cls = "locator"
            elif DESIGN_BEFORE.search(before) or DESIGN_AFTER.search(after):
                cls = "design"
            elif COUNT_AFTER.search(after):
                cls = "count"
            else:
                cls = "claim"
            ctx = text[max(0, m.start() - 70): m.end() + 45]
            yield cls, i, tok, ctx


if __name__ == "__main__":
    for name in ("L05", "L06"):
        for cls, line, tok, ctx in page_tokens(ROOT / "course/modules/S/S7" / f"{name}.html"):
            print(f"{cls}\t{name}\t{line}\t{tok}\t{ctx}")
