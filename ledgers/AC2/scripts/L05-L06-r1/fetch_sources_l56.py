"""Re-read the four L05-L06 sources that are reachable by plain HTTP, and record every status.

Written by the L05-L06 verifier. Crossref (api.crossref.org) is queried with a User-Agent that carries no
personal data. Publisher pages behind a bot check are NOT bypassed: the script records the HTTP status and the
page title only, and does not retry with other headers. Run: python -I fetch_sources_l56.py
"""

import json
import re
import urllib.error
import urllib.request

DOIS = {
    "sloan1996stock": "10.2308/tar-9608042309",
    "dechow1995detecting": "10.2308/tar-9505096112",
    "mclean2016academic": "10.1111/jofi.12365",
    "hou2018replicating": "10.1093/rfs/hhy131",
}
UA = "ac2-verifier/1.0 (no contact)"


def get(url: str) -> tuple[int, str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", "replace")
            return resp.status, resp.geturl(), body
    except urllib.error.HTTPError as err:
        body = err.read().decode("utf-8", "replace")
        return err.code, err.geturl(), body


for key, doi in DOIS.items():
    status, final, body = get(f"https://api.crossref.org/works/{doi}")
    print(f"== {key} crossref HTTP {status}")
    if status == 200:
        msg = json.loads(body)["message"]
        print("title:", " ".join(msg.get("title", [])))
        print("authors:", [f"{a.get('family')}, {a.get('given')}" for a in msg.get("author", [])])
        print("container/volume/issue/pages:", msg.get("container-title"), msg.get("volume"), msg.get("issue"), msg.get("page"))
        abstract = re.sub(r"<[^>]+>", " ", msg.get("abstract", ""))
        print("abstract:", " ".join(abstract.split()))
    s2, final2, body2 = get(f"https://doi.org/{doi}")
    title = re.search(r"<title>([^<]*)</title>", body2)
    print(f"publisher via doi.org HTTP {s2} final {final2} page_title {title.group(1) if title else None!r}")
    print()
