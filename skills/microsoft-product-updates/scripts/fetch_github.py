#!/usr/bin/env python3
"""Fetch GitHub changelog updates within a date window as JSON.

Uses the GitHub Blog WordPress REST API (the changelog is a WordPress custom
post type), which returns structured JSON, up to 100 items per page, and
supports server-side date filtering (`after`/`before`) and label filtering.
This is cleaner and faster than scraping the RSS feed. GitHub has no formal
lifecycle field, so the stage is inferred from title/body wording as a
best-effort guess.

Stdlib only. Usage:
    python fetch_github.py --since 2026-01-01 [--until 2026-07-01]
                           [--keyword copilot] [--label copilot]
                           [--max-pages 50]
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API = "https://github.blog/wp-json/wp/v2/changelogs"
LABEL_API = "https://github.blog/wp-json/wp/v2/label"
PER_PAGE = 100

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
    text = re.sub(r"&#8217;|&#8216;", "'", text)
    text = re.sub(r"&#8220;|&#8221;", '"', text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def infer_stage(title, body):
    haystack = f"{title} {body}"
    for stage, pattern in STAGE_PATTERNS:
        if pattern.search(haystack):
            return stage
    return "unknown"


def parse_gmt(value):
    """WordPress *_gmt fields are ISO 8601 without timezone; treat as UTC."""
    if not value:
        return None
    try:
        dt = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return None
    return dt.replace(tzinfo=timezone.utc)


def get_json(url, retries=4):
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "agent-skills/microsoft-product-updates"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.load(resp), resp.headers
        except urllib.error.HTTPError as exc:
            if exc.code == 400:  # page beyond last -> WP returns 400
                return [], {}
            last = exc
            time.sleep(2 ** attempt)
        except (urllib.error.URLError, TimeoutError) as exc:
            last = exc
            time.sleep(2 ** attempt)
    raise last


def resolve_label(slug):
    q = urllib.parse.urlencode({"slug": slug, "per_page": 100})
    data, _ = get_json(f"{LABEL_API}?{q}")
    for term in data:
        if term.get("slug") == slug:
            return term["id"]
    if data:  # fall back to first match
        return data[0]["id"]
    raise SystemExit(f"error: no changelog label matching '{slug}'")


def paged_items(since, until, label_id, max_pages):
    """Yield changelog posts using server-side date filtering, newest first."""
    params = {
        "per_page": PER_PAGE,
        "orderby": "date",
        "order": "desc",
        "after": since.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    if until:
        params["before"] = until.strftime("%Y-%m-%dT%H:%M:%S")
    if label_id is not None:
        params["label"] = label_id
    for page in range(1, max_pages + 1):
        params["page"] = page
        data, _ = get_json(f"{API}?{urllib.parse.urlencode(params)}")
        if not data:
            return
        for post in data:
            yield post
        if len(data) < PER_PAGE:
            return


def normalize(post):
    title = strip_html((post.get("title") or {}).get("rendered", ""))
    body = strip_html((post.get("content") or {}).get("rendered", ""))
    pub = parse_gmt(post.get("date_gmt"))
    return {
        "title": title,
        "link": post.get("link", ""),
        "published": pub.isoformat() if pub else None,
        "_pub": pub,
        "categories": post.get("label", []),
        "stage": infer_stage(title, body),
        "summary": body[:500],
    }


def main():
    ap = argparse.ArgumentParser(description="Fetch GitHub changelog updates within a date window as JSON.")
    ap.add_argument("--since", required=True, help="Start date (inclusive), YYYY-MM-DD.")
    ap.add_argument("--until", help="End date (inclusive), YYYY-MM-DD.")
    ap.add_argument("--keyword", action="append", default=[],
                    help="Filter to a keyword in title/summary (repeatable, case-insensitive).")
    ap.add_argument("--label", help="Scope to a changelog label slug (e.g. copilot, actions).")
    ap.add_argument("--max-pages", type=int, default=50,
                    help="Safety cap on how many API pages to fetch (default 50).")
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

    label_id = resolve_label(args.label) if args.label else None
    wants = [k.casefold() for k in args.keyword]

    out = []
    for post in paged_items(since, until, label_id, args.max_pages):
        it = normalize(post)
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
