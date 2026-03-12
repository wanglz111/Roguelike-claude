#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$ROOT_DIR/ai_dev/logs"
PROMPT_FILE="$ROOT_DIR/ai_dev/claude_auto_loop_prompt.txt"
STOP_FILE="$ROOT_DIR/ai_dev/STOP"

ITERATIONS="${1:-5}"
MODEL="${CLAUDE_MODEL:-}"
EFFORT="${CLAUDE_EFFORT:-medium}"
PERMISSION_MODE="${CLAUDE_PERMISSION_MODE:-default}"
AUTO_COMMIT="${CLAUDE_AUTO_COMMIT:-1}"
EXTRA_ARGS=()

mkdir -p "$LOG_DIR"

if [[ ! -f "$PROMPT_FILE" ]]; then
  echo "Missing prompt file: $PROMPT_FILE" >&2
  exit 1
fi

if ! command -v claude >/dev/null 2>&1; then
  echo "claude command not found in PATH" >&2
  exit 1
fi

if [[ -n "$MODEL" ]]; then
  EXTRA_ARGS+=(--model "$MODEL")
fi

if [[ -n "$EFFORT" ]]; then
  EXTRA_ARGS+=(--effort "$EFFORT")
fi

if [[ -n "$PERMISSION_MODE" ]]; then
  EXTRA_ARGS+=(--permission-mode "$PERMISSION_MODE")
fi

echo "Root: $ROOT_DIR"
echo "Logs: $LOG_DIR"
echo "Iterations: $ITERATIONS"
echo "Permission mode: $PERMISSION_MODE"
echo "Auto commit: $AUTO_COMMIT"
[[ -n "$MODEL" ]] && echo "Model: $MODEL"
echo
echo "Create $STOP_FILE to stop the loop after the current iteration."
echo

for ((i = 1; i <= ITERATIONS; i++)); do
  if [[ -f "$STOP_FILE" ]]; then
    echo "Stop file detected before iteration $i. Exiting."
    break
  fi

  timestamp="$(date +%Y%m%d-%H%M%S)"
  log_file="$LOG_DIR/claude-iteration-${i}-${timestamp}.log"

  echo "=== Iteration $i / $ITERATIONS ==="
  echo "Logging to $log_file"

  (
    cd "$ROOT_DIR"
    cat "$PROMPT_FILE" | claude -p \
      "${EXTRA_ARGS[@]}" \
      --add-dir "$ROOT_DIR"
  ) | tee "$log_file"

  if [[ "$AUTO_COMMIT" == "1" ]]; then
    if ! git -C "$ROOT_DIR" diff --quiet --exit-code || ! git -C "$ROOT_DIR" diff --cached --quiet --exit-code; then
      git -C "$ROOT_DIR" add -A

      if ! git -C "$ROOT_DIR" diff --cached --quiet --exit-code; then
        commit_message="$(
          grep -E '^Commit message:' "$log_file" | tail -n 1 | sed 's/^Commit message:[[:space:]]*//'
        )"

        if [[ -z "$commit_message" ]]; then
          commit_message="claude: iteration $i"
        fi

        git -C "$ROOT_DIR" commit -m "$commit_message"
      fi
    else
      echo "No repository changes detected after iteration $i. Skipping commit."
    fi
  fi

  echo
done
