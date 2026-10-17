#!/usr/bin/env python3
"""Build the static site: wraps each _src/pages/*.html in _src/layout.html.

Usage: python3 build.py   (writes the pages to the repo root)

Each page starts with a metadata comment:
<!--
title: Page title
description: Meta description
nav: layanan | paket | tim | tentang | lokasi | (empty)
wa_text: Prefilled WhatsApp message for this page
og_image: og-image.jpg  (optional, defaults to the logo share image)
-->
Inside a page: {{wa}} is this page's WhatsApp link, {{wa:Some message}} a link
with a custom message, {{icon_wa}} the WhatsApp icon.
"""
import re
import time
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent
SRC = ROOT / "_src"
WA_NUMBER = "6281977888850"
# Absolute base for og:image / og:url (link previews need absolute URLs). Change when the real domain is live.
SITE_URL = "https://elrhea-redesign.pages.dev"
DEFAULT_WA_TEXT = "Halo Elrhea Clinic, saya ingin konsultasi dan booking jadwal terapi."
NAV_KEYS = ["layanan", "paket", "tim", "tentang", "lokasi"]

ICON_WA = (
    '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19.05 4.91A9.82 9.82 0 0 0 12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.91-7.01Zm-7.01 15.24h-.01a8.23 8.23 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.23 8.25-8.23a8.2 8.2 0 0 1 5.83 2.42 8.18 8.18 0 0 1 2.41 5.83c0 4.54-3.7 8.22-8.24 8.22Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.25-.64.81-.78.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.02-.38.11-.51.11-.11.25-.29.37-.43.13-.15.17-.25.25-.42.08-.17.04-.31-.02-.43-.06-.13-.56-1.34-.76-1.84-.2-.48-.41-.42-.56-.43h-.48c-.17 0-.43.06-.66.31-.22.25-.86.85-.86 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.14-1.18-.06-.1-.22-.16-.47-.29Z"/></svg>'
)


def wa_link(text):
    return f"https://wa.me/{WA_NUMBER}?text={quote(text)}"


def parse(page):
    raw = page.read_text(encoding="utf-8")
    m = re.match(r"\s*<!--(.*?)-->\s*", raw, re.S)
    meta = {}
    for line in m.group(1).strip().splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta, raw[m.end():]


def build():
    layout = (SRC / "layout.html").read_text(encoding="utf-8")
    version = time.strftime("%Y%m%d%H%M")
    for page in sorted((SRC / "pages").glob("*.html")):
        meta, body = parse(page)
        wa = wa_link(meta.get("wa_text") or DEFAULT_WA_TEXT)
        body = re.sub(r"\{\{wa:(.+?)\}\}", lambda m: wa_link(m.group(1)), body)
        html = layout.replace("{{content}}", body)
        values = {
            "title": meta["title"],
            "description": meta["description"],
            "og_image": meta.get("og_image") or "og-image.jpg",
            "site_url": SITE_URL,
            "path": "" if page.name == "index.html" else page.name[:-5],
            "wa": wa,
            "icon_wa": ICON_WA,
            "version": version,
        }
        for key in NAV_KEYS:
            current = meta.get("nav") == key
            attr = 'data-current' if key == "layanan" else 'aria-current="page"'
            values[f"current_{key}"] = attr if current else ""
        for key, value in values.items():
            html = html.replace("{{" + key + "}}", value)
        html = re.sub(r" +>", ">", html)
        leftover = re.findall(r"\{\{[^}]+\}\}", html)
        if leftover:
            raise SystemExit(f"{page.name}: unresolved {leftover}")
        (ROOT / page.name).write_text(html, encoding="utf-8")
        print("built", page.name)


if __name__ == "__main__":
    build()
