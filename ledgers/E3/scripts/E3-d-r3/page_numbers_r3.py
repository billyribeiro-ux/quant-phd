"""Round-3 probes of the E3 project page's printed numbers, recomputed from the page's own definitions.

1. Exemplar word counts (project.html line 610): memo-text of Exemplar A and Exemplar B, tags removed, runs of
   characters between whitespace, headings included.
2. Seed-49 standard errors and the reverse-order sensitivity quoted in test_project.py lines 873-884.
3. Lab 1 printed values (project.html lines 131-137) and Lab 2 values (lines 183-186), recomputed in float.
4. Exemplar B instrument facts (project.html lines 668-679): prize range, pair 0 and pair 3, probabilities summing to 1.

Usage: .venv/bin/python -B ledgers/E3/scripts/E3-d-r3/page_numbers_r3.py <checkout-root>
"""

from __future__ import annotations

import html
import importlib.util
import json
import math
import re
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[4]
PAGE = ROOT / "course/modules/E/E3/project.html"
GRADER = ROOT / "course/modules/E/E3/grader"


def article(text: str, article_id: str) -> str:
    start = text.index(f'id="{article_id}"')
    end = text.index("</article>", start)
    return text[start:end]


def memo_texts(block: str) -> list[str]:
    out = []
    for m in re.finditer(r'<div class="memo-text">(.*?)</div>\s*</div>|<div class="memo-text">(.*?)</div>', block, re.S):
        out.append(m.group(1) if m.group(1) is not None else m.group(2))
    return out


def words(fragment: str) -> tuple[int, int]:
    plain = html.unescape(re.sub(r"<[^>]+>", " ", fragment))
    return len(plain.split()), len(re.findall(r"[^ ]+", plain))


def exemplar_counts(text: str) -> None:
    for name in ("exemplar-a", "exemplar-b"):
        block = article(text, name)
        # memo-text divs are the passages; each passage is closed by the first </div> that follows its <p>
        passages = re.findall(r'<div class="memo-text">(.*?)</p>\s*</div>', block, re.S)
        total_split = total_space = 0
        for passage in passages:
            a, b = words(passage + "</p>")
            total_split += a
            total_space += b
        print(f"{name}: passages={len(passages)} words(whitespace split)={total_split} words(space runs)={total_space}")


