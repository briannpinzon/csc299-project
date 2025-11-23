"""Simple AI agent helpers.

This module implements a small local summarizer and task-suggestion heuristics.
It is intentionally dependency-free so it runs out-of-the-box; users may replace
or extend it to call external APIs or local ML models.
"""
from typing import List, Dict
import re


def summarize_text(text: str, max_sentences: int = 2) -> str:
    """Return a naive summary: first N sentences after trimming whitespace.

    This is a simple fallback summarizer. In production, swap this with
    a call to an external model or local ML component.
    """
    # Simple sentence splitter (naive)
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    if not sentences:
        return ""
    return " ".join(sentences[:max_sentences])


def suggest_tasks(text: str, max_suggestions: int = 5) -> List[Dict[str, str]]:
    """Heuristic extraction of candidate tasks from text.

    Finds sentences that look like actions (start with a verb or contain 'should', 'need to', 'todo').
    Returns a list of suggestion dicts with `title` and `excerpt`.
    """
    sents = re.split(r'(?<=[.!?])\s+', text.strip())
    suggestions = []
    verb_start = re.compile(r'^(?:[A-Z][a-z]+|[A-Z])\b')
    for sent in sents:
        low = sent.lower()
        if any(k in low for k in ("should", "need to", "todo", "please")):
            title = sent.strip()
            suggestions.append({"title": title[:80], "excerpt": sent.strip()})
        elif len(suggestions) < max_suggestions and len(sent.split()) <= 12:
            # short sentences often are action-like
            # crude heuristic: starts with a verb (lowercased)
            first_word = sent.strip().split()[0].lower() if sent.strip() else ""
            if first_word in ("write", "review", "call", "email", "schedule", "create", "update", "fix", "implement"):
                suggestions.append({"title": sent.strip()[:80], "excerpt": sent.strip()})
        if len(suggestions) >= max_suggestions:
            break
    # Fallback: if no suggestions found but text is long, offer a generic review action
    if not suggestions and len(text.strip()) > 120:
        excerpt = text.strip()[:120].rsplit(" ", 1)[0]
        suggestions.append({"title": "Review note", "excerpt": excerpt})
    return suggestions
