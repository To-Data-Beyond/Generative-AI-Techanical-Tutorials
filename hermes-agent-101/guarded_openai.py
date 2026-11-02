"""Text-only, non-streamed OpenAI cost accounting for the opt-in Hermes demo."""
import fcntl
import json
from pathlib import Path
from contextlib import contextmanager

import httpx
import requests


@contextmanager
def guarded_network(ledger_path):
    ledger = Path(ledger_path)
    original_send = httpx.Client.send
    original_request = requests.sessions.Session.request

    def send(client, request, *args, **kwargs):
        if request.url.host != "api.openai.com" or request.url.path not in {"/v1/chat/completions", "/v1/responses"}:
            raise ValueError("Only the explicit OpenAI inference origin is enabled.")
        payload = json.loads(request.content)
        if payload.get("model") != "gpt-5.4-mini" or payload.get("stream"):
            raise ValueError("Review pricing/accounting before changing model or streaming.")
        maximum = payload.get("max_completion_tokens", payload.get("max_tokens", payload.get("max_output_tokens", 0)))
        if not 0 < maximum <= 1024 or len(request.content) > 150000 or payload.get("service_tier", "default") != "default":
            raise ValueError("Request exceeds the bounded demo contract.")
        bound = len(request.content) + 8192
        reserve = 1.15 * (bound * .75 + maximum * 4.5) / 1_000_000
        with open(str(ledger) + ".lock", "a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            state = json.loads(ledger.read_text()) if ledger.exists() else {"reserved": 0, "calls": []}
            if state["reserved"] + reserve > 1:
                raise RuntimeError("Cumulative one-dollar limit would be exceeded.")
            state["reserved"] += reserve
            index = len(state["calls"])
            state["calls"].append({"reservation": reserve, "input_bound": bound})
            ledger.write_text(json.dumps(state, indent=2))
        response = original_send(client, request, *args, **kwargs)
        response.read()
        data = response.json()
        usage = data.get("usage")
        if response.status_code != 200 or not usage:
            raise RuntimeError("Inference failed or returned no usage; reservation retained.")
        inp = usage.get("input_tokens", usage.get("prompt_tokens"))
        out = usage.get("output_tokens", usage.get("completion_tokens"))
        if inp > bound or out > maximum:
            raise RuntimeError("Usage exceeded its conservative bound.")
        with open(str(ledger) + ".lock", "a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            state = json.loads(ledger.read_text())
            state["calls"][index].update(input_tokens=inp, output_tokens=out, status=200,
                estimated_usd=(inp * .75 + out * 4.5) / 1_000_000)
            ledger.write_text(json.dumps(state, indent=2))
        return response

    def deny(*args, **kwargs):
        raise RuntimeError("Other HTTP clients are disabled in this isolated demonstration.")

    httpx.Client.send = send
    requests.sessions.Session.request = deny
    try:
        yield
    finally:
        httpx.Client.send = original_send
        requests.sessions.Session.request = original_request
