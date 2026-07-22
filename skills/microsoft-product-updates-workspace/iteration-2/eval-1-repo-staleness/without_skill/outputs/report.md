# eval-1 repo-staleness — WITHOUT skill / baseline (agent it2-e1-without, 429s)

Read-only; did not inspect skills/microsoft-product-updates/.

## Findings
1. skills/microsoft-foundry-resources/SKILL.md → Client SDK lists only .NET / Microsoft.Agents.AI.*. Update: Foundry Agent Framework now has unified C# AND Python SDKs. Source: https://www.microsoft.com/releasecommunications/api/v2/azure/564312 — High.
2. Same file → may need GA wording. Update: Agent Harness in Microsoft Agent Framework GA for .NET and Python. Source: https://www.microsoft.com/releasecommunications/api/v2/azure/563546 — Medium.
3. README / gh CLI skill guidance → no required update; v2.90.0+ minimum not contradicted by v2.96.0. — Medium.

## Sources used
- Azure RSS: https://www.microsoft.com/releasecommunications/api/v2/azure/rss
- Azure detail API: https://www.microsoft.com/releasecommunications/api/v2/azure/{id}
- GitHub changelog RSS: https://github.blog/changelog/feed/
- GitHub changelog REST (WordPress): https://github.blog/wp-json/wp/v2/changelogs?per_page=100&page=1
- GitHub CLI releases: https://api.github.com/repos/cli/cli/releases

Oldest GitHub entry considered: 2026-06-18.

## Difficulties
Azure old /updates/feed/ redirects to HTML; usable feed is the Release Communications RSS/API.