def load_reference():
    spec = importlib.util.spec_from_file_location("reference_mod", GRADER / "reference.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(GRADER))
    spec.loader.exec_module(mod)
    return mod


def seed49(ref_mod) -> None:
    sys.path.insert(0, str(GRADER))
    from instance import make_instance

    inst = make_instance(49)
    responses = json.loads(str(inst["responses_json"]))

    def parse(r):
        return (
            [int(x) for x in r["prizes_a"]],
            [Fraction(str(s)) for s in r["probs_a"]],
            [int(x) for x in r["prizes_b"]],
            [Fraction(str(s)) for s in r["probs_b"]],
            str(r["choice"]),
        )

    parsed = [parse(r) for r in responses]
    fit = ref_mod.estimate(responses)
    print("seed 49 reference estimate:", {k: round(v, 6) for k, v in fit.items()})

    # the test's oracle, copied from test_project.py
    def ov(x, g, lam):
        return math.pow(float(x), 1.0 - g) if x >= 0 else -lam * math.pow(float(-x), 1.0 - g)

    def op(prizes, probs, g, lam):
        total = sum(float(p) * ov(x, g, lam) for x, p in zip(prizes, probs, strict=True))
        if total >= 0.0:
            return math.pow(total, 1.0 / (1.0 - g))
        return -math.pow(-total / lam, 1.0 / (1.0 - g))

    def oll(rows, g, lam, kap):
        total = 0.0
        for pa, qa, pb, qb, choice in rows:
            z = kap * (op(pa, qa, g, lam) - op(pb, qb, g, lam)) / 10_000.0
            total += -math.log1p(math.exp(-z)) if choice == "A" else -math.log1p(math.exp(z))
        return total

    def inv3(m):
        aug = [list(row) + [1.0 if i == j else 0.0 for j in range(3)] for i, row in enumerate(m)]
        for col in range(3):
            piv = max(range(col, 3), key=lambda r: abs(aug[r][col]))
            aug[col], aug[piv] = aug[piv], aug[col]
            d = aug[col][col]
            aug[col] = [x / d for x in aug[col]]
            for r in range(3):
                if r != col:
                    f = aug[r][col]
                    aug[r] = [x - f * y for x, y in zip(aug[r], aug[col], strict=True)]
        return [row[3:] for row in aug]

    def info(rows, theta, h):
        def at(*moves):
            y = list(theta)
            for idx, amount in moves:
                y[idx] += amount
            return oll(rows, 1.0 / (1.0 + math.exp(-y[0])), math.exp(y[1]), math.exp(y[2]))

        f0 = at()
        m = [[0.0] * 3 for _ in range(3)]
        for i in range(3):
            m[i][i] = -(at((i, h)) - 2.0 * f0 + at((i, -h))) / (h * h)
            for j in range(i + 1, 3):
                v = -(at((i, h), (j, h)) - at((i, h), (j, -h)) - at((i, -h), (j, h)) + at((i, -h), (j, -h))) / (
                    4.0 * h * h
                )
                m[i][j] = m[j][i] = v
        return m

    g, lam, kap = fit["gamma_hat"], fit["lambda_hat"], fit["kappa_hat"]
    theta = [math.log(g / (1.0 - g)), math.log(lam), math.log(kap)]
    reversed_rows = list(reversed(parsed))
    for h in (1e-5, 1e-6):
        for label, rows in (("forward", parsed), ("reverse", reversed_rows)):
            cov = inv3(info(rows, theta, h))
            se = {
                "se_gamma": g * (1 - g) * math.sqrt(cov[0][0]),
                "se_lambda": lam * math.sqrt(cov[1][1]),
                "se_kappa": kap * math.sqrt(cov[2][2]),
            }
            print(f"h={h:g} {label}: " + " ".join(f"{k}={v:.6g}" for k, v in se.items()))
    # the percentage claims of the docstring
    for h in (1e-5, 1e-6):
        fwd = inv3(info(parsed, theta, h))
        rev = inv3(info(reversed_rows, theta, h))
        fl = math.sqrt(fwd[1][1]) * lam
        rl = math.sqrt(rev[1][1]) * lam
        fg = (g * (1 - g)) * math.sqrt(fwd[0][0])
        rg = (g * (1 - g)) * math.sqrt(rev[0][0])
        print(f"h={h:g}: lambda reverse vs forward {100 * (rl - fl) / fl:+.3f}%  gamma reverse vs forward {100 * (rg - fg) / fg:+.3f}%")
    # step sensitivity claims
    fl5 = lam * math.sqrt(inv3(info(parsed, theta, 1e-5))[1][1])
    fl6 = lam * math.sqrt(inv3(info(parsed, theta, 1e-6))[1][1])
    fg5 = g * (1 - g) * math.sqrt(inv3(info(parsed, theta, 1e-5))[0][0])
    fg6 = g * (1 - g) * math.sqrt(inv3(info(parsed, theta, 1e-6))[0][0])
    print(f"step 1e-6 vs 1e-5: lambda {100 * (fl6 - fl5) / fl5:+.3f}%  gamma {100 * (fg6 - fg5) / fg5:+.3f}%")
    _ = ref_mod


def lab1_and_lab2() -> None:
    import math as m

    gamma, lam, kappa, wealth = 0.40, 2.00, 1.50, 100_000

    def nearest_cent(a: float) -> int:
        return m.floor(a + 0.5)

    def crra(prizes, probs, g, w):
        finals = [w + x for x in prizes]
        e = sum(float(p) * m.pow(wv, 1.0 - g) for p, wv in zip(probs, finals, strict=True))
        return m.pow(e, 1.0 / (1.0 - g)) - w

    def pv(x, g, l):
        return m.pow(float(x), 1.0 - g) if x >= 0 else -l * m.pow(float(-x), 1.0 - g)

    def pce(prizes, probs, g, l):
        t = sum(float(p) * pv(x, g, l) for x, p in zip(prizes, probs, strict=True))
        return m.pow(t, 1.0 / (1.0 - g)) if t >= 0.0 else -m.pow(-t / l, 1.0 / (1.0 - g))

    def pa_of(ca, cb, k):
        return 1.0 / (1.0 + m.exp(-k * (ca - cb) / 10_000.0))

    pairs = [
        ([2000, -1000], [Fraction(1, 2), Fraction(1, 2)], [500], [Fraction(1)], "A"),
        ([3000], [Fraction(1)], [4000, -2000], [Fraction(1, 4), Fraction(3, 4)], "B"),
        ([1500, 2500], [Fraction(1, 3), Fraction(2, 3)], [-500, 3000], [Fraction(1, 2), Fraction(1, 2)], "A"),
    ]
    total = 0.0
    for i, (pa, qa, pb, qb, chosen) in enumerate(pairs, 1):
        ca, cb = pce(pa, qa, gamma, lam), pce(pb, qb, gamma, lam)
        print(
            f"pair {i} CRRA A,B = {nearest_cent(crra(pa, qa, gamma, wealth))} {nearest_cent(crra(pb, qb, gamma, wealth))}"
            f" | prospect A,B = {nearest_cent(ca)} {nearest_cent(cb)}"
        )
        p = pa_of(ca, cb, kappa)
        pc = p if chosen == "A" else 1 - p
        total += m.log(pc)
        print(f"pair {i} P(A)={p:.6f} chosen {chosen} log P(chosen)={m.log(pc):.6f}")
    print(f"total log-likelihood {total:.6f}")
    # Lab 2
    ca, cb, k = 1500.0, 2200.0, 2.0
    z = k * (ca - cb) / 10_000.0
    print(f"lab2 z={z}, log A={-m.log1p(m.exp(-z)):.9f}, log B={-m.log1p(m.exp(z)):.9f}")
    print(f"lab2 prob A={m.exp(-m.log1p(m.exp(-z))):.9f}, prob B={m.exp(-m.log1p(m.exp(z))):.9f}")


def exemplar_b_facts() -> None:
    import ast

    src = (GRADER / "../modules/E/E3/project.html").resolve()
    _ = src
    lab = ROOT / "tests/labs/E3/lab-E3-project-3.py"
    text = lab.read_text(encoding="utf-8")
    module = ast.parse(text)
    answers = None
    for node in module.body:
        if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", "") == "ANSWERS":
            answers = ast.literal_eval(node.value)
    assert answers is not None
    prizes = [x for a in answers for x in (a[2] + a[4])]
    print("prize min/max:", min(prizes), max(prizes))
    print("pair 0 A:", answers[0][2:4], "B:", answers[0][4:6])
    print("pair 3 A:", answers[3][2:4], "B:", answers[3][4:6])
    sums = []
    for a in answers:
        for qs in (a[3], a[5]):
            sums.append(sum(Fraction(q) for q in qs) == 1)
    print("every lottery probability sums to exactly 1:", all(sums), "count", len(sums))
    print("prize counts per lottery:", sorted({len(a[2]) for a in answers}), sorted({len(a[4]) for a in answers}))


def main() -> int:
    text = PAGE.read_text(encoding="utf-8")
    print("== exemplar word counts")
    exemplar_counts(text)
    print("== lab 1 and lab 2")
    lab1_and_lab2()
    print("== exemplar B facts")
    exemplar_b_facts()
    print("== seed 49")
    seed49(load_reference())
    return 0


if __name__ == "__main__":
    sys.exit(main())
