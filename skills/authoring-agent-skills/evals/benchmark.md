# Behavioral benchmark

> **Unofficial, personal measurement.** These are ad-hoc results from one
> contributor's local Copilot CLI runs, not official GitHub Copilot benchmarks
> or performance figures, and not representative of Copilot generally. They are
> a small, dated snapshot (see date/models below) and will drift as models and
> the CLI change.

Whether this skill actually changes behavior — for a meta/authoring skill the
payoff is behavioral (does the agent *run* an evaluation), not a cost/latency
number — so this tracks pass/fail versus a no-skill baseline rather than credits.

Method: run the eval prompt in fresh isolated sessions with the skill body in
context, compare against a no-skill baseline, and check each assertion against
the observed transcript. `scripts/ab_eval.sh <skill-dir> <eval-id> [model]`
spawns both arms into the gitignored workspace. See `evals.json` and
https://agentskills.io/skill-creation/evaluating-skills. Raw runs are local
scratch in the gitignored `skills/authoring-agent-skills-workspace/`.

## Results — as of 2026-07-22

### Eval `evaluate-means-measure` (does "evaluate" trigger a measurement?)

Given this skill and asked to "evaluate a proposed skill", does the agent *run*
a with/without measurement, or just hypothesize from inspection?

| arm, `claude-sonnet-4.6` | runs the comparison | evidence-grounded | correct ship/cut call |
| --- | --- | --- | --- |
| baseline (no skill) | no | no | wrong ("ship it") |
| with skill | **yes** (ran both sessions) | **yes** (quoted outputs) | right; caught a regression baseline missed |

On a weaker model (`claude-haiku-4.5`) the with-skill arm surfaces the exact
command but does not run it, so drive skill evaluation with a capable model.

### Eval `eval-artifact-naming-and-placement` (does the skill teach the convention?)

Asked where to save eval results, does the agent name `evals/benchmark.md`
(dated, disclaimed) + a gitignored workspace?

| arm, `claude-haiku-4.5` | names `benchmark.md` | dated/model-stamped | gitignored workspace | unofficial disclaimer | credits |
| --- | --- | --- | --- | --- | --- |
| baseline (no skill) | yes* | yes | yes | yes | 3.36 |
| with skill | yes | yes | yes | yes | 1.28 |

\*Inside this repo the baseline reached the convention only by reading the
existing `benchmark.md` files (it ran `find`), so this eval is partly leaked to
the baseline here; a clean baseline would run outside the repo. The skill's
value on this eval is efficiency — it states the convention directly, ~2.6×
cheaper, without filesystem spelunking — not unlocking a new capability.

## How to read this

- **Model capability decides execution:** a capable model ran the comparison
  autonomously; a weak one only surfaced the command for a human to run.
- **Running beats hypothesizing:** with the skill, the capable arm found the
  drafted test skill caused a regression (dropped a conventional-commit prefix)
  that inspection alone missed.

**Decision cue:** drive skill authoring/evaluation with a capable model; on a
weak model, expect to run the surfaced command yourself.

## Caveats

- Two evals, single run per arm — directional, not statistically robust.
- The naming/placement eval is partly leaked to the baseline when run inside
  this repo (the convention is discoverable in existing files); treat its
  baseline column as a lower bound on the skill's edge.
- Point-in-time: depends on the models and CLI on the date above. Re-run
  (`scripts/ab_eval.sh`) and update the date/models if you need current behavior.
