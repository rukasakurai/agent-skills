---
name: microsoft-product-updates
description: 'Fetch and interpret recent Microsoft product updates (Azure and GitHub) from their authoritative change feeds — the Azure release communications JSON API and the GitHub changelog RSS feed — reading lifecycle signals (GA, public/private preview, in development, retirement) consistently. Use when you need "what recently changed for product Y" over a date window, e.g. checking whether pinned versions or GA/preview claims in a repo have gone stale.'
argument-hint: Name the product area (Azure and/or GitHub) and the date window you care about
---

# Microsoft Product Updates

## When to Use

- You need recent updates for an Azure or GitHub product over a date window ("what changed since <date>").
- You are checking whether a repo's GA/preview claims, retirements, or pinned versions have gone stale.
- For "what is the latest stable version of X to pin", use `latest-stable-version` instead — this skill answers "what recently *changed*", not "what version to pin".

This skill explains how to obtain and read updates. Keep repo-specific cross-referencing (e.g. comparing against pinned Bicep API versions) in the consuming repo.

## Sources

| Product | Endpoint | Shape |
| --- | --- | --- |
| Azure | `https://www.microsoft.com/releasecommunications/api/v2/azure` | Paginated OData JSON |
| GitHub | `https://github.blog/changelog/feed/` | RSS 2.0 (no JSON API) |

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

These signals can disagree (e.g. `title` says `Public Preview` while `status` is `Launched` because a feature GA'd but a sub-capability is still in preview). Prefer `availabilities[].ring`; when signals conflict, report the item as ambiguous rather than guessing.

## GitHub (RSS feed)

No structured API — parse the RSS. The feed is the current year's archive; older years live at `https://github.blog/changelog/YYYY/feed/`.

```sh
curl -s https://github.blog/changelog/feed/
```

Per `<item>`: `<title>`, `<link>`, `<pubDate>` (RFC 822 — filter your window on this), `<category>`, and `<content:encoded>` (full HTML). GitHub has no formal ring field; infer lifecycle from title/body wording ("generally available", "public preview", "deprecated", "sunset", "retired").

## Lifecycle Mapping

Normalize both sources to one vocabulary:

| Stage | Azure signal | GitHub wording |
| --- | --- | --- |
| GA | `ring: General Availability` / `status: Launched` / title `Generally Available` | "generally available", "GA" |
| Public preview | `ring: Preview` / `status: In preview` / title `Public Preview` | "public preview", "beta" |
| Private preview | `ring: Private Preview` / title `Private Preview` | "private preview", "limited" |
| In development | `status: In development` | "coming soon", "in development" |
| Retirement | `ring: Retirement` / `tags: Retirements` | "deprecated", "retired", "sunset" |
