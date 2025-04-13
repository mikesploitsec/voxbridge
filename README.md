# VoxBridge – OpenAI API Proxy Bridge

Built by [mikesploit](https://github.com/mikesploitsec/voxbridge)  
**License:** CC BY-NC 4.0 (Non-Commercial)  
**Contact:** [mikesploit@proton.me](mailto:mikesploit@proton.me)  

A lightweight Flask API proxy for OpenAI’s Assistants and GPT-4 completions.  
Designed for terminal fans, red team tinkerers, and log file lurkers.  
Includes CLI tools, Prometheus metrics, and good vibes.

## ✨ Features

- Assistant routing via prompt prefix or CLI flag
- Supports OpenAI Assistants + raw GPT-4 completions
- Bash and PowerShell wrappers with animated output
- Prometheus-style `/metrics` and `/metrics/summary`
- Rotating log files for prompts and API stats

## 🛠️ Planned Features

- Ollama support (local model routing)
- Better code lol
- Assistant routing fixes (see Known Issues)

## ⚡ Quickstart

1. Clone the repo  
2. Copy `.env.example` → `.env`  
3. Update your API key and assistants map:

    ```env
    OPENAI_API_KEY=sk-...
    VOXBRIDGE_ASSISTANTS="{\"assistant_1\": \"asst-xxxxxxxx\", \"assistant_2\": \"asst-yyyyyyyy\"}"
    ```

4. Launch with Docker:

    ```bash
    docker compose up --build -d
    ```

5. Test it:

    ```bash
    ask hello world
    ask assistant_1 scan for threats
    ```

## 🖥️ CLI Wrappers

- `ask.sh`: Bash shell script with randomized loading messages
- `ask.ps1`: PowerShell script with similar functionality

**Sample output:**
```bash
$ ask what is the airspeed velocity of an unladen swallow
Consulting the AI oracle...
About 11 meters per second, or 40 kilometers per hour, for Europan swallow. However, it's important to note that these figures could vary due to a number of factors such as the specific species of swallow, its age, size, health, and the weather conditions.
```

## 📊 Metrics

- Prometheus-compatible `/metrics`
- JSON summary via `/metrics/summary`
```json
{
  "avg_latency": 1.234,
  "requests": 42,
  "tokens": 1287
}
```

## 🫢 Known Issues
- When using GPT-4 fallback (no assistant), the first word of the prompt will be incorrectly removed if it doesn't match an assistant key. This will be patched in a future version.

## 🤩 Contributing

Pull requests welcome! This project is designed for educational use and beginner-friendly hacking.
MIT-style vibes, Creative Commons license.
Don't sell it. But do use it, remix it, and learn from it.

## 🙏 Thanks!
Thanks for checking out the project!
This is me learning Python, Git, Docker, and OpenAI in public.
If you’ve got feedback, feature ideas, or just want to say hi, I’d love to hear from you.
– mikesploit

### Support
If this tool made your terminal more powerful (or your day more fun), you can support the madness here:
☕ [ko-fi.com/mikesploit](https://ko-fi.com/mikesploit)  
