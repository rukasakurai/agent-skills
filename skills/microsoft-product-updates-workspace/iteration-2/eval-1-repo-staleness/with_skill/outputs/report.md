# eval-1 repo-staleness — WITH skill (agent it2-e1-with, 310s)

Read-only; no repo changes.

## Findings
- skills/microsoft-foundry-resources/SKILL.md → Client SDK row "Microsoft Agent SDK (.NET) / Microsoft.Agents.AI.*". Azure update: Microsoft Foundry introducing Agent Framework, unified multi-agent SDK for C# and Python — https://azure.microsoft.com/updates?id=564312 — Medium (feed doesn't confirm exact package names).
- skills/microsoft-foundry-resources/SKILL.md → Agent Framework may also warrant mentioning Copilot/Claude Code connectors — https://azure.microsoft.com/updates?id=563701 — Low/Medium.
- No high-confidence stale GitHub CLI / Agent Skills claims; recent GitHub updates additive (Copilot CLI GA, C++ LSP skill).

## Sources used
- Azure API: https://www.microsoft.com/releasecommunications/api/v2/azure?$count=true&$top=100&$skip=0&$orderby=modified+desc
- GitHub changelog RSS: https://github.blog/changelog/feed/ plus ?paged=2..10
- GitHub Copilot label RSS: https://github.blog/changelog/label/copilot/feed/ plus ?paged=2..5

Oldest GitHub entry considered: 2026-06-18T18:04:33Z.

## Difficulties
Azure update web pages not useful via fetch; used structured JSON API. Several Agent Framework items had ambiguous lifecycle (stage: review, ring Effective). GitHub RSS required pagination.
