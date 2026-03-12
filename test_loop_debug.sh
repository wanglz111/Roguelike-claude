#!/usr/bin/env bash

# Disable exit on error temporarily to debug
set -uo pipefail

ROOT_DIR="/home/lucascool/Roguelike"
PROMPT_FILE="$ROOT_DIR/ai_dev/claude_auto_loop_prompt.txt"

echo "Testing loop iteration..."

for ((i = 1; i <= 3; i++)); do
  echo "=== Iteration $i ==="

  # Run Claude command
  (
    cd "$ROOT_DIR"
    cat "$PROMPT_FILE" | claude -p \
      --permission-mode auto \
      --verbose \
      --output-format stream-json \
      --include-partial-messages \
      --add-dir "$ROOT_DIR"
  ) > /tmp/claude_output_$i.txt 2>&1

  CLAUDE_EXIT=$?
  echo "Claude exit code: $CLAUDE_EXIT"

  if [[ $CLAUDE_EXIT -ne 0 ]]; then
    echo "Claude failed! Output:"
    tail -20 /tmp/claude_output_$i.txt
    break
  fi

  echo "Iteration $i completed successfully"
  echo
done

echo "Test complete"
