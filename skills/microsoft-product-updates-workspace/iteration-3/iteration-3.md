# iteration-3 analysis — microsoft-product-updates

Methodology: https://agentskills.io/skill-creation/evaluating-skills,
**extended with two dimensions the guidance omits: cost (AI credits) and latency.**
Ran 2026-07-22.

## What changed since iteration-2
1. **Fixed a factual error in the skill.** iteration-2's baseline found GitHub's
   WordPress REST API (`github.blog/wp-json/wp/v2/changelogs`) — structured JSON,
   100/page, server-side date+label filtering — which the skill wrongly said didn't
   exist ("No structured API"). `fetch_github.py` and SKILL.md now use it. Verified
   live: 106 items across the month in one pass; label filter works.
2. **Tightened evals:** removed RSS-specific assertion wording; added an eval-2
   recall-floor assertion (iteration-2 had an undercount the assertions missed).
3. **Made cost measurable.** Each arm ran as its own isolated headless session
   (`copilot -p --session-id <uuid> --model claude-opus-4.8`), so AI credits, tokens,
   and wall time attribute to one arm. **AI Credits == total_nano_aiu / 1e9** (verified
   against the CLI's printed "AI Credits" line). Same model on both arms -> credits
   directly comparable.

## Results

| eval | quality (with/without) | AI credits (with/without) | wall s (with/without) |
|------|------------------------|---------------------------|-----------------------|
| repo-staleness | 4/4 vs 4/4 | 82.55 vs 83.96 (-1.7%) | 199 vs 224 |
| azure-preview  | 5/5 vs 5/5 | 23.53 vs 30.57 (-23%)  | 62 vs 89 |
| **aggregate**  | **9 vs 9 (tie)** | **106.1 vs 114.5 (-7.4%)** | **261 vs 313** |

## Interpretation

- **Quality: still a tie.** A capable model (opus-4.8) reaches the same authoritative
  feeds and reaches the same core findings with or without the skill. Both arms found
  the Agent-SDK->Agent-Framework staleness item; both stayed read-only; both listed 10
  confirmed preview items in eval-2. The skill does NOT unlock capability here.
- **Cost: the skill is NOT more expensive, and is cheaper on the narrower task.**
  This is the notable result. A common worry is "a skill adds context tokens on every
  call, so it costs more." Here the opposite held: with-skill spent fewer or equal
  credits (-1.7% and -23%). Why: the skill's deterministic scripts replace exploratory
  tool calls the baseline had to make (the baseline scraped RSS, probed NuGet, tried
  multiple endpoints), and produced fewer output tokens. Input tokens were higher for
  with-skill on eval-1 (767k vs 622k, from reading SKILL.md + scripts) but output
  tokens were much lower, and credits netted out even.
- **Latency: with-skill faster on both** (261s vs 313s aggregate).

## Honest caveats
- n=2 evals, single model, single run each — directional, not statistically robust.
- Both arms shared the same repo working tree; the "without" arm was only *instructed*
  not to use the skill (it isn't installed/auto-loaded), matching how a naive user
  would work without it.
- AI Credits here is the CLI's user-facing figure; the per-premium-request billing
  mapping wasn't independently reconciled, but same-model arms are comparable to each
  other regardless.

## Conclusion / decision input
The iteration-2 worry — "the skill doesn't beat baseline, so does it earn its context
cost?" — is answered more favorably once cost is actually measured: the skill matches
baseline quality **without** costing extra credits, and is faster. Its value is
**reliability + speed + not paying a token premium**, not capability unlock. The
factual GitHub-API error that made iteration-2 look bad is now fixed. Reasonable to
keep the skill; still worth deciding whether 2 evals justify the maintained harness.

## Follow-ups (out of scope for PR #11)
- The recurring `microsoft-foundry-resources` Agent-SDK->Agent-Framework staleness
  (id 564312) is a real repo finding — handle separately.
