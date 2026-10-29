import sys, re
from html.parser import HTMLParser
# report every '<' followed by a letter in text content that the HTML tokenizer would treat as a start tag
for path in sys.argv[1:]:
    text = open(path, encoding="utf-8").read()
    for m in re.finditer(r"<([A-Za-z][A-Za-z0-9]*)\b", text):
        name = m.group(1).lower()
        known = {"p","em","h1","h2","h3","h4","h5","h6","span","div","section","a","details","summary","code","pre","ol","ul","li","table","thead","tbody","tr","th","td","strong","sup","sub","button","svg","input","label","script","figure","figcaption","select","option","header","nav","main","article","br","img","dfn","style","canvas","body","head","meta","link","title","html","footer","aside","dl","dt","dd","blockquote","hr","i","b","kbd","path","g","line","circle","rect","text","polyline","defs","use","small","abbr","wbr","noscript","template","iframe","fieldset","legend","form","textarea","progress","output","time","mark","q","cite","var","samp","del","ins","u","s","big","tt","caption","col","colgroup","hgroup","address","nobr","menu","noframes","frameset","area","map","object","param","source","track","video","audio","picture","meter","data","ruby","rt","rp","bdi","bdo","dialog","slot","search","center","font","em"}
        if name not in known:
            line = text.count("\n", 0, m.start()) + 1
            print(f"{path}:{line}: unknown tag-like '<{m.group(1)}' -> {text[m.start():m.start()+60]!r}")
    # every '<' must be followed by a letter, '/', '!' or '?' for a tag; report bare '<' followed by a letter in math
    for m in re.finditer(r"<(?=[A-Za-z])", text):
        pass
print("scan done")
