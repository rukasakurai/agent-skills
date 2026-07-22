---
name: microsoft-product-updates
description: 'Fetch and interpret recent Microsoft product updates (Azure and GitHub) from their authoritative change feeds — the Azure release communications JSON API and the GitHub changelog WordPress REST API — reading lifecycle signals (GA, public/private preview, in development, retirement) consistently. Use when you need "what recently changed for product Y" over a date window, e.g. checking whether pinned versions or GA/preview claims in a repo have gone stale.'
argument-hint: Name the product area (Azure and/or GitHub) and the date window you care about
---

# Microsoft Product Updates

## When to Use

- You need recent updates for an Azure or GitHub product over a date window ("what changed since <date>").
- You are checking whether a repo's GA/preview claims, retirements, or pinned versions have gone stale.
- For "what is the latest stable version of X to pin", use `latest-stable-version` instead — this skill answers "what recently *changed*", not "what version to pin".

This skill explains how to obtain and read updates. Keep repo-specific cross-referencing (e.g. comparing against pinned Bicep API versions) in the consuming repo.

Cost/latency: using this skill is roughly cost- and latency-neutral versus not using it (it ties on quality while being no more expensive and typically faster) — see `evals/benchmark.md` for measured numbers and their date/model.

## Fetching Updates

Two stdlib-only Python scripts (no `pip install`) do the deterministic work — pagination, date-window filtering, and lifecycle normalization — and emit a normalized JSON array. Prefer them over hand-rolling requests.

```sh
# Azure updates modified on/after a date, optionally filtered by product
python scripts/fetch_azure.py --since 2026-01-01 [--until 2026-07-01] [--product "Azure Functions"]

# GitHub changelog entries published in a window, optionally filtered by keyword
python scripts/fetch_github.py --since 2026-01-01 [--until 2026-07-01] [--keyword copilot] [--label copilot]
```

Each output item carries a normalized `stage` (`ga`, `public-preview`, `private-preview`, `in-development`, `retirement`, plus `review`/`unknown`), the source `title`/`link`, dates, and the raw signals. Azure items whose signals disagree get `stage: "review"` with a `review.reason`; resolve those by reading the linked update rather than trusting one signal.

The sources and fields are documented below so you can query them directly (e.g. `curl`) when the scripts don't fit.

## Sources

| Product | Endpoint | Shape |
| --- | --- | --- |
| Azure | `https://www.microsoft.com/releasecommunications/api/v2/azure` | Paginated OData JSON |
| GitHub | `https://github.blog/wp-json/wp/v2/changelogs` | WordPress REST JSON |

Both are public; no auth or secrets.

## Azure (JSON API)

Query newest-first and page with `$top`/`$skip`. Each item is under `value[]`; `@odata.count` is the total.

```sh
curl -s 'https://www.microsoft.com/releasecommunications/api/v2/azure?$count=true&$top=100&$skip=0&$orderby=modified+desc'
```

Page by incrementing `$skip` by `$top` until items fall before your date window (they are sorted by `modified`). Relevant fields per item:

- `title` — often prefixed with the lifecycle, e.g. `Generally Available:`, `Public Preview:`.
- `status` — `Launched`, `In preview`, `In development`.
- `availabilities[].ring` — `General Availability`, `Preview`, `Private Preview`, `Retirement` (the most reliable lifecycle signal).
- `tags` — includes `Retirements` for deprecations.
- `products`, `productCategories` — filter to your product area.
- `modified`, `created`, `generalAvailabilityDate`, `previewAvailabilityDate`, `privatePreviewAvailabilityDate` — dates.
- `description` — HTML body.

These signals can disagree (e.g. `title` says `Public Preview` while `status` is `Launched` because a feature GA'd but a sub-capability is still in preview). Prefer `availabilities[].ring`; when signals conflict, report the item as ambiguous rather than guessing. `fetch_azure.py` implements this resolution and emits such items as `stage: "review"`.

Note: `modified`/`created` use 7-digit fractional seconds (e.g. `2026-07-20T15:09:43.6800215Z`), which `datetime.fromisoformat` rejects before Python 3.11 — truncate to 6 digits before parsing (the script handles this).

## GitHub (WordPress REST API)

The changelog is a WordPress custom post type, so query its REST API directly — structured JSON, up to 100 items/page, with **server-side date and label filtering**. No auth. `fetch_github.py` uses this.

```sh
# Entries in a window (after/before filter on post date; page beyond the last returns HTTP 400)
curl -s 'https://github.blog/wp-json/wp/v2/changelogs?per_page=100&after=2026-06-18T00:00:00&before=2026-07-21T23:59:59&orderby=date&order=desc'
# Scope to a label: resolve its term id, then pass ?label=<id>
curl -s 'https://github.blog/wp-json/wp/v2/label?slug=copilot'   # -> id, e.g. 2765
curl -s 'https://github.blog/wp-json/wp/v2/changelogs?per_page=100&label=2765'
```

Response headers `X-WP-Total` / `X-WP-TotalPages` give the totals; page with `&page=N`. Relevant fields per item:

- `title.rendered`, `link` — headline and URL.
- `date_gmt` / `modified_gmt` — ISO 8601 UTC (no offset suffix; treat as UTC). Filter your window on `date_gmt`.
- `content.rendered` — full HTML body.
- `label` — array of taxonomy term ids (resolve via the `label` endpoint above).

GitHub has no formal ring field; infer lifecycle from title/body wording ("generally available", "public preview", "deprecated", "sunset", "retired").

## Lifecycle Mapping

Normalize both sources to one vocabulary:

| Stage | Azure signal | GitHub wording |
| --- | --- | --- |
| GA | `ring: General Availability` / `status: Launched` / title `Generally Available` | "generally available", "GA" |
| Public preview | `ring: Preview` / `status: In preview` / title `Public Preview` | "public preview", "beta" |
| Private preview | `ring: Private Preview` / title `Private Preview` | "private preview", "limited" |
| In development | `status: In development` | "coming soon", "in development" |
| Retirement | `ring: Retirement` / `tags: Retirements` | "deprecated", "retired", "sunset" |
