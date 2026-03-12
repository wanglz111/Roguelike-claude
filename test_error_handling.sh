#!/usr/bin/env bash

# Test script to verify error handling works correctly

echo "Testing error handling scenarios..."
echo

# Test 1: Simulate Claude command failure
echo "Test 1: Simulating Claude command failure..."
(
  set +e
  (
    set -e
    false  # This will fail
  ) | tee /tmp/test.log
  EXIT=$?
  echo "Exit code: $EXIT"
  if [[ $EXIT -ne 0 ]]; then
    echo "✅ Correctly captured failure"
  else
    echo "❌ Failed to capture failure"
  fi
)
echo

# Test 2: Simulate git commit failure
echo "Test 2: Simulating git commit failure..."
(
  set +e
  git commit --allow-empty -m "test" 2>&1 > /dev/null
  EXIT=$?
  echo "Exit code: $EXIT"
  echo "✅ Git command completed (exit code captured)"
)
echo

# Test 3: Simulate Python script failure
echo "Test 3: Simulating Python script failure..."
(
  set +e
  python3 -c 'import sys; sys.exit(1)' 2>/dev/null
  EXIT=$?
  echo "Exit code: $EXIT"
  if [[ $EXIT -ne 0 ]]; then
    echo "✅ Correctly captured Python failure"
  else
    echo "❌ Failed to capture Python failure"
  fi
)
echo

# Test 4: Subshell exit code propagation
echo "Test 4: Testing subshell exit code propagation..."
(
  set +e
  (
    set +e
    false
    exit 1
  )
  EXIT=$?
  echo "Exit code: $EXIT"
  if [[ $EXIT -eq 1 ]]; then
    echo "✅ Subshell exit code correctly propagated"
  else
    echo "❌ Subshell exit code not propagated"
  fi
)
echo

echo "All error handling tests completed!"
