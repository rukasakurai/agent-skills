#!/usr/bin/env python3
"""Fetch Azure release-communication updates within a date window as JSON.

Pages the Azure release communications OData API (newest first) until items
fall before the requested start date, then emits a normalized JSON array to
stdout. Each item's lifecycle stage is resolved from the API's several
(sometimes conflicting) signals; conflicts are reported as stage "review"
with the disagreeing signals attached, rather than guessed.

Stdlib only. Usage:
    python fetch_azure.py --since 2026-01-01 [--until 2026-07-01]
                          [--product "Azure Functions"] [--page-size 100]
"""
import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API = "https://www.microsoft.com/releasecommunications/api/v2/azure"

# API status -> stage
STATUS_STAGE = {
    "launched": "ga",
    "in preview": "public-preview",
    "in development": "in-development",
}
# availabilities[].ring -> stage
RING_STAGE = {
    "general availability": "ga",
    "preview": "public-preview",
    "public preview": "public-preview",
    "private preview": "private-preview",
    "retirement": "retirement",
}
# title prefixes -> stage (order matters: most specific first)
TITLE_PREFIX_STAGE = (
    ("Generally Available", "ga"),
    ("General Availability", "ga"),
    ("Public Preview", "public-preview"),
    ("Private Preview", "private-preview"),
    ("In Development", "in-development"),
    ("Retirement", "retirement"),
    ("Preview", "public-preview"),
    ("GA", "ga"),
)
EDITORIAL_PREFIXES = ("Announcing", "New")
PREVIEW_STAGES = {"public-preview", "private-preview"}


def title_signals(raw_title):
    title = (raw_title or "").lstrip("\ufeff\u200b").strip()
    for prefix, stage in TITLE_PREFIX_STAGE:
        m = re.match(rf"^{re.escape(prefix)}\s*:\s*", title, re.IGNORECASE)
        if m:
            return title[m.end():].strip(), prefix, stage
    for prefix in EDITORIAL_PREFIXES:
        m = re.match(rf"^{re.escape(prefix)}\s*:\s*", title, re.IGNORECASE)
        if m:
            return title[m.end():].strip(), prefix, None
    return title, None, None


def ring_signals(item):
    rings, stages = [], []
    for a in item.get("availabilities") or []:
        ring = (a.get("ring") or "").strip()
        if not ring:
            continue
        rings.append(ring)
        stage = RING_STAGE.get(ring.casefold())
        if stage and stage not in stages:
            stages.append(stage)
    return rings, stages


def stages_compatible(title_stage, status_stage):
    if title_stage == status_stage:
        return True
    return status_stage == "public-preview" and title_stage in PREVIEW_STAGES


def rings_support(stage, ring_stages, include_private=False):
    s = set(ring_stages)
    if stage == "ga":
        return "ga" in s
    if stage == "public-preview":
        allowed = {"public-preview"} | ({"private-preview"} if include_private else set())
        return bool(s & allowed) and "ga" not in s
    if stage == "private-preview":
        return "private-preview" in s and "public-preview" not in s and "ga" not in s
    if stage == "in-development":
        return "in-development" in s
    if stage == "retirement":
        return "retirement" in s
    return False


def resolve_stage(item):
    """Resolve one item's lifecycle stage from title/status/ring/tags."""
    title, title_prefix, title_stage = title_signals(item.get("title", ""))
    raw_status = (item.get("status") or "").strip()
    status_stage = STATUS_STAGE.get(raw_status.casefold())
    rings, ring_stages = ring_signals(item)
    tag_names = {t.casefold() for t in (item.get("tags") or [])}
    retirement_tag = "retirements" in tag_names
    announcement = (title_prefix or "").casefold() == "announcing" or "announcement" in tag_names

    stage = None
    candidate = None
    reason = None

    if title_stage:
        if status_stage and not stages_compatible(title_stage, status_stage):
            candidate, reason = title_stage, "title prefix and API status disagree"
        elif ring_stages and not rings_support(title_stage, ring_stages):
            candidate, reason = title_stage, "title prefix and availability disagree"
        else:
            stage = title_stage
    elif announcement:
        if status_stage and rings_support(status_stage, ring_stages, include_private=True):
            stage = status_stage
            if status_stage == "public-preview" and set(ring_stages) == {"private-preview"}:
                stage = "private-preview"
        else:
            candidate, reason = status_stage, "announcement lifecycle is not corroborated"
    elif status_stage:
        if ring_stages and not rings_support(status_stage, ring_stages, include_private=True):
            candidate, reason = status_stage, "API status and availability disagree"
        else:
            stage = status_stage
            if status_stage == "public-preview" and set(ring_stages) == {"private-preview"}:
                stage = "private-preview"
    elif len(ring_stages) == 1:
        stage = ring_stages[0]
    elif retirement_tag:
        stage = "retirement"
    else:
        reason = "no lifecycle stage could be determined"

    result = {
        "id": str(item.get("id") or ""),
        "title": title,
        "stage": stage or "review",
        "status": raw_status,
        "rings": rings,
        "tags": item.get("tags") or [],
        "products": item.get("products") or [],
        "modified": item.get("modified"),
        "created": item.get("created"),
        "link": f"https://azure.microsoft.com/updates?id={item.get('id')}" if item.get("id") else None,
    }
    if reason:
        result["review"] = {"reason": reason, "candidate": candidate or ""}
    return result


def parse_iso(value):
    if not value:
        return None
    v = value.replace("Z", "+00:00")
    # Normalize fractional seconds to 6 digits (API emits 7; fromisoformat
    # on Python < 3.11 accepts only 0, 3, or 6 digits).
    m = re.match(r"(.*\.\d{6})\d*([+-]\d\d:\d\d)?$", v)
    if m:
        v = m.group(1) + (m.group(2) or "")
    try:
        dt = datetime.fromisoformat(v)
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def _get_json(url, retries=4):
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "agent-skills/microsoft-product-updates"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.load(resp)
        except (urllib.error.URLError, TimeoutError) as exc:
            last = exc
            time.sleep(2 ** attempt)
    raise last


def fetch(since, until, page_size):
    skip = 0
    while True:
        qs = urllib.parse.urlencode(
            {"$count": "true", "$top": page_size, "$skip": skip, "$orderby": "modified desc"},
            safe="$",
        )
        data = _get_json(f"{API}?{qs}")
        items = data.get("value", [])
        if not items:
            return
        for it in items:
            modified = parse_iso(it.get("modified"))
            if modified is None:
                continue
            if modified < since:
                return
            if until and modified > until:
                continue
            yield it
        skip += page_size


def main():
    ap = argparse.ArgumentParser(description="Fetch Azure updates within a date window as JSON.")
    ap.add_argument("--since", required=True, help="Start date (inclusive), YYYY-MM-DD.")
    ap.add_argument("--until", help="End date (inclusive), YYYY-MM-DD.")
    ap.add_argument("--product", action="append", default=[],
                    help="Filter to a product name (repeatable, case-insensitive substring).")
    ap.add_argument("--page-size", type=int, default=100)
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

    wants = [p.casefold() for p in args.product]
    out = []
    for item in fetch(since, until, args.page_size):
        if wants:
            products = " ".join(item.get("products") or []).casefold()
            if not any(w in products for w in wants):
                continue
        out.append(resolve_stage(item))
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
