#!/usr/bin/env bash

set -euo pipefail

# Global error handler to ensure graceful exit
trap 'echo "⚠️  Unexpected error on line $LINENO. Exiting gracefully..."; exit 1' ERR

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$ROOT_DIR/ai_dev/logs"
PROMPT_FILE="$ROOT_DIR/ai_dev/claude_auto_loop_prompt.txt"
STOP_FILE="$ROOT_DIR/ai_dev/STOP"

ITERATIONS="${1:-5}"
MODEL="${CLAUDE_MODEL:-}"
EFFORT="${CLAUDE_EFFORT:-medium}"
PERMISSION_MODE="${CLAUDE_PERMISSION_MODE:-auto}"
AUTO_COMMIT="1"  # FORCED: Always commit after each iteration
EXTRA_ARGS=()

mkdir -p "$LOG_DIR"

# Remove STOP file if it exists from previous run
if [[ -f "$STOP_FILE" ]]; then
  echo "Removing existing STOP file from previous run..."
  rm "$STOP_FILE"
fi

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

if [[ "$PERMISSION_MODE" == "bypassPermissions" ]]; then
  EXTRA_ARGS+=(--dangerously-skip-permissions)
fi

echo "============================================================"
echo "Claude Auto Loop - AI Development Session"
echo "============================================================"
echo "Root: $ROOT_DIR"
echo "Logs: $LOG_DIR"
echo "Iterations: $ITERATIONS"
echo "Permission mode: $PERMISSION_MODE"
echo "Auto commit: FORCED (always enabled)"
[[ -n "$MODEL" ]] && echo "Model: $MODEL"
[[ -n "$EFFORT" ]] && echo "Effort: $EFFORT"
echo
echo "To stop the loop after current iteration: touch $STOP_FILE"
echo "============================================================"
echo

SUCCESS_COUNT=0
FAIL_COUNT=0

for ((i = 1; i <= ITERATIONS; i++)); do
  # Wrap entire iteration in error handling
  (
    set +e  # Disable exit on error for this iteration

    if [[ -f "$STOP_FILE" ]]; then
      echo "⚠️  Stop file detected before iteration $i. Exiting gracefully."
      rm "$STOP_FILE"
      exit 99  # Special exit code to break loop
    fi

    timestamp="$(date +%Y%m%d-%H%M%S)"
    log_file="$LOG_DIR/claude-iteration-${i}-${timestamp}.log"

    echo
    echo "============================================================"
    echo "=== Iteration $i / $ITERATIONS ($(date '+%Y-%m-%d %H:%M:%S')) ==="
    echo "============================================================"
    echo "Logging to: $log_file"
    echo

    ITERATION_SUCCESS=true

    # Run Claude command with proper error handling
    set -o pipefail  # Enable pipefail for this section
    (
      set -e
      cd "$ROOT_DIR"
      cat "$PROMPT_FILE" | claude -p \
        "${EXTRA_ARGS[@]}" \
        --verbose \
        --output-format stream-json \
        --include-partial-messages \
        --add-dir "$ROOT_DIR"
    ) 2>&1 | python3 -c '
import json
import sys

for raw_line in sys.stdin:
    line = raw_line.rstrip("\n")
    if not line:
        continue
    try:
        event = json.loads(line)
    except json.JSONDecodeError:
        print(line, flush=True)
        continue

    event_type = event.get("type", "")
    if event_type in {"assistant", "message"}:
        message = event.get("message", {})
        content = message.get("content", [])
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text = block.get("text", "")
                    if text:
                        print(text, end="", flush=True)
        elif isinstance(content, str) and content:
            print(content, end="", flush=True)
    elif event_type in {"content_block_delta", "delta"}:
        delta = event.get("delta", {})
        text = delta.get("text", "")
        if text:
            print(text, end="", flush=True)
    elif event_type in {"content_block_stop", "message_stop"}:
        print(flush=True)
    elif event_type == "error":
        print("\n[Claude error] {}".format(event.get("error", event)), flush=True)
    else:
        text = event.get("text", "")
        if text:
            print(text, end="", flush=True)
' | tee "$log_file"
    PIPE_EXIT=${PIPESTATUS[0]}  # Get exit code of the first command in pipe
    set +o pipefail  # Disable pipefail

    if [[ $PIPE_EXIT -ne 0 ]]; then
      echo "⚠️  Claude command failed with exit code $PIPE_EXIT"
      ITERATION_SUCCESS=false
    fi

    echo
    echo "------------------------------------------------------------"

    # FORCED AUTO COMMIT: Always commit after each iteration
    git -C "$ROOT_DIR" diff --quiet --exit-code
    UNSTAGED=$?
    git -C "$ROOT_DIR" diff --cached --quiet --exit-code
    STAGED=$?

    if [[ $UNSTAGED -ne 0 ]] || [[ $STAGED -ne 0 ]]; then
      git -C "$ROOT_DIR" add -A

      git -C "$ROOT_DIR" diff --cached --quiet --exit-code
      HAS_CHANGES=$?

      if [[ $HAS_CHANGES -ne 0 ]]; then
        commit_message="$(
          python3 - "$log_file" <<'PY' 2>/dev/null || echo ""
import pathlib
import re
import sys

try:
    text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    match = re.search(r"\*?\*?Commit message:\*?\*?\s*(.+)", text, re.IGNORECASE)
    if match:
        print(match.group(1).strip())
except Exception:
    pass
PY
        )"

        if [[ -z "$commit_message" ]]; then
          echo "⚠️  WARNING: No commit message found in Claude output. Using default message."
          commit_message="AI iteration $i - auto commit"
        fi

        echo "📝 Committing changes with message: $commit_message"
        if git -C "$ROOT_DIR" commit -m "$commit_message" 2>&1; then
          echo "✅ Changes committed successfully"
          exit 0  # Success
        else
          echo "❌ Commit failed, but continuing..."
          ITERATION_SUCCESS=false
          exit 1  # Failure
        fi
      else
        echo "ℹ️  No staged changes to commit after iteration $i."
        exit 0  # Success (no changes)
      fi
    else
      echo "ℹ️  No repository changes detected after iteration $i."
      exit 0  # Success (no changes)
    fi
  )

  ITER_EXIT=$?

  if [[ $ITER_EXIT -eq 99 ]]; then
    # Stop file detected
    break
  elif [[ $ITER_EXIT -eq 0 ]]; then
    ((SUCCESS_COUNT++))
    echo "✅ Iteration $i completed successfully"
  else
    ((FAIL_COUNT++))
    echo "⚠️  Iteration $i completed with errors, but continuing to next iteration..."
  fi

  echo "------------------------------------------------------------"

  # Small delay between iterations to avoid rate limiting
  if [[ $i -lt $ITERATIONS ]]; then
    sleep 2
  fi
done

echo
echo "============================================================"
echo "Session Summary"
echo "============================================================"
echo "Total iterations: $((SUCCESS_COUNT + FAIL_COUNT))"
echo "Successful: $SUCCESS_COUNT"
echo "Failed: $FAIL_COUNT"
echo "Logs saved to: $LOG_DIR"
echo "============================================================"
echo
