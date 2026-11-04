"""Round-8 verifier (FC1-c): strip the lesson HTML to line-numbered text (tags removed, entities unescaped; no content edited)."""
import html, pathlib, re, sys
root = pathlib.Path(sys.argv[1]); out = pathlib.Path(sys.argv[2])
for n in ["L01", "L02", "L03", "L04", "L05"]:
    src = (root / f"course/modules/FC/FC1/{n}.html").read_text(encoding="utf-8")
    src = re.sub(r"(?s)<script.*?</script>|<style.*?</style>", "", src)
    src = re.sub(r"(?i)<br\s*/?>|</(p|li|h[1-6]|tr|div|section|pre|dt|dd|table)>", "\n", src)
    txt = html.unescape(re.sub(r"</?[a-zA-Z][^>]*>", "", src))
    lines = [l.strip() for l in txt.splitlines()]
    lines = [l for l in lines if l]
    (out / f"{n}.txt").write_text("\n".join(f"{i+1:4d}: {l}" for i, l in enumerate(lines)) + "\n", encoding="utf-8")
    print(n, len(lines), "lines", sum(len(l) for l in lines), "chars")
