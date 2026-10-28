# Plain-text extraction of M5 lesson pages for line-by-line reading (keeps "<" that is math, not a tag).
import html
import re
import sys

KNOWN = set("a abbr b body br button caption code col dd details div dfn dl dt em fieldset figure figcaption footer h1 h2 h3 h4 h5 h6 head header html i input kbd label legend li link main meta nav ol option p pre s script section select small span strong style sub summary sup svg table tbody td template textarea tfoot th thead title tr u ul img path g rect line circle polyline text defs marker use noscript iframe canvas aside article time mark q blockquote cite hr address output progress meter".split())


def fix(s: str) -> str:
    def rep(m: re.Match[str]) -> str:
        if m.group(1).lower() in KNOWN or m.group(0).startswith("</"):
            return m.group(0)
        return "&lt;" + m.group(0)[1:]

    return re.sub(r"<([a-zA-Z][^\s/>]*)", rep, s)


def main(path: str, out: str) -> None:
    s = fix(open(path, encoding="utf-8").read())
    s = re.sub(r"<script.*?</script>", "", s, flags=re.S)
    s = re.sub(r"<style.*?</style>", "", s, flags=re.S)
    s = re.sub(r"</?(br|p|li|h[1-6]|div|tr|section|pre|details|summary)\b[^>]*>", "\n", s)
    s = re.sub(r"<[a-zA-Z/!][^>]*>", "", s)
    s = html.unescape(s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    open(out, "w", encoding="utf-8").write(s)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
