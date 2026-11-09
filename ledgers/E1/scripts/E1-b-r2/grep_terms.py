"""List every visible-text line of the L04-L06 pages (tags stripped, code blocks removed) that contains a term from a watch list."""
import re
import sys

WATCH = re.compile(
    r"nash|lagrang|convex|concav|expected utility|welfare theorem|kkt|pareto|public good|externalit|surplus|"
    r"deadweight|utility|edgeworth|reaction function|competitive equilibrium|process|verif|builder|round|"
    r"unit report|requests|todo|tbd|lorem|clearly|obviously|studies show|experts|well known|checked directly|"
    r"verified|checked|\.\.\.|every|all |always|never|any |only|exactly|welfare|market structure|real|data",
    re.I,
)
for path in sys.argv[1:]:
    text = open(path, encoding="utf-8").read()
    text = re.sub(r"<pre><code.*?</code></pre>", "", text, flags=re.S)
    text = re.sub(r"<pre class=\"expected\".*?</pre>", "", text, flags=re.S)
    text = re.sub(r"<script.*?</script>", "", text, flags=re.S)
    text = re.sub(r"<style.*?</style>", "", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    for n, line in enumerate(text.split("\n"), 1):
        for m in WATCH.finditer(line):
            s = max(0, m.start() - 70)
            e = min(len(line), m.end() + 50)
            print(f"{path.split('/')[-1]} L{n}: ...{' '.join(line[s:e].split())}...  [{m.group(0)}]")
