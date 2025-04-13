# VoxBridge - OpenAI API Proxy Bridge
# Developed by Mikesploit - https://github.com/mikesploitsec/voxbridge
# Description: Flask API bridge to OpenAI (Assistants + Chat), with CLI integration, metrics, and logging.
# License: CC BY-NC 4.0 (Non-Commercial)
# Contact: mikesploit@proton.me

from flask import Flask, request, jsonify, Response
import os, time, json, re
from openai import OpenAI
from metrics import REQUEST_COUNT, TOKEN_COUNT, LATENCY, METRICS
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# === Logging Setup === #
LOG_DIR = Path("/voxbridge/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

PROMPT_LOG = LOG_DIR / "prompts.log"
BALANCE_LOG = LOG_DIR / "balance.log"

def create_logger(name, log_file, level=logging.INFO):
    handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
    formatter = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False
    return logger

prompt_logger = create_logger("prompt_logger", PROMPT_LOG)
balance_logger = create_logger("balance_logger", BALANCE_LOG)

# === Core App Setup === #
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
app = Flask(__name__)

# Load assistant routing from VOXBRIDGE_ASSISTANTS (JSON string)
ASSISTANT_MAP = {}
try:
    assistants_json = os.getenv("VOXBRIDGE_ASSISTANTS", "{}")
    ASSISTANT_MAP = json.loads(assistants_json)
except Exception as e:
    print(f"[WARN] Failed to load VOXBRIDGE_ASSISTANTS: {e}")

@app.route("/ask", methods=["POST"])
@LATENCY.time()
def ask():
    data = request.get_json()

    # Get prompt and assistant from payload
    prompt = data.get("prompt", "")
    assistant = data.get("assistant")

    # Split prompt only if assistant is not already provided
    if not assistant and isinstance(prompt, str):
        words = prompt.strip().split()
        if words and words[0] in ASSISTANT_MAP:
            assistant = words[0]
            prompt = " ".join(words[1:])  # Only drop assistant name
        else:
            assistant = None  # Force to None so it triggers fallback mode

    # Route to assistant if matched
    if assistant in ASSISTANT_MAP:
        try:
            start = time.time()
            thread = client.beta.threads.create()
            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=prompt
            )
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=ASSISTANT_MAP[assistant]
            )

            while True:
                run_status = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
                if run_status.status == "completed":
                    break
                elif run_status.status in ["failed", "cancelled", "expired"]:
                    return jsonify({"error": f"Run {run_status.status}"}), 500
                time.sleep(1)

            messages = client.beta.threads.messages.list(thread_id=thread.id)
            result = messages.data[0].content
            if isinstance(result, list) and len(result) > 0:
                result = result[0].text.value
            elif isinstance(result, dict):
                result = result.get("text", {}).get("value", "[No response text]")

            result = re.sub(r"\\n{2,}", "\n", result)
            result = re.sub(r"\\n", "\n", result)
            result = re.sub(r"\\*", "", result)

            duration = round(time.time() - start, 2)
            prompt_logger.info(f"[{assistant}] Prompt: {prompt}")
            prompt_logger.info(f"[{assistant}] Response: {result.strip()} | Duration: {duration}s")
            REQUEST_COUNT.inc()

            return jsonify({
                "response": result.strip(),
                "tokens": 0,
                "duration": duration
            })

        except Exception as e:
            prompt_logger.error(f"[{assistant}] Error: {str(e)}")
            return jsonify({"error": str(e)}), 500

    # Default fallback: GPT-4 chat completion
    try:
        start = time.time()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        result = response.choices[0].message.content
        tokens = response.usage.total_tokens
        duration = round(time.time() - start, 2)
        REQUEST_COUNT.inc()
        TOKEN_COUNT.inc(tokens)

        prompt_logger.info(f"[chat] Prompt: {prompt}")
        prompt_logger.info(f"[chat] Tokens: {tokens} | Duration: {duration}s")
        prompt_logger.info(f"[chat] Response: {result.strip()}")

        return jsonify({
            "response": result.strip(),
            "tokens": tokens,
            "duration": duration
        })
    except Exception as e:
        prompt_logger.error(f"[chat] Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/balance", methods=["GET"])
def balance():
    balance_logger.info("Balance endpoint hit, but feature is deprecated by OpenAI.")
    return jsonify({
        "error": "The /balance route is no longer supported. OpenAI disabled access to billing data via API keys in 2025.",
        "note": "You can manually check your usage at https://platform.openai.com/account/usage",
        "status": "deprecated"
    }), 200

@app.route("/metrics")
def metrics():
    return Response(METRICS(), mimetype="text/plain")

@app.route("/metrics/summary")
def metrics_summary():
    try:
        latency_data = next(metric for metric in LATENCY.collect())
        count = 0
        total = 0.0

        for sample in latency_data.samples:
            if sample.name.endswith("_count"):
                count = sample.value
            elif sample.name.endswith("_sum"):
                total = sample.value

        request_count = REQUEST_COUNT._value.get()
        token_count = TOKEN_COUNT._value.get()
        avg_latency = round(total / count, 3) if count else 0

        return jsonify({
            "requests": request_count,
            "tokens": token_count,
            "avg_latency": avg_latency
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
