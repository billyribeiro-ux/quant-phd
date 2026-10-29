"""Round 3 M2-a: banned-phrase and scope-word scan over visible prose (scripts outside <pre> blocks)."""
import html, os, re
M2 = "/tmp/verifyB3-M2-a/course/modules/M/M2"
banned = (r"\b(roughly|about|historically|typically|usually|generally|often|commonly|approximately|half|percent|"
          r"build|builder|round|verifier|REQUEST|process|several|most|always|every|all|only|any|same|drives|"
          r"offsets|raises|as much as|clearly|obviously|trivially|known)\b|\.\.\.")
for p in ["index.html"] + [f"L0{i}.html" for i in range(1, 7)]:
    s = open(os.path.join(M2, p), encoding="utf8").read()
    s = re.sub(r"<script.*?</script>|<style.*?</style>|<pre.*?</pre>", "", s, flags=re.S)
    t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s)))
    for m in re.finditer(banned, t, flags=re.I):
        print(p, "|", t[max(0, m.start() - 70): m.end() + 50])
