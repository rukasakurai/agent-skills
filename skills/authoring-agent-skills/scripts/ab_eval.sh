#!/usr/bin/env bash
# Reproducible with/without-skill A/B for one eval, in isolated Copilot CLI sessions.
# Re-run this and grade the transcripts against evals/evals.json to check a skill
# still beats its baseline (and hasn't regressed). Output goes to a gitignored
# workspace beside the skill, never into the shipped skill folder.
#
# Usage: scripts/ab_eval.sh <skill-dir> <eval-id> [model]
#   e.g. scripts/ab_eval.sh skills/authoring-agent-skills 1 claude-sonnet-4.6
set -euo pipefail

SKILL_DIR="${1:?usage: ab_eval.sh <skill-dir> <eval-id> [model]}"
EVAL_ID="${2:?eval id from <skill-dir>/evals/evals.json}"
MODEL="${3:-claude-sonnet-4.6}"
SKILL_DIR="${SKILL_DIR%/}"
NAME="$(basename "$SKILL_DIR")"

PROMPT="$(python3 - "$SKILL_DIR/evals/evals.json" "$EVAL_ID" <<'PY'
import json, sys
evals = json.load(open(sys.argv[1]))["evals"]
print(next(e for e in evals if str(e["id"]) == sys.argv[2])["prompt"])
PY
)"

WS="$(dirname "$SKILL_DIR")/${NAME}-workspace"
OUT="$WS/iteration-$(date +%Y%m%d-%H%M%S)-eval${EVAL_ID}"
mkdir -p "$OUT"
echo "skill=$NAME eval=$EVAL_ID model=$MODEL -> $OUT"

run() { copilot -p "$1" --session-id "$(uuidgen)" --model "$MODEL" --allow-all-tools --no-color; }

{ echo "# baseline (no skill)"; run "$PROMPT"; } > "$OUT/baseline.out" 2>&1
{ echo "# with skill"; run "You have this Agent Skill available; apply it when relevant.

<skill name=$NAME>
$(cat "$SKILL_DIR/SKILL.md")
</skill>

$PROMPT"; } > "$OUT/with_skill.out" 2>&1

echo "wrote $OUT/{baseline,with_skill}.out"
echo "grade both against the assertions for eval $EVAL_ID in $SKILL_DIR/evals/evals.json"
