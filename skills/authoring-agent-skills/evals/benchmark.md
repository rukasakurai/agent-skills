# Behavioral benchmark

> **Unofficial, personal measurement.** These are ad-hoc results from one
> contributor's local Copilot CLI runs, not official GitHub Copilot benchmarks
> or performance figures, and not representative of Copilot generally. They are
> a small, dated snapshot (see date/models below) and will drift as models and
> the CLI change.

Whether this skill actually changes behavior — for a meta/authoring skill the
payoff is behavioral (does the agent *run* an evaluation), not a cost/latency
number — so this tracks pass/fail across skill versions and models rather than
credits.

Method: run the eval prompt in fresh isolated sessions with the skill body in
context, compare against a no-skill baseline, and check each assertion against
the observed transcript. See `evals.json` and
https://agentskills.io/skill-creation/evaluating-skills. Raw runs are local
scratch in the gitignored `skills/authoring-agent-skills-workspace/`.

## Results — as of 2026-07-22 (eval `evaluate-means-measure`)

Question: given this skill and asked to "evaluate a proposed skill", does the
agent *run* a with/without measurement, or just hypothesize from inspection?

| arm (skill version, model) | runs the comparison | evidence-grounded | correct ship/cut call |
| --- | --- | --- | --- |
| baseline (no skill), `claude-haiku-4.5` | no | no | wrong ("ship it") |
| v1-v2 descriptive, `claude-haiku-4.5` | no | no | right, from reasoning |
| v3 imperative + recipe, `claude-haiku-4.5` | no (surfaces the command) | no | right |
| v3 imperative + recipe, `claude-sonnet-4.6` | **yes** (ran both sessions) | **yes** (quoted outputs) | right; caught a regression |

## How to read this

- **Prose framing decides triggering:** descriptive "you should evaluate" prose
  never triggered a measurement; an imperative "run it now" step plus a concrete
  environment recipe did.
- **Model capability decides execution:** a capable model ran the comparison
  autonomously; a weak one only surfaced the command for a human to run.
- **Running beats hypothesizing:** the capable arm found the drafted skill caused
  a regression (dropped a conventional-commit prefix) that inspection missed.

**Decision cue:** drive skill authoring/evaluation with a capable model; on a
weak model, expect to run the surfaced command yourself.

## Caveats

- One eval, single run per arm - directional, not statistically robust.
- Point-in-time: depends on the models and CLI on the date above. Re-run and
  update the date/models if you need current behavior.
