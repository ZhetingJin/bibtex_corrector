#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fill missing `url = {…}` fields in a BibTeX file and print every title
together with the URL that was inserted (or report that nothing was found).

• Works on Python ≥3.7.
• Needs:  pip install requests googlesearch-python
"""

import json
import re
import time
import urllib.parse
from pathlib import Path
from typing import Optional, Union

import requests

try:
    # optional – if unavailable we fall back on Crossref only
    from googlesearch import search as google_search
except ImportError:  # pragma: no cover
    google_search = None  # type: ignore

# ───────────────────────── helpers ──────────────────────────

TITLE_RX = re.compile(r"title\s*=\s*{([^}]*)}", re.I | re.S)   # supports multi‑line titles
StrOrPath = Union[str, Path]


def _clean_title(raw: str) -> str:
    """Remove LaTeX braces/commands and collapse whitespace."""
    txt = re.sub(r"[{}\\]", " ", raw)
    return re.sub(r"\s+", " ", txt).strip()


def _crossref_url(title: str, timeout: int = 10) -> Optional[str]:
    """Query Crossref and return a DOI URL (https://doi.org/...) or None."""
    try:
        params = {"query.title": title, "rows": 1}
        r = requests.get("https://api.crossref.org/works", params=params, timeout=timeout)
        if r.ok:
            items = r.json()["message"]["items"]
            if items:
                doi = items[0].get("DOI")
                if doi:
                    return f"https://doi.org/{doi}"
    except Exception:
        pass
    return None


def _google_url(title: str, pause: float = 2.0) -> Optional[str]:
    """Use google-search to grab the first result (None if nothing / error)."""
    if google_search is None:
        return None
    try:
        for url in google_search(title, num=1, stop=1, pause=pause, lang="en"):
            return url
    except Exception:
        pass
    return None

def _insert_url_field(block: str, url: str) -> str:
    """
    Insert “  url = {url},” as the penultimate line of the BibTeX entry.

    The function:
      1. removes trailing whitespace,
      2. makes sure the last existing field ends with a comma,
      3. appends the new url line,
      4. restores the closing brace and a final newline.
    """
    head, sep, _ = block.rstrip().rpartition("}")
    if not sep:                               # malformed entry, give up
        return block

    # add comma to the current last field if missing
    if not head.rstrip().endswith(","):
        head = head.rstrip() + ","

    return f"{head}\n  url = {{{url}}},\n}}\n"

# ───────────────────────── main routine ─────────────────────

def process_bib_file(inp: StrOrPath, out: StrOrPath) -> None:
    """Insert missing URLs and print a log line for every entry processed."""
    text = Path(inp).read_text(encoding="utf-8")
    blocks = re.split(r"(?=@\w+\s*{)", text)          # keep the "@entry{" delimiters
    processed = []

    for block in blocks:
        if not block.strip():
            continue

        if "url" not in block.lower():
            m = TITLE_RX.search(block)
            if m:
                title_raw = m.group(1)
                title = _clean_title(title_raw)

                print(f"🔎  {title}")

                url = (_crossref_url(title)            # 1. try Crossref
                       or _google_url(title))          # 2. fall back on Google

                if url:
                    print(f"   ↳ {url}")
                    block = _insert_url_field(block, url)
                else:
                    print("   ✘ no URL found")

        processed.append(block)

    Path(out).write_text("\n".join(processed), encoding="utf-8")

if __name__ == "__main__":
    process_bib_file("input.bib", "v1.bib")
