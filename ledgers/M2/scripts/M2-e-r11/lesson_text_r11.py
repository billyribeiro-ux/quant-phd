"""Print tag-stripped text of one M2 lesson page (scripts, styles removed; entities decoded; whitespace squeezed)."""
import html, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
raw = re.sub(r"<style.*?</style>", " ", raw, flags=re.S)
print(re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw))))
