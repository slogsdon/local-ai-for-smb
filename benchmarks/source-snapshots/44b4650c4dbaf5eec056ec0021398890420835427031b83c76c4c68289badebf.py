"""Provider transport; retain native Ollama timing rather than proxying it away."""
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

PROVIDERS = {
    "ollama": ("OLLAMA_BASE_URL", "http://127.0.0.1:11434", "native"),
    "lemonade": ("LEMONADE_BASE_URL", "http://127.0.0.1:8001/api/v1", "openai"),
    "nvidia-nim": ("NIM_BASE_URL", "https://integrate.api.nvidia.com/v1", "openai"),
}


def endpoint(provider):
    variable, default, _ = PROVIDERS[provider]
    url = os.environ.get(variable, default).rstrip("/")
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme not in ("http", "https") or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("Endpoint must be HTTP(S), without credentials, query, or fragment")
    if provider == "nvidia-nim" and parsed.scheme != "https":
        raise ValueError("NIM credentials require HTTPS")
    return url


def request_json(provider, path, body=None, timeout=180):
    headers = {"Content-Type": "application/json"}
    if provider == "nvidia-nim":
        key = os.environ.get("NVIDIA_API_KEY")
        if not key:
            raise ValueError("NVIDIA_API_KEY is required")
        headers["Authorization"] = "Bearer " + key
    request = urllib.request.Request(endpoint(provider) + path,
        data=None if body is None else json.dumps(body).encode(), headers=headers)
    # Do not follow redirects carrying credentials to a different service.
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None
    with urllib.request.build_opener(NoRedirect).open(request, timeout=timeout) as response:
        return json.load(response)


def make_request(provider, model, messages, temperature, max_tokens, context, seed):
    body = {"model": model, "messages": messages, "stream": False}
    if provider == "ollama":
        body["options"] = {"temperature": temperature, "num_predict": max_tokens, "num_ctx": context}
        body["keep_alive"] = "5m"
        if seed is not None:
            body["options"]["seed"] = seed
        return "/api/chat", body
    body.update(temperature=temperature, max_tokens=max_tokens)
    if seed is not None:
        body["seed"] = seed
    return "/chat/completions", body


def normalize(provider, raw):
    if provider == "ollama":
        duration = raw.get("eval_duration")
        count = raw.get("eval_count")
        return {"response": raw["message"]["content"], "input_tokens": raw.get("prompt_eval_count"),
            "output_tokens": count, "tokens_per_second": count / (duration / 1e9) if duration and count is not None else None,
            "native_metrics": {k: raw.get(k) for k in ("load_duration", "prompt_eval_duration", "eval_duration", "total_duration")},
            "finish_reason": raw.get("done_reason")}
    choice = raw["choices"][0]
    usage = raw.get("usage") or {}
    return {"response": choice["message"]["content"], "input_tokens": usage.get("prompt_tokens"),
        "output_tokens": usage.get("completion_tokens"), "tokens_per_second": None,
        "native_metrics": {}, "finish_reason": choice.get("finish_reason")}


def generate(provider, path, body, timeout):
    started = time.monotonic()
    result = dict(response=None, input_tokens=None, output_tokens=None, tokens_per_second=None,
        time_to_first_token=None, native_metrics={}, finish_reason=None, raw_response=None, error=None)
    try:
        result["raw_response"] = request_json(provider, path, body, timeout)
        result.update(normalize(provider, result["raw_response"]))
    except urllib.error.HTTPError as error:
        # Bodies may echo credentials or infrastructure details. Record status only.
        result["error"] = {"type": "http", "status": error.code}
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, KeyError, IndexError, TypeError) as error:
        result["error"] = {"type": type(error).__name__}
    result["total_time"] = time.monotonic() - started
    return result
