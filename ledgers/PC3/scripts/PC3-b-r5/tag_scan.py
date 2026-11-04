import re, sys
from html.parser import HTMLParser
from pathlib import Path
ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE5-PC3-b/course/modules/PC/PC3")
VOID = {"area","base","br","col","embed","hr","img","input","link","meta","source","track","wbr"}
class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.stack=[]; self.errs=[]
    def handle_starttag(self, tag, attrs):
        if tag not in VOID: self.stack.append((tag, self.getpos()))
    def handle_startendtag(self, tag, attrs): pass
    def handle_endtag(self, tag):
        if tag in VOID: return
        if not self.stack: self.errs.append(("extra close", tag, self.getpos())); return
        t,pos=self.stack.pop()
        if t!=tag: self.errs.append(("mismatch", t, tag, self.getpos()))
total=0
for lid in ["L04","L05","L06"]:
    txt=(ROOT/f"{lid}.html").read_text(encoding="utf-8")
    # strip script/style and lab code blocks for raw '<' scan
    body=re.sub(r'<pre><code class="language-python" data-run>.*?</code></pre>','',txt,flags=re.S)
    body=re.sub(r'<pre class="expected".*?</pre>','',body,flags=re.S)
    raw=re.findall(r'<(?![A-Za-z/!?])', body)
    rawletter=re.findall(r'<(?=[^A-Za-z/!?<\s][^>]*$)', "")
    p=P(); p.feed(txt); p.close()
    unclosed=p.stack
    print(lid, "parse errors", len(p.errs), p.errs[:3], "unclosed", len(unclosed), "raw '<' outside code:", len(raw))
    total+=len(p.errs)+len(unclosed)+len(raw)
print("TOTAL", total)
