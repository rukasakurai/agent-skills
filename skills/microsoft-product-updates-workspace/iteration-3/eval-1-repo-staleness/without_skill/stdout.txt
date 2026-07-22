I'll start by exploring the repo to find version pins and GA/preview/retirement claims.

● List directory .
  └ 4 files found

● Repo overview (shell)
  │ cd /home/rusakura/code/github.com/rukasakurai/agent-skills && git log --oneline -5 && echo "---"
  │ && ls -la
  └ 14 lines…

● Read README.md
  └ 56 lines read

● List skill files (shell)
  │ cd /home/rusakura/code/github.com/rukasakurai/agent-skills && find skills -type f | head -100
  └ 30 lines…

This is a skills repo. The version pins/GA/preview claims likely live in `microsoft-foundry-resources` and `latest-stable-version`. Let me read those as review subjects.

● Read SKILL.md
  │ skills/microsoft-foundry-resources/SKILL.md
  └ 82 lines read

● Read SKILL.md
  │ skills/latest-stable-version/SKILL.md
  └ 43 lines read

Now I understand the review targets. Key stale-able claims:
- **microsoft-foundry-resources**: Foundry rename/"classic" branding, "Since June 2025 hub capabilities moving to Foundry resource", ARM types/kinds, `Microsoft.Agents.AI.*` NuGet SDK.
- **latest-stable-version / README**: GitHub CLI v2.90.0+ / `gh skill` command.

Let me independently fetch the authoritative Azure and GitHub update feeds for 2026-06-21→2026-07-21.

● Probe Azure + GitHub feeds (shell)
  │ cd /tmp && echo "=== Azure Updates API ===" && curl -s --max-time 30
  │ "https://www.microsoft.com/releasecommunications/api/v2/azure?$top=5" | head -c 800; echo; echo
  │ "=== GitHub changelog feed ===" && curl -s --max-time 30 "https://github.blog/changelog/feed/" |
  │ head -c 800
  └ 33 lines…

GitHub feed works; Azure API blocked. Let me get the full GitHub changelog and try Azure feeds with a proper UA.

● Try Azure feeds with UA, save GH feed (shell)
  │ cd /tmp && UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)
  │ Chrome/120 Safari/537.36"
  │ echo "=== releasecommunications API w/ UA ==="; curl -s --max-time 30 -A "$UA"
  │ "https://www.microsoft.com/releasecommunications/api/v2/azure" | head -c 400; echo
  │ echo "=== azure updates RSS ==="; curl -s --max-time 30 -A "$UA" …
  └ 10 lines…

Azure release-communications API works with a UA. Let me query it for Foundry-related items and the date window, and parse the GitHub changelog for `gh skill`/CLI entries.

● Pull Azure updates pages, inspect (shell)
  │ cd /tmp && UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
  │ # Pull several pages of Azure updates
  │ > azure_all.json
  │ for skip in 0 100 200 300 400; do
  │ curl -s --max-time 40 -A "$UA" …
  └ 23 lines…

● Analyze Azure items for window+keywords (shell)
  │ cd /tmp && python3 - <<'PY'
  │ import json
  │ items=[]
  │ for line in open('/tmp/azure_all.json'):
  │ line=line.strip()…
  └ 27 lines…

● Azure updates ordered by modified desc (shell)
  │ cd /tmp && UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
  │ curl -s --max-time 40 -A "$UA" "https://relcomms-prod-dagnegedescbeefs.b02.azurefd.net/api/v2/
  │ azure/?\$orderby=modified%20desc&\$top=20" > az_recent.json
  │ python3 - <<'PY'
  │ import json…
  └ 25 lines…

Now the feed shows 2026-07 items. Let me pull the full window ordered by modified desc and extract Foundry/Agent/ML/retirement items.

● Filter window items for skill-relevant topics (shell)
  │ cd /tmp && UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
  │ > az_win.json
  │ for skip in 0 100 200 300; do
  │ curl -s --max-time 40 -A "$UA" "https://relcomms-prod-dagnegedescbeefs.b02.azurefd.net/api/v
  │ 2/azure/?\$orderby=modified%20desc&\$skip=$skip" >> az_win.json…
  └ 43 lines…

Several Foundry/Agent-Framework items land in the window. Let me read the full descriptions of the most relevant ones for the foundry-resources skill.

● Full descriptions of key Foundry/Agent items (shell)
  │ cd /tmp && python3 - <<'PY'
  │ import json
  │ items=[]
  │ for line in open('/tmp/az_win.json'):
  │ line=line.strip()…
  └ 41 lines…

Now let me parse the GitHub changelog for the window (`gh skill`/CLI/Agent Skills) and verify the `Microsoft.Agents.AI` NuGet SDK status.

● Parse GitHub changelog window + relevant titles (shell)
  │ cd /tmp && python3 - <<'PY'
  │ import re,html
  │ xml=open('gh_changelog.xml',encoding='utf-8').read()
  │ items=re.findall(r'<item>(.*?)</item>',xml,re.S)
  │ print("items in feed:",len(items))…
  └ 27 lines…

The feed only returns 10 items (back to 2026-07-16). I need to paginate to cover the full window back to 2026-06-21.

