import html, json, re, subprocess, sys
REPO = "/Users/billyribeiro/.fanout/wt/verifyG1-BK4-b"
BASE, HEAD = "95f3f8cb21c2cd9fc904430bd30a6b734d01f672", "2a805c83"
def show(path, rev):
    return subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout
def text(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(re.sub(r"\s+", " ", s)).strip()
for path in ["course/modules/BK/BK4/L04.html", "course/modules/BK/BK4/L05.html"]:
    src = show(path, HEAD)
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', src, re.S)
    t = text(m.group(1))
    print(path, "why-it-matters words:", len(t.split()))
# word counts at base for comparison
for path in ["course/modules/BK/BK4/L04.html", "course/modules/BK/BK4/L05.html"]:
    src = show(path, BASE)
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', src, re.S)
    print("BASE", path, "why-it-matters words:", len(text(m.group(1)).split()))
# scope words and process words in changed lines
hunks = subprocess.run(["git", "-C", REPO, "diff", "-U0", BASE, HEAD, "--", "course/modules/BK/BK4/L04.html", "course/modules/BK/BK4/L05.html"], capture_output=True, text=True).stdout
added = [l[1:] for l in hunks.splitlines() if l.startswith("+") and not l.startswith("+++")]
scope = re.compile(r"\b(only|all|always|every|any|same|drives|exactly|whatever|never|none)\b", re.I)
proc = re.compile(r"\b(we|this section|the lab shows|paragraph|let us|we will)\b", re.I)
for l in added:
    t = text(l)
    print("ADDED:", t[:2000])
    print("  scope:", sorted(set(x.lower() for x in scope.findall(t))), " process:", proc.findall(t), " T1:", "T1" in t)
