"""P-14: every in-page #anchor and href target on project.html exists; P-06: (99n+99)//100 equals ceil(0.99 n) for n in 1..20000."""
import re, math, pathlib
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB11-M4-d")
M4 = ROOT / "course/modules/M/M4"
page = (M4 / "project.html").read_text(encoding="utf-8")
ids = set(re.findall(r'\sid="([^"]+)"', page))
frag = set(re.findall(r'href="#([^"]+)"', page))
print("in-page anchors missing:", sorted(frag - ids))
rel = set(re.findall(r'href="([^"#]+)', page))
missing = [r for r in sorted(rel) if not (M4 / r).exists()]
print("relative href targets checked:", sorted(rel))
print("relative href targets missing on disk:", missing)
bad = [n for n in range(1, 20001) if (99 * n + 99) // 100 != math.ceil(0.99 * n) and (99 * n + 99) // 100 != -(-99 * n // 100)]
print("n in 1..20000 where (99n+99)//100 != ceil(0.99n) (exact integer ceil):", bad[:5], len(bad))