● Paginate GitHub changelog to cover full window (shell)
  │ cd /tmp && for p in 1 2 3 4 5 6; do
  │ curl -s --max-time 30 "https://github.blog/changelog/feed/?paged=$p" -o gh_$p.xml
  │ n=$(grep -c "<item>" gh_$p.xml)
  │ echo "page $p items=$n"
  │ done…
  └ 90 lines…

Let me extend pagination back to 2026-06-21 to fully cover the window.

● Extend changelog to 2026-06-21 (shell)
  │ cd /tmp && for p in 7 8 9 10; do
  │ curl -s --max-time 30 "https://github.blog/changelog/feed/?paged=$p" -o gh_$p.xml
  │ echo "page $p items=$(grep -c '<item>' gh_$p.xml)"
  │ done
  │ cat gh_2.xml gh_3.xml gh_4.xml gh_5.xml gh_6.xml gh_7.xml gh_8.xml gh_9.xml gh_10.xml > …
  └ 59 lines…

Full window covered (oldest considered 2026-06-18). No `gh skill`/gh-CLI-version entry contradicts the README. Let me verify the `Microsoft.Agents.AI` NuGet SDK status to gauge the foundry-resources SDK claim.

● Check Microsoft.Agents.AI NuGet versions (shell)
  │ cd /tmp && curl -s --max-time 30
  │ "https://api.nuget.org/v3-flatcontainer/microsoft.agents.ai/index.json" | python3 -c "import
  │ sys,json; v=json.load(sys.stdin)['versions']; stable=[x for x in v if '-' not in x]; print('all
  │ count',len(v)); print('latest 5:',v[-5:]); print('latest stable:', stable[-1] if stable else
  │ 'NONE (preview only)')" 2>/dev/null || echo "package not found under that id"
  └ 4 lines…

Analysis complete. Cleaning up temp files, then reporting.

● Remove temp files (shell)
  │ cd /tmp && rm -f azure_all.json az_recent.json az_win.json gh_*.xml gh_changelog.xml
  │ 2>/dev/null; echo cleaned
  └ 2 lines…

# Repo staleness review (window 2026-06-21 → 2026-07-21)

Reviewed the version-pinning / lifecycle-claiming files: `skills/microsoft-foundry-resources/SKILL.md`, `skills/latest-stable-version/SKILL.md`, `README.md`. (Did not consult the `microsoft-product-updates` skill; found feeds independently.)

## Potentially stale items

1. **`microsoft-foundry-resources` — "Client SDK" table calls it "Microsoft Agent SDK (.NET) / `Microsoft.Agents.AI.*`".** — **Confidence: Medium.**
   Azure now brands this as the **Microsoft (Foundry) Agent Framework**, a unified multi-agent orchestration SDK for **C# *and* Python** consolidating AutoGen + Semantic Kernel — so the "Microsoft Agent SDK" name and ".NET"-only scope are outdated. Companion GA connectors also shipped.
   - Azure Update id **564312** — "Multi-agent orchestration SDK with the Microsoft Foundry Agent Framework in C# and Python" (2026-07-15) — https://azure.microsoft.com/updates?id=564312
   - Azure Update id **563701** — "GitHub Copilot and Claude Code connectors in Microsoft Agent Framework" (GA, 2026-07-15) — https://azure.microsoft.com/updates?id=563701
   - Note: the NuGet package id `Microsoft.Agents.AI` itself is still valid and is now GA (latest stable **1.14.0**), so only the *label/scope* is stale, not the package name.

2. **`microsoft-foundry-resources` — branding section (only "Microsoft Foundry" vs "Foundry (classic)").** — **Confidence: Low.**
   A new **"Microsoft Foundry NextGen" portal** brand now appears in official updates, a naming layer the skill doesn't mention. Worth watching; not yet clearly contradicting the classic/modern framing.
   - Azure Update id **563331** — "Document PII playground sample in Microsoft Foundry NextGen" (2026-07-01) — https://azure.microsoft.com/updates?id=563331

## Checked and NOT stale
- **ARM providers/types/kinds** (`Microsoft.CognitiveServices/accounts[/projects/applications/agentDeployments]`, `Microsoft.MachineLearningServices/workspaces` + kinds): no rename/retirement in window. The skill pins **no** API version, so nothing to bump. (New feature "Toolboxes in Microsoft Foundry" GA, id 563481, doesn't affect the resource model.)
- **`Azure AI Foundry` still coexists** as a product tag (id 567594), consistent with the skill's classic/modern distinction.
- **README "requires GitHub CLI v2.90.0+" (`gh skill`)** and **`latest-stable-version` commands**: no GitHub Changelog entry in the window changes `gh skill` or the stated version floor. (Confidence: High that these are current.)

## Sources used
- **Azure updates** (release-communications API): `https://www.microsoft.com/releasecommunications/api/v2/azure` → data endpoint `https://relcomms-prod-dagnegedescbeefs.b02.azurefd.net/api/v2/azure/?$orderby=modified desc&$skip=N` (browser UA required)
- **GitHub Changelog** RSS: `https://github.blog/changelog/feed/?paged=1..10`
- **NuGet**: `https://api.nuget.org/v3-flatcontainer/microsoft.agents.ai/index.json`
- **Oldest GitHub changelog entry considered: 2026-06-18** (window fully covered back to 2026-06-21).

