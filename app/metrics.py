from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter("vox_requests_total", "Total prompts processed")
TOKEN_COUNT = Counter("vox_tokens_total", "Total tokens used")
LATENCY = Histogram("vox_latency_seconds", "Request processing time")

def METRICS():
    return generate_latest()
