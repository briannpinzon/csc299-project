
import os
import json
import textwrap
from typing import List, Optional

try:
    import requests
except Exception:
    requests = None


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def summarize_with_openai(paragraph: str, model: str = "chatgpt-5-mini") -> Optional[str]:
    """Call the OpenAI Chat Completions API to get a short-phrase summary.

    Returns the phrase on success, or None if the API key is missing or the HTTP call failed.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    if requests is None:
        print("requests library is not available; cannot call OpenAI API")
        return None

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    system_prompt = (
        "You are a concise summarizer.\n"
        "Given a paragraph describing a task, return a very short phrase (12-16 words) that captures the task.\n"
        "Return only the short phrase — no explanation, no punctuation at the end."
    )

    user_prompt = (
        "Paragraph:\n\n" + paragraph + "\n\nSummarize the above paragraph as a short phrase (no more than 16 words)."
    )

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": 16,
        "temperature": 0.2,
    }

    try:
        resp = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        # Newer API returns choices[0].message.content
        content = data["choices"][0]["message"]["content"].strip()
        # Ensure single-line summary
        return " ".join(content.splitlines()).strip()
    except Exception as e:
        print(f"OpenAI API call failed: {e}")
        return None


def simulated_summary(paragraph: str) -> str:
    """Produce a simple short-phrase fallback summary without calling the API.

    This is intentionally simple: we take the first sentence and extract up to 16 important words.
    """
    # Normalize whitespace and get first sentence
    text = " ".join(paragraph.split())
    # Break into sentences (naive)
    first_sentence = text.split(".")
    if not first_sentence:
        words = text.split()[:6]
    else:
        words = first_sentence[0].split()[:6]
    # Clean punctuation
    words = [w.strip(" ,;:-()[]\"'") for w in words if w]
    phrase = " ".join(words)
    # Make it look like a title phrase
    return phrase.capitalize() or "Summary"


def summarize_paragraphs(paragraphs: List[str], model: str = "chatgpt-5-mini") -> List[str]:
    """Summarize each paragraph independently. Use OpenAI when available, otherwise fallback."""
    summaries: List[str] = []
    api_key = os.getenv("OPENAI_API_KEY")
    for i, p in enumerate(paragraphs, start=1):
        if api_key and requests is not None:
            s = summarize_with_openai(p, model=model)
            if s:
                summaries.append(s)
                continue
        # Fallback
        summaries.append(simulated_summary(p) + " (simulated)")
    return summaries


SAMPLE_PARAGRAPHS = [
    textwrap.dedent(
        """
        We need to build a secure user authentication system for our web application. The
        feature should include signup, login, password reset, and email verification. It must
        support hashed passwords, rate limiting on login attempts, and clear error messages
        for users. Document the API endpoints and include unit tests.
        """
    ),

    textwrap.dedent(
        """
        Analyze the last five years of sales data across all product categories to identify
        seasonal trends and top-performing regions. Produce a short report with charts that show
        month-over-month growth and provide actionable recommendations for inventory planning.
        Deliver the results as a PDF and a small dashboard.
        """
    ),
]


def main():
    print("Summarizing sample paragraphs using Chat Completions (ChatGPT-5-mini) if available...")
    summaries = summarize_paragraphs(SAMPLE_PARAGRAPHS)
    print()
    for i, (p, s) in enumerate(zip(SAMPLE_PARAGRAPHS, summaries), start=1):
        print(f"Description {i}:")
        print("- " + " ".join(p.split()[:40]) + ("..." if len(p.split()) > 40 else ""))
        print(f"Summary {i}: {s}\n")


if __name__ == "__main__":
    main()
