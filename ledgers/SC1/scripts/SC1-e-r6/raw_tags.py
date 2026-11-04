"""Report HTML start tags that the parser sees inside a lesson's raw source; a raw '<' followed by a letter inside math
starts a fake tag, so the browser hides the text up to the next '>'. Usage: raw_tags.py <page.html>"""
import sys
from html.parser import HTMLParser

class T(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.bad: list[tuple[str, int]] = []
    def handle_starttag(self, tag, attrs):  # type: ignore[no-untyped-def]
        if not tag.isalpha() and tag not in ("h1","h2","h3","h4","p","li","ul","ol","dd","dt","td","th","tr","tbody","thead","table","code","pre","span","em","strong","a","div","section","details","summary","sup","sub","dfn","img","br","hr","svg","path","g","text","rect","line","circle","tspan","title","desc","i","b","small","figure","figcaption","header","main","nav","footer","article","aside","label","input","button","select","option","textarea","form","body","html","head","meta","link","script","style","noscript","iframe","canvas","object","param","source","video","audio","abbr","cite","kbd","samp","var","time","q","mark","thead","caption","col","colgroup","tfoot","blockquote","dl","address","wbr","fieldset","legend","progress","meter","output","data","del","ins","s","u","big","tt","strike","center","font","base","area","map","embed","track"):
            self.bad.append((tag, self.getpos()[0]))
        elif tag.isalpha() and tag not in ("p","li","ul","ol","dd","dt","td","th","tr","tbody","thead","table","code","pre","span","em","strong","a","div","section","details","summary","sup","sub","dfn","img","br","hr","svg","path","g","text","rect","line","circle","tspan","title","desc","i","b","small","figure","figcaption","header","main","nav","footer","article","aside","label","input","button","select","option","textarea","form","body","html","head","meta","link","script","style","noscript","iframe","canvas","object","param","source","video","audio","abbr","cite","kbd","samp","var","time","q","mark","caption","col","colgroup","tfoot","blockquote","dl","address","wbr","fieldset","legend","progress","meter","output","data","del","ins","s","u","big","tt","strike","center","font","base","area","map","embed","track","h1","h2","h3","h4","h5","h6","table","colgroup"):
            self.bad.append((tag, self.getpos()[0]))

p = T()
p.feed(open(sys.argv[1], encoding="utf-8").read())
print(len(p.bad), "start tags with a non-HTML name:", p.bad[:30])
