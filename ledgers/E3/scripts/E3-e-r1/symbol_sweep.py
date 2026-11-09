"""Whole-page sweep of math segments for single-letter and renamed symbols in E3 slice pages.
Math = \\( ... \\), \\[ ... \\], and $...$ inside <p>/<td>/<li>, HTML-unescaped."""
import html, re, sys, pathlib
root = pathlib.Path(sys.argv[1]) / "course/modules/E/E3"
targets = {
    "a": r"(?<![A-Za-z\\])a(?![A-Za-z])",
    "b": r"(?<![A-Za-z\\])b(?![A-Za-z])",
    "W": r"(?<![A-Za-z\\])W(?![A-Za-z])|\\mathrm\{W\}",
    "PV": r"\\mathrm\{PV\}|(?<![A-Za-z\\])PV(?![A-Za-z])",
    "Omega": r"\\Omega|(?<![A-Za-z\\])Omega",
    "Xi": r"\\Xi|(?<![A-Za-z\\])Xi",
    "rho": r"\\rho|(?<![A-Za-z\\])rho",
    "tau": r"\\tau|(?<![A-Za-z\\])tau",
    "iota": r"\\iota|(?<![A-Za-z\\])iota",
    "check": r"\\check",
    "tilde": r"\\tilde",
    "phi": r"\\phi|\\varsigma",
    "epsilon": r"\\epsilon|\\varepsilon",
    "eta": r"\\eta",
    "v": r"(?<![A-Za-z\\])v(?![A-Za-z])",
    "T": r"(?<![A-Za-z\\])T(?![A-Za-z])",
    "Phi": r"\\Phi",
    "Q": r"(?<![A-Za-z\\])Q(?![A-Za-z])|\\mathbb\{Q\}",
    "R_f": r"R_f|R_\{f\}",
    "gamma_3": r"\\gamma_3|\\gamma_4",
    "R_ast": r"R\^\\ast|R\^\{\\ast\}|R\^\{e\\ast\}",
    "kappa": r"\\kappa|kappa",
    "epsilon_plain": r"(?<![A-Za-z\\])eps(?![A-Za-z])",
}
math_re = re.compile(r"\\\((.+?)\\\)|\\\[(.+?)\\\]|\$\$(.+?)\$\$|\$([^$\n]+?)\$", re.S)
for f in ["index.html"] + [f"L0{i}.html" for i in range(1, 9)]:
    text = (root / f).read_text(encoding="utf-8")
    # strip script/pre (code is not math)
    body = re.sub(r"<script.*?</script>|<style.*?</style>", "", text, flags=re.S)
    for m in math_re.finditer(body):
        seg = html.unescape(next(g for g in m.groups() if g is not None))
        line = body.count("\n", 0, m.start()) + 1
        for name, pat in targets.items():
            hits = re.findall(pat, seg)
            if hits:
                print(f"{f}:{line}\t{name}\t{len(hits)}\t{seg[:110]!r}")
