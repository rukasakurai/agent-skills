I'll find the authoritative Azure updates feed and query it. Let me start.

● Test Azure release communications API (shell)
  │ curl -s "https://www.microsoft.com/releasecommunications/api/v2/azure?$top=5" -H "Accept:
  │ application/json" | head -c 2000
  └ 23 lines…

● Test Azure updates RSS feed (shell)
  │ curl -s "https://azure.microsoft.com/en-us/updates/feed/" | head -c 1500
  └ 1 line…

The first was blocked. Let me query the release communications API correctly.

● Query release communications API with top=3 (shell)
  │ curl -s "https://www.microsoft.com/releasecommunications/api/v2/azure?%24top=3" -H "Accept:
  │ application/json" | head -c 3000
  └ 2 lines…

API works. Let me inspect the full field structure and find the date field for ordering.

● List all fields of an item (shell)
  │ curl -s "https://www.microsoft.com/releasecommunications/api/v2/azure?%24top=1" -H "Accept:
  │ application/json" | python3 -c "import json,sys; d=json.load(sys.stdin);
  │ print(list(d['value'][0].keys()))"
  └ 2 lines…

● Inspect recent items ordered by created (shell)
  │ curl -s "https://www.microsoft.com/releasecommunications/api/v2/azure?%24orderby=created%20des
  │ c&%24top=3" -H "Accept: application/json" | python3 -c "
  │ import json,sys
  │ d=json.load(sys.stdin)
  │ for i in d['value']:…
  └ 16 lines…

Clear structure. Let me fetch recent items and filter for the date range with preview logic.

● Fetch 300 recent items (shell)
  │ curl -s "https://www.microsoft.com/releasecommunications/api/v2/azure?%24orderby=created%20desc&
  │ %24top=300" -H "Accept: application/json" -o /tmp/azupd.json; python3 -c "import
  │ json;d=json.load(open('/tmp/azupd.json'));print('count:',len(d['value']));print('oldest
  │ created:',d['value'][-1]['created'])"
  └ 3 lines…

100 items reach back to 2026-06-02, covering our window. Let me analyze.

● Filter preview items in date window (shell)
  │ python3 << 'EOF'
  │ import json
  │ d=json.load(open('/tmp/azupd.json'))
  │ start="2026-06-21"; end="2026-07-21"
  │ preview=[]; flagged=[]…
  └ 77 lines…

Analysis complete. The "Effective"/"Retirement"/"Announcing" items have a single clear non-preview ring, so they're excluded rather than flagged. Only genuine signal conflicts are flagged.

# Azure Preview Updates (2026-06-21 → 2026-07-21)

Items still **only in preview** (no General Availability signal):

| # | Lifecycle stage | Date | Update |
|---|---|---|---|
| 1 | Public Preview | 2026-06-24 | Application Gateway for Containers – Inference gateway |
| 2 | Public Preview | 2026-07-01 | Instant Access via application consistent restore points |
| 3 | Public + Private Preview | 2026-07-07 | Azure Chaos Studio Workspaces and Scenarios |
| 4 | Public Preview | 2026-07-07 | Exceptions in WAF for Azure Application Gateway and Azure Front Door |
| 5 | Public + Private Preview | 2026-07-07 | Export historical data from Log Analytics workspace with Export jobs |
| 6 | Public Preview | 2026-07-09 | Manage Azure Chaos Studio from the Azure CLI |
| 7 | Public Preview | 2026-07-14 | Azure Front Door edge actions |
| 8 | Public Preview | 2026-07-15 | Advanced platform metrics in Azure Monitor |
| 9 | Public Preview | 2026-07-15 | Azure SQL updates for mid-July 2026 |
| 10 | Public + Private Preview | 2026-07-20 | Protect sensitive generative AI telemetry in Application Insights and Microsoft Foundry |

## ⚠️ Flagged for review (conflicting lifecycle signals)
Titled "Public Preview" and carry a Preview availability ring, but `status = Launched` with **no** GA date — preview vs. launched conflict:

- **Azure Functions Support for PowerShell 7.6** (2026-07-17) — ring=Preview, status=Launched, GA=none
- **Document PII playground sample in Microsoft Foundry NextGen** (2026-07-01) — ring=Preview, status=Launched, GA=none
- **Azure Storage Mover supports migration from Google Cloud Storage (GCS)** (2026-07-01) — ring=Preview, status=Launched, GA=none

(Note: "Announcing"/"Effective" and "Retirement" items in-window carry non-preview rings and were excluded as not-preview, not flagged.)

## Source used (exact endpoint)
`https://www.microsoft.com/releasecommunications/api/v2/azure?$orderby=created desc&$top=300` (public Azure Updates release-communications API; filtered client-side by `created` date and `availabilities`/`status`/GA-date fields). No secrets used.

**Total preview items found: 10** (plus 3 flagged for review).

