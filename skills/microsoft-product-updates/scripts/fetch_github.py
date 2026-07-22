#!/usr/bin/env python3
"""Fetch GitHub changelog updates within a date window as JSON.

Parses the GitHub changelog RSS feed (there is no JSON API), filters items by
publication date, and emits a normalized JSON array to stdout. GitHub has no
formal lifecycle field, so the stage is inferred from title/body wording and
returned as a best-effort guess.

Stdlib only. Usage:
    python fetch_github.py --since 2026-01-01 [--until 2026-07-01]
                           [--keyword copilot] [--year 2026]
"""
import argparse
import json
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree

FEED = "https://github.blog/changelog/feed/"
CONTENT_NS = "{http://purl.org/rss/1.0/modules/content/}encoded"

# Ordered most-specific first; first match wins.
STAGE_PATTERNS = (
    ("retirement", re.compile(r"\b(deprecat|retir|sunset|end of life|no longer)\b", re.I)),
    ("ga", re.compile(r"\b(generally available|general availability|now available|\bGA\b)\b", re.I)),
    ("public-preview", re.compile(r"\b(public preview|in preview|now in beta|public beta)\b", re.I)),
    ("private-preview", re.compile(r"\b(private preview|limited (public )?preview|early access|technical preview)\b", re.I)),
    ("in-development", re.compile(r"\b(coming soon|in development|on the roadmap)\b", re.I)),
)


def strip_html(html):
    text = re.sub(r"(?s)<[^>]+>", " ", html or "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def infer_stage(title, body):
    haystack = f"{title} {body}"
    for stage, pattern in STAGE_PATTERNS:
        if pattern.search(haystack):
            return stage
    return "unknown"


def parse_date(value):
    try:
        dt = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    if dt is None:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def fetch(url, retries=4):
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "agent-skills/microsoft-product-updates"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return ElementTree.parse(resp).getroot()
        except (urllib.error.URLError, TimeoutError) as exc:
            last = exc
            time.sleep(2 ** attempt)
    raise last


def items(root):
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub = parse_date(item.findtext("pubDate"))
        categories = [c.text.strip() for c in item.findall("category") if c.text]
        encoded = item.findtext(CONTENT_NS) or item.findtext("description") or ""
        body = strip_html(encoded)
        yield {
            "title": title,
            "link": link,
            "published": pub.isoformat() if pub else None,
            "_pub": pub,
            "categories": categories,
            "stage": infer_stage(title, body),
            "summary": body[:500],
        }


def main():
    ap = argparse.ArgumentParser(description="Fetch GitHub changelog updates within a date window as JSON.")
    ap.add_argument("--since", required=True, help="Start date (inclusive), YYYY-MM-DD.")
    ap.add_argument("--until", help="End date (inclusive), YYYY-MM-DD.")
    ap.add_argument("--keyword", action="append", default=[],
                    help="Filter to a keyword in title/summary (repeatable, case-insensitive).")
    ap.add_argument("--year", type=int, action="append", default=[],
                    help="Fetch a specific year's archive feed (repeatable). Defaults to the current feed.")
    args = ap.parse_args()

    try:
        since = datetime.strptime(args.since, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        until = (
            datetime.strptime(args.until, "%Y-%m-%d").replace(
                hour=23, minute=59, second=59, tzinfo=timezone.utc)
            if args.until else None
        )
    except ValueError:
        print("error: dates must be YYYY-MM-DD", file=sys.stderr)
        return 2

    urls = [f"https://github.blog/changelog/{y}/feed/" for y in args.year] or [FEED]
    wants = [k.casefold() for k in args.keyword]

    out = []
    for url in urls:
        for it in items(fetch(url)):
            pub = it.pop("_pub")
            if pub is None or pub < since or (until and pub > until):
                continue
            if wants:
                hay = f"{it['title']} {it['summary']}".casefold()
                if not any(w in hay for w in wants):
                    continue
            out.append(it)

    out.sort(key=lambda x: x["published"] or "", reverse=True)
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
