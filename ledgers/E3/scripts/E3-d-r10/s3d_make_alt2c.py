"""Round-10 verifier (E3-d): alt2c = Newton with finite differences at step 1e-6 (gradient and Hessian), Levenberg-damped
only where the Hessian is not negative definite, from the best point of a 3x3x3 start."""
import pathlib, re
HERE = pathlib.Path(__file__).resolve().parent
REF = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD10-E3-d/course/modules/E/E3/grader/reference.py").read_text(encoding="utf-8")
src = (HERE / "s3d_make_alts_v2.py").read_text(encoding="utf-8")
NEWTON_POLISH = src[src.index("NEWTON_POLISH = '''") + len("NEWTON_POLISH = '''"): src.index("'''\n\nALT1")]
MAX = '''
def _maximise(parsed: list[Parsed]) -> list[float]:
    def f(t: list[float]) -> float:
        return _objective(t, parsed)

    best_t = [0.0, 0.0, 0.0]
    best_v = -math.inf
    for c in (-2.0, 0.0, 2.0):
        for a in (-1.0, 0.5, 2.0):
            for b in (-1.0, 0.0, 1.0):
                v = f([c, a, b])
                if v > best_v:
                    best_v, best_t = v, [c, a, b]
    return _newton_polish(f, best_t)
'''
text = REF.replace("_H = 1e-5  # finite-difference step in the transformed coordinates", "_H = 1e-6  # finite-difference step in the transformed coordinates", 1)
pat = re.compile(r"^def _maximise\(.*?(?=^def |\Z)", re.S | re.M)
m = pat.search(text)
text = text[: m.start()] + MAX.lstrip("\n") + "\n\n" + text[m.end():]
text = text.replace("def _maximise", NEWTON_POLISH.lstrip("\n") + "\n\ndef _maximise", 1)
d = HERE / "alts" / "alt2c_newton_fd1e-6_damped"
d.mkdir(parents=True, exist_ok=True)
(d / "elicit.py").write_text(text, encoding="utf-8")
print("wrote", d / "elicit.py")
