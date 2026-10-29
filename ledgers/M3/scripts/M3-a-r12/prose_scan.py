"""Word count of each why-it-matters paragraph, banned-phrase and process-word scan over the M3 slice pages."""
import html
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1]) / "course/modules/M/M3"
banned = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "it can be shown", "In this lesson we", "Let us", "In summary"]
process = [r"\bround\b", r"\bverifier", r"\bbuilder", r"\bagent\b", r"\bdraft\b", r"\bplaceholder\b",
           r"\bgrader\b", r"\bnot yet\b", r"\bpending\b"]
for name in ["index.html", "L01.html", "L02.html", "L03.html"]:
    text = (root / name).read_text(encoding="utf-8")
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', text, re.S)
    if m:
        print(name, "why-it-matters words:", len(html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).split()))
    plain = html.unescape(re.sub(r"<[^>]+>", " ", text))
    for b in banned:
        for hit in re.finditer(re.escape(b), plain, re.I):
            print(name, "BANNED", repr(b), "at offset", hit.start())
    for p in process:
        for hit in re.finditer(p, plain, re.I):
            print(name, "PROCESS", repr(p), repr(plain[max(0, hit.start() - 40):hit.end() + 40]))
    for hit in re.finditer(r"\.\.\.", plain):
        print(name, "ELLIPSIS", repr(plain[max(0, hit.start() - 30):hit.end() + 20]))
print("scan complete")
