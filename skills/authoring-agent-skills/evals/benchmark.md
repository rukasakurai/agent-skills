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
runs each arm from a clean temp dir (so a run can't read this repo's own files
and leak the answer) and writes transcripts to the gitignored workspace. See
`evals.json` and https://agentskills.io/skill-creation/evaluating-skills.

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

| arm, `claude-haiku-4.5` | names `benchmark.md` | dated/model-stamped | gitignored workspace | unofficial disclaimer |
| --- | --- | --- | --- | --- |
| baseline (no skill) | no (invents a `.json` name) | partial (date, no model) | no | no |
| with skill | yes | yes | yes | yes |

Run in isolated temp dirs, so the baseline cannot recover the convention by
reading this repo's existing files; here the skill unlocks the correct
convention rather than just doing it faster.

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
- Each arm runs in an isolated temp dir; personal/builtin skills (if any) are
  still available to both arms equally, but this repo's `skills/` is not an
  autodiscovery path so the tested skill is delivered only via the prompt.
- Point-in-time: depends on the models and CLI on the date above. Re-run
  (`scripts/ab_eval.sh`) and update the date/models if you need current behavior.
