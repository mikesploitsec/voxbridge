# VoxBridge - OpenAI API Proxy Bridge
# Developed by Mikesploit - https://github.com/mikesploitsec/voxbridge
# Description: Flask API bridge to OpenAI (Assistants + Chat), with CLI integration, metrics, and logging.
# License: CC BY-NC 4.0 (Non-Commercial)
# Contact: mikesploit@proton.me

## Features
- Supports both OpenAI Assistants and raw GPT-4 completions
- Automatic routing to assistants based on prompt prefix
- CLI wrappers for Bash and PowerShell
- Prometheus-style `/metrics` and `/metrics/summary` for Grafana dashboards
- Rotating log files for prompts and balance API responses

## Planend Features
- Support for local AI models running in Ollama containers
- Better code lol

## Quickstart
1. Clone the repo
2. Create your `.env` file from `.env.example`
3. Update the `VOXBRIDGE_ASSISTANTS` with your assistant name-ID pairs
```env
OPENAI_API_KEY=sk-...
VOXBRIDGE_ASSISTANTS="{\"assistant_1\": \"asst-xxxxxxxxxxxxxxxxxxxx\", \"assistant_2\": \"asst-yyyyyyyyyyyyyyyyyyyy\"}"
```

4. Run with Docker:
```bash
docker compose up --build -d
```

5. Test from CLI (after symlinking or copying `ask.sh` or `ask.ps1`):
```bash
ask hello world
ask assistant_1 scan for threats
```

## CLI Wrappers
- `ask.sh`: Bash shell script with randomized loading messages
- `ask.ps1`: PowerShell script with similar functionality

**Sample output:**
```bash
$ ask what is the airspeed velocity of an unladen swallow
Consulting the AI oracle...
About 11 meters per second, or 40 kilometers per hour, for Europan swallow. However, it's important to note that these figures could vary due to a number of factors such as the specific species of swallow, its age, size, health, and the weather conditions.
```

## Metrics
- Prometheus-compatible `/metrics`
- JSON summary via `/metrics/summary`
```json
{
  "avg_latency": 1.234,
  "requests": 42,
  "tokens": 1287
}
```

## Known Issues
- When using GPT-4 fallback (no assistant), the first word of the prompt will be incorrectly removed if it doesn't match an assistant key. This will be patched in a future version.

## Contributing
Pull requests welcome! This project is designed for educational use and beginner-friendly hacking.

---

"On the shoulders of giants" – Built with Flask, OpenAI Python SDK, Prometheus, and pure stubbornness.

---

MIT-style vibes, Creative Commons license.
Don't sell it. But do use it, remix it, and learn from it.

Thanks for checking out the project!
This is me learning Python, Git, Docker, and OpenAI in public.
If you’ve got feedback, feature ideas, or just want to say hi, I’d love to hear from you.
– mikesploit

