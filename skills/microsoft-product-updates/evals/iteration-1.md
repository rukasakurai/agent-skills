# Eval results — iteration 1

Method: eval #1 (`evals.json`) run twice in fresh, isolated contexts — once
with the skill available, once without (baseline not told the skill exists).
Target repo: this repo (`rukasakurai/agent-skills`), which itself makes the
kind of stale-prone GA/preview claims the skill addresses. Date: 2026-07-22 JST.

## Outcome

| | Without skill (baseline) | With skill |
| --- | --- | --- |
| Final finding | Same single medium-confidence item (`Microsoft.Agents.AI.*` / "Agent Framework" SDK wording in `microsoft-foundry-resources`) | Same item |
| Azure authoritative feed | **Failed** — "Azure Updates RSS redirected to an HTML page"; fell back to Microsoft Learn docs | **Reached** the release communications JSON API; cited a specific update (`id=564312`) |
| High-confidence stale pins | none | none |
| Duration | 219s | 331s |

## Interpretation

- On this repo the skill did **not** change the conclusion — the repo has few
  concrete version pins, so both runs converged on the same soft finding.
- The skill's measurable advantage was on the **Azure path**: the baseline
  could not reach the structured feed at all, while the skill run did and cited
  a specific structured update. That is the skill's core promise.
- The GitHub path was **weaker than the baseline assumed possible**: the run
  surfaced two real defects (dead `/YYYY/feed/` URL; feed returns only ~10
  items so a month window silently covered ~6 days). Both were fixed after this
  iteration (pagination via `?paged=N`, `--label` feed).

## Takeaway

Value is currently in **method and citation quality**, not in changing the
answer for a low-pin repo. Re-run against a repo with concrete pinned ARM/SDK
versions to test whether the skill flips a wrong baseline conclusion.
