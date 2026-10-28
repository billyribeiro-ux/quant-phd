# Scans the learner text of L05.html and L06.html for BUILDER_RULES 1.2/1.3 banned strings and process words (run -I).
import re, sys, html
pat = re.compile(r"TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|"
                 r"roughly half|about 6%|historically|it is important to note|studies show|experts agree|"
                 r"it is well known|obviously|clearly|it can be shown that|\.\.\.|…|"
                 r"\bbuilder\b|\bbuild\b|\bround\b|\bverifier\b|\bREQUESTS\b|unit report|\bagent\b", re.I)
for page in sys.argv[1:]:
    src = open(page, encoding="utf-8").read()
    body = re.sub(r"<pre.*?</pre>", " ", src, flags=re.S)  # code and expected output excluded
    body = re.sub(r"<script.*?</script>", " ", body, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", body))
    hits = [(m.group(0), text[max(0, m.start()-60):m.end()+40].replace("\n", " ")) for m in pat.finditer(text)]
    print(page, "hits", len(hits))
    for h in hits:
        print("  ", h[0], "|", h[1])
