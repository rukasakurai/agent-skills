# Cost / latency / quality benchmark

> **Unofficial, personal measurement.** These are ad-hoc numbers from one
> contributor's local Copilot CLI runs, not official GitHub Copilot benchmarks,
> pricing, or performance figures, and not representative of Copilot generally.
> They are a small, dated snapshot (see date/model below) and will drift as
> models, feeds, and the CLI change.

How this skill compares to **not** using it, to help decide when to invoke it
(e.g. when rushing, low on AI credits, or when quality matters most).

Method: run each eval prompt twice in fresh isolated sessions — once with this
skill, once without — same model in both arms, and compare. See
`evals.json` and https://agentskills.io/skill-creation/evaluating-skills.
"AI Credits" here is the relative per-run usage figure the Copilot CLI printed
for these runs — a local convenience number for comparison only, not an official
cost or pricing metric.

## Results — as of 2026-07-22, model `claude-opus-4.8`

| eval | quality (with / without) | AI credits (with / without) | latency s (with / without) |
| --- | --- | --- | --- |
| repo-staleness-review | 4/4 / 4/4 (tie) | 82.6 / 84.0 (−1.7%) | 199 / 224 |
| azure-preview-updates | 5/5 / 5/5 (tie) | 23.5 / 30.6 (−23%) | 62 / 89 |
| **aggregate** | **tie** | **106.1 / 114.5 (−7.4%)** | **261 / 313** |

## How to read this

- **Quality:** a tie in this snapshot on a capable model — it reached the same
  authoritative feeds and findings with or without the skill. Here the skill's
  value looked like reliability + speed, not unlocking a capability.
- **AI credits:** in these runs the skill was not more expensive despite adding
  context (roughly equal-to-lower), plausibly because its deterministic scripts
  replace exploratory tool calls the baseline makes, offsetting the tokens spent
  reading the skill.
- **Latency:** faster with the skill in both evals in this snapshot.

**Decision cue:** in this small snapshot there was no cost/latency penalty for
using the skill — it tied on quality while being similar-or-cheaper and faster.
This is n=2, single-run, one model, so treat it as directional, not a
guarantee; a slower model, larger repo, or more evals could change it. Re-run
and update the date/model above if you need current numbers.

## Caveats

- n=2 evals, single run each, one model — directional, not statistically robust.
- Numbers are point-in-time: they depend on the model and on the live feeds'
  contents on the date above. Treat as a snapshot, not a guarantee.
- The "without" arm was only instructed not to use the skill (the skill is not
  auto-loaded), matching how a user without it would work.
