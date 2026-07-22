I'll start by reading the skill file.

● Read SKILL.md
  │ skills/microsoft-product-updates/SKILL.md
  └ 95 lines read

Now let me explore the scripts and the repo structure.

● List directory .
  └ 4 files found

● List directory skills
  └ 6 files found

● List skill directory contents (shell)
  │ cd /home/rusakura/code/github.com/rukasakurai/agent-skills && ls -R
  │ skills/microsoft-product-updates
  └ 16 lines…

Let me examine the scripts and scan the repo for pinned versions and lifecycle claims.

● Read fetch_azure.py
  │ skills/microsoft-product-updates/scripts/fetch_azure.py
  └ 248 lines read

● Read fetch_github.py
  │ skills/microsoft-product-updates/scripts/fetch_github.py
  └ 180 lines read

Now let me find pinned versions and lifecycle claims across the repo.

● List each skill's files (shell)
  │ cd /home/rusakura/code/github.com/rukasakurai/agent-skills && for d in skills/*/; do echo "===
  │ $d ==="; ls "$d"; done
  └ 16 lines…

/ Search (grep)
  │ "\b(20\d{2}-\d{2}-\d{2}|api-version|apiVersion|GA|generally available|public preview|private
  │ preview|preview|retire|deprecat|sunset|version|@\d)\b" (skills/latest-stable-version,
  │ skills/microsoft-foundry-resources, skills/draft-github-issue, skills/authoring-agent-skills,
  │ README.md)
  └ 3 files found

● Read SKILL.md
  │ skills/latest-stable-version/SKILL.md
  └ 43 lines read

● Read SKILL.md
  │ skills/microsoft-foundry-resources/SKILL.md
  └ 82 lines read

● Read README.md
  └ 56 lines read

● List workspace dir (shell)
  │ cd /home/rusakura/code/github.com/rukasakurai/agent-skills && ls -R
  │ skills/microsoft-product-updates-workspace | head -50
  └ 50 lines…

Now let me USE the skill's scripts to fetch the updates for the window (2026-06-21 → 2026-07-21). Starting both fetches in parallel.

● Fetch all GitHub changelog entries in window (shell)
  │ cd /home/rusakura/code/github.com/rukasakurai/agent-skills/skills/microsoft-product-updates &&
  │ python3 scripts/fetch_github.py --since 2026-06-21 --until 2026-07-21 > /tmp/gh_all.json
  │ 2>/tmp/gh_err.txt; echo "exit=$?"; wc -c /tmp/gh_all.json; head -c 300 /tmp/gh_err.txt
  └ 3 lines…

● Fetch all Azure updates in window (shell)
  │ cd /home/rusakura/code/github.com/rukasakurai/agent-skills/skills/microsoft-product-updates &&
  │ python3 scripts/fetch_azure.py --since 2026-06-21 --until 2026-07-21 > /tmp/az_all.json
  │ 2>/tmp/az_err.txt; echo "exit=$?"; wc -c /tmp/az_all.json; head -c 300 /tmp/az_err.txt
  └ 3 lines…

● Count items (shell)
  │ cd /tmp && echo "GH count: $(python3 -c 'import
  │ json;print(len(json.load(open("/tmp/gh_all.json"))))')"; echo "AZ count: $(python3 -c 'import
  │ json;print(len(json.load(open("/tmp/az_all.json"))))')"
  └ 3 lines…

Let me filter for items relevant to the repo's claims (Foundry/AI/ML on Azure; CLI/skills/copilot on GitHub).

● Filter Azure items for Foundry/AI relevance (shell)
  │ cd /tmp && python3 - <<'PY'
  │ import json
  │ az=json.load(open("az_all.json"))
  │ kw=["foundry","ai ","machine learning","cognitive","agent","openai","ml ","model"]
  │ print("=== AZURE relevant ===")…
  └ 71 lines…

● Filter GitHub items relevant to CLI/skills/copilot (shell)
  │ cd /tmp && python3 - <<'PY'
  │ import json
  │ gh=json.load(open("gh_all.json"))
  │ kw=["skill","cli","copilot","agent"]
  │ print("=== GITHUB relevant ===")…
  └ 67 lines…

Let me inspect the Agent Framework Azure update to assess the SDK-naming claim in the foundry skill.

● Fetch Agent Framework Azure update detail (shell)
  │ cd /tmp && curl -s 'https://www.microsoft.com/releasecommunications/api/v2/azure?$top=1&$skip=
  │ 0&$filter=id%20eq%20564312' | python3 -c 'import sys,json,re; d=json.load(sys.stdin);
  │ v=d.get("value",[]);
  │ for it in v:
  │ print("TITLE:",it.get("title")); print("STATUS:",it.get("status")); …
  └ 6 lines…

● Fetch descriptions for key Foundry/Agent updates (shell)
  │ cd /tmp && for id in 564312 563481; do echo "=== id=$id ==="; curl -s "https://www.microsoft.c
  │ om/releasecommunications/api/v2/azure?\$top=100&\$skip=0&\$orderby=modified+desc" > /dev/null
  │ 2>&1; done
  │ # Instead fetch the public update page bodies from az_all raw. Re-fetch raw azure with
  │ descriptions:…
  └ 38 lines…

I have enough to report. Here's my read-only staleness assessment.

## Repo staleness review (Microsoft updates 2026-06-21 → 2026-07-21)

I used the skill's two scripts (`fetch_azure.py`, `fetch_github.py`) over the window: **43 Azure** items and **95 GitHub** changelog entries. The repo's only substantive version/lifecycle claims live in `skills/microsoft-foundry-resources/SKILL.md` and `README.md`; the other skills state method/rules with no pinned versions.

### Potentially stale items

**1. "Microsoft Agent SDK (.NET)" label — `skills/microsoft-foundry-resources/SKILL.md` (line 49)**
The table lists *"Microsoft Agent SDK (.NET) | NuGet: `Microsoft.Agents.AI.*`"*. In-window Azure updates rebrand/consolidate this as **"Microsoft Agent Framework"**, a *unified multi-agent orchestration SDK for **C# and Python*** (consolidating AutoGen + Semantic Kernel), with GA connectors.
- Cite: id **564312** (`azure.microsoft.com/updates?id=564312`), id **563701** (GA GitHub Copilot/Claude Code connectors).
- Impact: label is now ".NET-only SDK" vs. current cross-language "Agent Framework" branding; the `Microsoft.Agents.AI.*` package prefix still appears valid.
- **Confidence: Medium** (naming/scope drift, not a hard error).

**2. "Foundry / Foundry (classic)" brand + hub-migration claims — same file (lines 17, 22, 65)**
Checked against the feed: the **"Microsoft Foundry"** brand is actively current (e.g. GA "Toolboxes in Microsoft Foundry", id **563481**), and "Azure AI Foundry" still appears as a product tag (id **567594**), consistent with an ongoing rename. The "Since June 2025 hub capabilities moving to Foundry resource" line is a dated historical statement, not contradicted.
- **Confidence: High that these are NOT stale** (no action needed).

**3. `gh skill install/update` + "GitHub CLI v2.90.0+" — `README.md` (lines 17–18)**
No GitHub changelog entry in the window covers `gh skill` or a CLI version bump (GitHub CLI point releases aren't published to this changelog feed), so I could not corroborate or refute the `v2.90.0+` floor from the permitted feeds. Note there is unrelated "skill" news — *New C++ language server config skill for Copilot CLI* (2026-07-01) — which is a **Copilot CLI** feature, not `gh skill`; don't conflate.
- **Confidence: Low** (uncorroborated by the two feeds; verify against GitHub CLI release notes out of band).

### Not applicable
Azure retirements in-window (Python 2.7/3.8 & PowerShell 7.1/7.2 by 2026-09-30; Blueprints; AV36 nodes) and GA items (Functions Python 3.14, GPT-5.6, Claude Sonnet 5) touch products the repo does not pin, so no repo change is implied.

**Bottom line:** one medium-confidence naming refresh (Agent SDK → Agent Framework), one low-confidence item to verify externally (`gh skill` / CLI version). No files modified.

## Sources used
- Azure: `https://www.microsoft.com/releasecommunications/api/v2/azure?$count=true&$top=100&$skip=N&$orderby=modified desc` (via `fetch_azure.py --since 2026-06-21 --until 2026-07-21`).
- GitHub: `https://github.blog/wp-json/wp/v2/changelogs?per_page=100&after=2026-06-21T00:00:00&before=2026-07-21T23:59:59&orderby=date&order=desc` (via `fetch_github.py`).
- **Oldest GitHub changelog entry considered: 2026-06-22** (2026-06-22T15:34Z; window opened at 2026-06-21, no entries dated 06-21).

