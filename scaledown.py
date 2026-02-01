import requests
import json

SCALEDOWN_URL = "https://api.scaledown.xyz/compress/raw/"

def compress_prompt(context, prompt, api_key):
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "context": context,
        "prompt": prompt,
        "model": "gpt-4o",
        "scaledown": {"rate": "auto"}
    }

    response = requests.post(
        SCALEDOWN_URL,
        headers=headers,
        data=json.dumps(payload),
        timeout=60
    )

    data = response.json()

    if not data.get("successful"):
        raise RuntimeError(data)

    return data["compressed_prompt"], data
