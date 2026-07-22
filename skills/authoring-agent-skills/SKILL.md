---
name: authoring-agent-skills
description: 'Create, update, or retire an agentskills.io Agent Skill (a SKILL.md plus optional references/, scripts/, assets/) so its description reliably triggers the model and its body stays lean. Use when writing or reviewing a SKILL.md, wording a skill description, deciding what belongs in a skill, or planning a skill lifecycle (sharing, installing, updating, retiring).'
argument-hint: Describe the skill you are creating, updating, or retiring
---

# Authoring Agent Skills

## What an Agent Skill Actually Is

- A skill is a **folder**, not just `SKILL.md`. It can also carry `references/` (Markdown loaded on demand), `scripts/` (deterministic code the model can run), and `assets/` (templates, files). Put detail there instead of bloating `SKILL.md`.
- Loading is **progressive**: the `description` is always in context; the body loads when the skill triggers; `references/`, `scripts/`, and `assets/` load only when needed. Design for this.
- A skill **shapes the model's behavior** — it is not just a place to store instructions. Judge it by how it changes responses, not by how much it documents.

## Common Mistakes to Avoid

- Writing the `description` without understanding that it is what makes the model load (or ignore) the skill.
- Treating `SKILL.md` as the whole skill and ignoring `references/`, `scripts/`, and `assets/`.
- Treating a skill as documentation rather than a lever on model behavior.
- Adding content by default. Deleting or editing is often the higher-value move; verbosity costs context and tokens.
- Stating what the model already knows (general programming, common-sense advice). Keep only what it would otherwise get wrong.
- Shipping a skill without checking it actually beats the no-skill baseline — a quick with/without run often exposes instructions that change nothing, or a task the model already handles unaided.
- Shipping a skill without thinking about how it will be shared and maintained.

## Writing the Description (the highest-leverage part)

Write it in the third person and make it answer two things: **what the skill does** and **when to use it**, using words a prompt would actually contain so the model can match. Keep everything else out.

## When to Read the Official Docs

These are authoritative; read the relevant one before committing rather than reproducing it here. (Docs describe intended behavior — sanity-check against how skills actually load in your agent.)

- [Best practices](https://agentskills.io/skill-creation/best-practices) — before creating a new skill or restructuring one.
- [Optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) — when a skill triggers too rarely, too often, or on the wrong prompts.
- [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills) — when you cannot tell whether a skill is actually improving responses.
- [Using scripts in skills](https://agentskills.io/skill-creation/using-scripts) — before adding `scripts/`, or when an operation must be deterministic rather than model-generated.

## Verifying a Skill Earns Its Keep

- **Check it against the no-skill baseline.** Run 2–3 realistic prompts with and without the skill, in fresh contexts, and compare. This is the cheapest way to catch a skill that reads well but changes nothing — or is silently broken. Escalate to the full `evals/` harness (see "Evaluating skill output quality" above) only when a manual A/B can't answer the question.
- **Weigh cost, not just quality.** A skill spends context tokens (and any bundled-script tool calls) on every use. When quality ties, latency and token/credit cost decide whether it earns its place — and the honest result is sometimes to cut it. Note that clean per-run credit attribution isn't well supported today, so this is often a rough comparison.
- **Keep eval artifacts out of the shipped folder.** `gh skill install` copies the *whole* skill directory to consumers, so commit only small, durable files (e.g. `evals/evals.json`, a short dated results summary), and keep bulky run outputs in a gitignored workspace *beside* the skill, not inside it.

## Lifecycle

- **Share/install** via [`gh skill install`](https://cli.github.com/manual/gh_skill_install) (e.g. `gh skill install OWNER/REPO <skill> --scope user`).
- **Update** installed skills with `gh skill update`; keep the source repo the single source of truth.
- **Retire** skills that no longer earn their context: delete them, and prefer editing or merging over accumulating near-duplicates.
