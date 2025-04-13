#!/bin/bash

# === VoxBridge CLI Helper (Bash) ===
# Sends prompt to local VoxBridge instance with optional assistant routing

# Loading hallucination vibes 😵‍💫
loading_lines=(
  "Hallucination loading..."
  "Consulting the AI oracle..."
  "Reality distortion field online..."
  "Assembling a plausible reply..."
  "Routing through linguistic chaos..."
  "Unleashing artificial intelligence..."
  "Fabricating answers with confidence..."
  "Conjuring plausible realities..."
  "Plausibility matrix engaged..."
  "Hallucination seeding complete. Executing..."
)

echo "${loading_lines[$RANDOM % ${#loading_lines[@]}]}"

# Parse arguments
assistant="$1"
shift
prompt="$*"

# If no assistant (single word prompt), treat first word as possible assistant
if [[ -z "$prompt" ]]; then
  prompt="$assistant"
  assistant=""
fi

# Prepare JSON body
if [[ -n "$assistant" ]]; then
  json=$(jq -n --arg prompt "$prompt" --arg assistant "$assistant" '{prompt: $prompt, assistant: $assistant}')
else
  json=$(jq -n --arg prompt "$prompt" '{prompt: $prompt}')
fi

# Send request
curl -s -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d "$json" | jq -r '.response'
