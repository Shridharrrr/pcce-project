import os
import httpx
from typing import List, Optional
from dotenv import load_dotenv
import asyncio

load_dotenv()  # load .env if present

HF_MODEL = "facebook/bart-large-cnn"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
HF_TOKEN = os.getenv("HF_TOKEN")

HEADERS = {"Authorization": f"Bearer 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"} if HF_TOKEN else {}

async def summarize_text(chunks: List[str], max_new_tokens: int = 200) -> Optional[str]:
    """
    Calls Hugging Face Inference API to summarize concatenated text chunks.
    Returns summary string or None on failure.
    """
    if not HF_TOKEN:
        return None

    # Join chunks keeping reasonably small payload
    text = "\n".join(chunks)
    # Truncate to ~6000 characters to keep request small
    text = text[-6000:]

    payload = {
        "inputs": text,
        "parameters": {
            "max_length": max_new_tokens,
            "min_length": 60,
            "do_sample": False
        }
    }

    try:
        attempts = 0
        async with httpx.AsyncClient(timeout=60) as client:
            while attempts < 4:
                resp = await client.post(HF_API_URL, headers=HEADERS, json=payload)
                # Handle model loading
                if resp.status_code in (503, 524):
                    attempts += 1
                    try:
                        info = resp.json()
                        wait_s = min(int(info.get("estimated_time", 10)) + 1, 20)
                    except Exception:
                        wait_s = 8
                    await asyncio.sleep(wait_s)
                    continue
                # Unauthorized or forbidden (bad token)
                if resp.status_code in (401, 403):
                    return None
                if resp.status_code != 200:
                    return None
                data = resp.json()
                # Inference API returns list of dicts with 'summary_text'
                if isinstance(data, list) and data and "summary_text" in data[0]:
                    return data[0]["summary_text"]
                # Some models may return a dict
                if isinstance(data, dict) and "summary_text" in data:
                    return data["summary_text"]
                return None
            return None
    except Exception:
        return None
