"""Reference-registry tooling: parse curriculum source strings, resolve them
against Crossref, and maintain the verified citation registry.

The registry (``references/references.json``) is the only legal citation
source for course pages. An entry enters it only when its bibliographic
metadata has been resolved from Crossref, so citation fields are
machine-sourced rather than typed from memory.
"""
