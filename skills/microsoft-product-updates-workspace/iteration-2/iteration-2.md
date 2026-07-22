# iteration-2 analysis — microsoft-product-updates

Methodology: https://agentskills.io/skill-creation/evaluating-skills
A/B, fresh agent contexts, 2 committed evals, assertion-graded. Ran 2026-07-21.

## Result

| eval | with-skill | baseline | delta | with-skill duration | baseline duration |
|------|-----------|----------|-------|--------------------|-------------------|
| repo-staleness-review | 4/4 | 4/4 | 0 | 310s | 429s |
| azure-preview-updates | 4/4 | 4/4 | 0 | 104s | 299s |

**The skill did NOT beat baseline on assertions (8/8 vs 8/8).** With-skill was faster
in both evals, but a capable model reached the same authoritative feeds unaided.

## What the baseline discovered that the skill got wrong

1. **GitHub has a structured JSON API; the skill claims it doesn't.**
   Baseline used `https://github.blog/wp-json/wp/v2/changelogs?per_page=100&page=1`
   (WordPress REST). One request covered the whole month (2026-06-18 → 07-21) with
   `date`, `modified`, `status`, `title`, `content`, `link`. Cleaner than the skill's
   RSS `?paged=N` walking. SKILL.md's "No structured API" statement is false.

2. **eval-2 undercount.** With-skill found 13 preview items; baseline found 18,
   including 5 Microsoft Agent Framework items the with-skill run missed. The extra
   items were within window — a recall miss, not a stage-labeling difference.
   (Assertions still passed because they check quality of what's listed, not recall —
   a gap in the assertions themselves.)

## What the skill did right

- **GitHub pagination/404 fix is verified through the loop:** both with-skill runs
  paged RSS back to 2026-06-18; the dead `/changelog/YYYY/feed/` URL was already removed.
- **Lifecycle-signal ambiguity handling** appeared in both configs, but the skill
  documents it explicitly — plausibly why with-skill was ~3x faster on eval-2.

## Interpretation

For a capable model, this skill's main value is **speed / first-try reliability**, not
capability unlock — it did not change pass/fail. That is a weaker justification than
iteration-1 suggested (where baseline failed to reach the Azure feed at all). The
difference: iteration-1 baseline gave up on the feed; iteration-2 baseline persisted.

## Decisions for next iteration

1. **Fix the factual error:** replace the GitHub RSS approach with the WordPress REST
   API (`wp-json/wp/v2/changelogs`) as the primary path; update `fetch_github.py` and
   SKILL.md. This is a correctness fix regardless of the skill's overall value.
2. **Tighten eval-2 assertion** to include a recall floor (e.g. "lists >= N known
   preview items in window") so undercounts fail.
3. **Re-run and decide** whether speed-only benefit justifies the context cost, or
   whether to sharpen scope.

Separate from this skill: the recurring `microsoft-foundry-resources` staleness finding
(Agent Framework now unified C#+Python, id=564312) is a real repo issue but out of scope
for this PR.
