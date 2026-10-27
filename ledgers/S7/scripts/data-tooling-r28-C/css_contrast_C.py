"""Round-28 part C: WCAG 2.x contrast re-derivation of the numbers quoted in course.css comments (lines 1117-1119 for
--cell-strong-opacity, 1213 for .chart .bar, 1328 for .chart .cell.strong). Every colour is read from course.css
(the file the S7 pages load; tokens.css is not loaded by them). Light = the :root block, dark = the data-theme="dark"
block (the media-query dark block gives the same values; checked below). Composite fill = series colour at the given
opacity source-over --bg. Run: python -I css_contrast_C.py <checkout>"""
import re
import sys

ROOT = sys.argv[1]
css = open(f"{ROOT}/course/assets/css/course.css", encoding="utf-8").read()


def blocks(pattern):
    """Bodies of every block whose opening line matches pattern, in document order."""
    out = []
    for m in re.finditer(pattern, css):
        out.append(css[m.start():css.index("}", m.start())])
    return out


def first_with(bodies, name):
    return next(b for b in bodies if re.search(r"--" + re.escape(name) + r":", b))


def value(body, name):
    m = re.search(r"--" + re.escape(name) + r":\s*([^;]+);", body)
    return m.group(1).strip() if m else None


ROOT_RE = r"\n:root \{"
DARK_RE = r':root\[data-theme="dark"\] \{'
root_blocks = blocks(ROOT_RE)
dark_blocks = blocks(DARK_RE)
light_core = first_with(root_blocks, "bg")
light_chart = first_with(root_blocks, "chart-0")
dark_core = first_with(dark_blocks, "bg")
dark_chart = first_with(dark_blocks, "chart-0")
themes = {
    "light": {k: value(light_chart, k) for k in ["chart-0", "chart-1", "chart-2", "chart-3", "chart-4", "chart-5", "cell-strong-opacity"]},
    "dark": {k: value(dark_chart, k) for k in ["chart-0", "chart-1", "chart-2", "chart-3", "chart-4", "chart-5", "cell-strong-opacity"]},
}
themes["light"].update(bg=value(light_core, "bg"), ink=value(light_core, "ink"))
themes["dark"].update(bg=value(dark_core, "bg"), ink=value(dark_core, "ink"))
media = blocks(r'@media \(prefers-color-scheme: dark\) \{\s*:root:not\(\[data-theme="light"\]\) \{')
print("media-query dark chart and opacity equal data-theme dark:",
      {k: value(media[1], k) == themes["dark"][k] for k in ["chart-0", "chart-1", "chart-5", "cell-strong-opacity"]} if len(media) > 1 else media)
def lum(hexc):
    h = hexc.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def blend(fg, bg, alpha):
    f = [int(fg.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    b = [int(bg.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    return "#" + "".join(f"{round(alpha * x + (1 - alpha) * y):02x}" for x, y in zip(f, b))


claims = {}
for theme, v in themes.items():
    bg, ink = v["bg"], v["ink"]
    ch = {k: v[f"chart-{k}"] for k in "012345"}
    op = float(v["cell-strong-opacity"])
    print(f"== {theme}: bg {bg} ink {ink} strong-cell opacity {op} series0 {ch['0']}")
    fill0 = blend(ch["0"], bg, op)
    print(f"  [strong] series 0 fill vs --bg {ratio(fill0, bg):.4f}  (comment: 3.1:1 in both themes)")
    print(f"  [strong] --ink vs series 0 fill {ratio(ink, fill0):.4f}  (comment: 5.2 light, 5.0 dark)")
    others_bg = {k: ratio(blend(ch[k], bg, op), bg) for k in "12345"}
    others_ink = {k: ratio(ink, blend(ch[k], bg, op)) for k in "12345"}
    print(f"  [strong] series 1-5 fill vs --bg min {min(others_bg.values()):.4f} (series {min(others_bg, key=others_bg.get)}) (comment: 2.6:1)")
    print(f"  [strong] series 1-5 --ink vs fill min {min(others_ink.values()):.4f} (series {min(others_ink, key=others_ink.get)}) (comment: 4.4:1)")
    print(f"  [stroke] series 0 colour vs its own strong fill {ratio(ch['0'], fill0):.4f}  (comment: 2.4 light, 2.9 dark)")
    bar = {k: ratio(blend(ch[k], bg, 0.75), bg) for k in "012345"}
    print(f"  [bar 0.75] min over series 0-5 vs --bg {min(bar.values()):.4f} (series {min(bar, key=bar.get)}) (comment: 3.3 or more; lowest series 5 light)")
    bar55 = {k: ratio(blend(ch[k], bg, 0.55), bg) for k in "012345"}
    print(f"  [bar 0.55] min over series 0-5 vs --bg {min(bar55.values()):.4f} (series {min(bar55, key=bar55.get)}) (comment: 2.3:1)")
