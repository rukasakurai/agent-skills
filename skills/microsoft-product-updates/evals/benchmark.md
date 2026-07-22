# Cost / latency / quality benchmark

How this skill compares to **not** using it, to help decide when to invoke it
(e.g. when rushing, low on AI credits, or when quality matters most).

Method: run each eval prompt twice in fresh isolated sessions — once with this
skill, once without — same model in both arms, and compare. See
`evals.json` and https://agentskills.io/skill-creation/evaluating-skills.
AI Credits are the Copilot CLI's per-run figure (== `total_nano_aiu / 1e9`).

## Results — as of 2026-07-22, model `claude-opus-4.8`

| eval | quality (with / without) | AI credits (with / without) | latency s (with / without) |
| --- | --- | --- | --- |
| repo-staleness-review | 4/4 / 4/4 (tie) | 82.6 / 84.0 (−1.7%) | 199 / 224 |
| azure-preview-updates | 5/5 / 5/5 (tie) | 23.5 / 30.6 (−23%) | 62 / 89 |
| **aggregate** | **tie** | **106.1 / 114.5 (−7.4%)** | **261 / 313** |

## How to read this

- **Quality:** a tie on a capable model — it reaches the same authoritative
  feeds and findings with or without the skill. The skill's value is
  reliability + speed, not unlocking a capability.
- **AI credits:** the skill was **not** more expensive despite adding context —
  equal-to-cheaper. Its deterministic scripts replace the exploratory tool
  calls the baseline makes, offsetting the tokens spent reading the skill.
- **Latency:** faster with the skill in both evals.

**Decision cue:** for this skill there is no cost/latency tradeoff to weigh — it
ties on quality while being no more expensive and faster. If a future run shows
that changing (slower model, larger repo, more evals), re-run and update the
date/model above.

## Caveats

- n=2 evals, single run each, one model — directional, not statistically robust.
- Numbers are point-in-time: they depend on the model and on the live feeds'
  contents on the date above. Treat as a snapshot, not a guarantee.
- The "without" arm was only instructed not to use the skill (the skill is not
  auto-loaded), matching how a user without it would work.
