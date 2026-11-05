"""Print each line of an HTML file as its line number and visible text (all tags removed, math kept)."""
import html
import re
import sys

path = sys.argv[1]
with open(path, encoding="utf-8") as fh:
    for number, raw in enumerate(fh, 1):
        text = re.sub(r"<script.*?</script>|<style.*?</style>", "", raw, flags=re.S)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"[ \t]+", " ", html.unescape(text)).strip()
        if text:
            print(f"{number}: {text}")
