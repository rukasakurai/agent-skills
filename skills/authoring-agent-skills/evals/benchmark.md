# authoring-agent-skills — eval results

Unofficial personal measurements; not authoritative benchmarks. Raw runs live in the
gitignored `skills/authoring-agent-skills-workspace/`.

## Iteration 1 — 2026-07-22 (eval `evaluate-means-measure`)

Question: does an agent given this skill, when asked to "evaluate a proposed skill",
actually *run* a with/without measurement, or just hypothesize from inspection?

| Arm | Runs the comparison | Grounds verdict in observed evidence | Correct ship/cut call |
|---|---|---|---|
| Baseline (no skill), haiku-4.5 | no | no | wrong ("ship it") |
| Skill v1–v2 (descriptive), haiku-4.5 | no | no | right ("cut"), from reasoning |
| Skill v3 (imperative + run recipe), haiku-4.5 | no (surfaces the command) | no | right |
| Skill v3, sonnet-4.6 | **yes** (ran baseline + with-skill sessions) | **yes** (quoted outputs) | right; also caught a regression |

Takeaways:
- Descriptive "you should evaluate" prose does not trigger the behavior; an imperative
  "run it now" step plus a concrete environment recipe does.
- Autonomous execution also depends on model capability: a capable driving model ran the
  comparison; a weak one only surfaced the command for a human to run. Drive skill
  evaluation with a capable model.
- Running beats hypothesizing: the sonnet arm discovered the drafted skill caused a
  regression (dropped a conventional-commit prefix) that inspection alone missed.
