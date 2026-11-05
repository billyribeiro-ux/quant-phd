"""Round-10 verifier (E3-d): alt3 = hand-written Nelder-Mead (bounded iterations) + damped Newton polish;
alt5 = float implementation with exp/log arithmetic for the prospect CE (a different float path) and the same half-up rule."""
import pathlib, re
HERE = pathlib.Path(__file__).resolve().parent
REF = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD10-E3-d/course/modules/E/E3/grader/reference.py").read_text(encoding="utf-8")
v2 = (HERE / "s3d_make_alts_v2.py").read_text(encoding="utf-8")
NEWTON_POLISH = v2[v2.index("NEWTON_POLISH = '''") + len("NEWTON_POLISH = '''"): v2.index("'''\n\nALT1")]
NM = '''
def _nelder_mead(f, x0: list[float], scale: float) -> list[float]:
    n = len(x0)
    simplex = [list(x0)]
    for i in range(n):
        p = list(x0)
        p[i] += scale
        simplex.append(p)
    vals = [f(p) for p in simplex]
    for _ in range(4000):
        order = sorted(range(n + 1), key=lambda k: vals[k])
        simplex = [simplex[k] for k in order]
        vals = [vals[k] for k in order]
        spread = max(abs(simplex[k][i] - simplex[0][i]) for k in range(1, n + 1) for i in range(n))
        if vals[-1] - vals[0] < 1e-13 and spread < 1e-10:
            break
        centroid = [sum(simplex[k][i] for k in range(n)) / n for i in range(n)]
        worst = simplex[-1]
        xr = [centroid[i] + (centroid[i] - worst[i]) for i in range(n)]
        fr = f(xr)
        if fr < vals[0]:
            xe = [centroid[i] + 2.0 * (centroid[i] - worst[i]) for i in range(n)]
            fe = f(xe)
            simplex[-1], vals[-1] = (xe, fe) if fe < fr else (xr, fr)
        elif fr < vals[-2]:
            simplex[-1], vals[-1] = xr, fr
        else:
            xc = [centroid[i] + 0.5 * (worst[i] - centroid[i]) for i in range(n)]
            fc = f(xc)
            if fc < vals[-1]:
                simplex[-1], vals[-1] = xc, fc
            else:
                for k in range(1, n + 1):
                    simplex[k] = [simplex[0][i] + 0.5 * (simplex[k][i] - simplex[0][i]) for i in range(n)]
                    vals[k] = f(simplex[k])
    return simplex[min(range(n + 1), key=lambda k: vals[k])]
'''
MAX3 = '''
def _maximise(parsed: list[Parsed]) -> list[float]:
    def f(t: list[float]) -> float:
        value = _objective(t, parsed)
        return -value if math.isfinite(value) else math.inf

    x = _nelder_mead(f, [0.0, 0.5, 0.0], 0.5)
    x = _nelder_mead(f, x, 0.05)
    return _newton_polish(lambda t: _objective(t, parsed), x)
'''
t3 = REF.replace("def _maximise", NM.lstrip("\n") + "\n" + NEWTON_POLISH.lstrip("\n") + "\n\ndef _maximise", 1)
m = re.compile(r"^def _maximise\(.*?(?=^def |\Z)", re.S | re.M).search(t3)
t3 = t3[: m.start()] + MAX3.lstrip("\n") + "\n\n" + t3[m.end():]
ALT5 = '''
def _prospect_ce(prizes: list[int], probs: list[Fraction], gamma: float, lam: float) -> float:
    """Unrounded prospect CE in floats through exp and log (a different float path), not the power function."""
    total = 0.0
    for x, p in zip(prizes, probs, strict=True):
        if x > 0:
            v = math.exp((1.0 - gamma) * math.log(float(x)))
        elif x == 0:
            v = 0.0
        else:
            v = -lam * math.exp((1.0 - gamma) * math.log(float(-x)))
        total += float(p) * v
    if total > 0.0:
        return math.exp(math.log(total) / (1.0 - gamma))
    if total == 0.0:
        return 0.0
    return -math.exp(math.log(-total / lam) / (1.0 - gamma))
'''
t5 = REF.replace("def _prospect_ce", ALT5.lstrip("\n") + "\n\ndef _prospect_ce_unused", 1)
for name, text in {"alt3_nelder_mead_v2": t3, "alt5_exp_log_float": t5}.items():
    d = HERE / "alts" / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "elicit.py").write_text(text, encoding="utf-8")
    print("wrote", d / "elicit.py")
