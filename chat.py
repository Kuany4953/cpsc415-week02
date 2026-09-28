#!/usr/bin/env python3
"""chat.py — one-shot OpenAI-compatible chat client.

Reads CHAT_BASE_URL, CHAT_MODEL, OPENROUTER_API_KEY from the environment,
POSTs a system + user message to {CHAT_BASE_URL}/chat/completions, prints
the assistant's reply, then prints a final summary line:

    --- model=<name> input=<n> output=<m>
"""

import json
import os
import sys
import urllib.error
import urllib.request


# --- Editable knobs ---------------------------------------------------------

MAX_TOKENS = 20  # observation knob: set low to watch the answer get cut off.
SYSTEM_MESSAGE = "You are a helpful assistant. Answer concisely."


# --- Helpers ----------------------------------------------------------------

def die(msg: str) -> None:
    """Print msg to stderr and exit with status 1."""
    print(msg, file=sys.stderr)
    sys.exit(1)


# --- Main -------------------------------------------------------------------

def main() -> None:
    # 1. argv: exactly one positional arg, the question.
    if len(sys.argv) != 2:
        die(f'usage: {sys.argv[0]} "<question>"')

    question = sys.argv[1]

    # 2. env: all three required. Empty string counts as missing.
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    base_url = os.environ.get("CHAT_BASE_URL", "")
    model = os.environ.get("CHAT_MODEL", "")

    missing = [
        name for name, value in (
            ("OPENROUTER_API_KEY", api_key),
            ("CHAT_BASE_URL", base_url),
            ("CHAT_MODEL", model),
        )
        if not value
    ]
    if missing:
        die(f"missing required environment variable(s): {', '.join(missing)}")

    # 3. Build the request body.
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": question},
        ],
        "max_tokens": MAX_TOKENS,
    }).encode("utf-8")

    url = base_url.rstrip("/") + "/chat/completions"
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    # 4. Send the request.
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            status = resp.status
            raw = resp.read()
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        die(f"HTTP {e.code}\n{body_text}")
    except urllib.error.URLError as e:
        die(f"connection error: {e.reason}")
    except TimeoutError:
        die("request timed out")

    if status < 200 or status >= 300:
        die(f"HTTP {status}\n{raw.decode('utf-8', errors='replace')}")

    # 5. Parse the JSON response.
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as e:
        die(f"failed to decode response JSON: {e}\n{raw.decode('utf-8', errors='replace')}")

    # 6. Pull the assistant content out.
    try:
        content = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        die(f"response missing 'choices[0].message.content': {payload}")

    print(content)

    # 7. Summary line.
    #    model name comes from the response (what the provider reported).
    #    usage may be missing on local models — that's not a failure, just unknown.
    model_name = payload.get("model", "unknown")
    usage = payload.get("usage")
    if isinstance(usage, dict) and "prompt_tokens" in usage and "completion_tokens" in usage:
        print(f"--- model={model_name} input={usage['prompt_tokens']} output={usage['completion_tokens']}")
    else:
        print(f"--- model={model_name} input=unknown output=unknown")


if __name__ == "__main__":
    main()
