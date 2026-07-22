I'll start by reading the skill file.

● Read SKILL.md
  │ skills/microsoft-product-updates/SKILL.md
  └ 95 lines read

● List scripts directory (shell)
  │ cd /home/rusakura/code/github.com/rukasakurai/agent-skills/skills/microsoft-product-updates &&
  │ ls -R scripts/
  └ 8 lines…

● Fetch Azure updates for window (shell)
  │ cd /home/rusakura/code/github.com/rukasakurai/agent-skills/skills/microsoft-product-updates &&
  │ python scripts/fetch_azure.py --since 2026-06-21 --until 2026-07-21 > /tmp/azure.json
  │ 2>/tmp/azure.err; echo "exit=$?"; head -c 300 /tmp/azure.err; echo; python -c "import
  │ json;d=json.load(open('/tmp/azure.json'));print('total',len(d))"
  └ 4 lines…

● Count stages (shell)
  │ cd /tmp && python3 -c "
  │ import json
  │ d=json.load(open('azure.json'))
  │ from collections import Counter
  │ print(Counter(x['stage'] for x in d))…
  └ 3 lines…

● Inspect item schema (shell)
  │ cd /tmp && python3 -c "
  │ import json
  │ d=json.load(open('azure.json'))
  │ print(json.dumps(d[0],indent=1)[:1500])
  │ "
  └ 22 lines…

● List preview and review items with signals (shell)
  │ cd /tmp && python3 -c "
  │ import json
  │ d=json.load(open('azure.json'))
  │ for x in d:
  │ if x['stage'] in ('public-preview','private-preview','review'):…
  └ 76 lines…

## Azure preview items — 2026-06-21 → 2026-07-21

Fetched via the skill's `scripts/fetch_azure.py --since 2026-06-21 --until 2026-07-21` (43 items total). Excluded 17 GA and 3 retirement. Below are items in preview or with ambiguous lifecycle signals.

### Public preview (10) — clear signals (`status: In preview`, `ring: Preview`)
1. Protect sensitive generative AI telemetry in Application Insights and Microsoft Foundry — id 567594
2. Azure SQL updates for mid-July 2026 — 567426
3. Advanced platform metrics in Azure Monitor — 567726
4. Azure Front Door edge actions — 567402
5. Manage Azure Chaos Studio from the Azure CLI — 567225
6. Exceptions in WAF for Azure Application Gateway and Azure Front Door — 567218
7. Azure Chaos Studio Workspaces and Scenarios — 567184
8. Export historical data from Log Analytics workspace with Export jobs — 566591
9. Instant Access via application consistent restore points — 565758
10. Application Gateway for Containers – Inference gateway — 566516

**Private preview: 0** (none had `ring: Private Preview` as their sole/resolved stage).

### ⚠️ Flagged for review (13) — conflicting/ambiguous signals, stage NOT auto-assigned
Signals disagree, so per the skill these are `stage: review` — verify by reading each linked update:

- Title/status conflict (title=preview vs `status: Launched`, likely preview sub-capability):
  - Azure Functions Support for PowerShell 7.6 — 567651
  - Document PII playground sample in Microsoft Foundry NextGen — 563331
  - Azure Storage Mover now supports migration from GCS — 566948
- Title=preview vs `status: In preview` but `ring: General Availability`:
  - Azure NetApp Files migration assistant — 565480
- Announcement lifecycle not corroborated (`ring: Effective`, no status) — Microsoft Agent Framework series:
  - GitHub Copilot and Claude Code connectors — 563701
  - Multi-agent orchestration patterns including Magentic — 563571
  - Agent Harness — 563546
  - Multi-agent orchestration SDK (C#/Python) — 564312
  - Tracing (Python/.NET) — 564071
  - CodeAct pattern and Hyperlight containers — 563566
  - Episodic procedural memory — 563561
  - Agent Channel for multi-agent communication — 563556
  - DevUI Agent Inspector — 563551

## Source used (exact endpoint)
`https://www.microsoft.com/releasecommunications/api/v2/azure` (paginated OData JSON, `$orderby=modified desc`), accessed via the skill's `scripts/fetch_azure.py`.

**Total preview items found: 10** confirmed in public/private preview (all public), **plus 13 flagged for review** (ambiguous — some are likely preview but signals conflict).

