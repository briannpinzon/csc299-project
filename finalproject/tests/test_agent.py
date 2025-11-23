from pkms.agent import summarize_text, suggest_tasks


def test_summarize_text_basic():
    text = "This is a sentence. This is another sentence. And another one."
    s = summarize_text(text, max_sentences=2)
    assert "This is a sentence." in s
    assert "This is another sentence." in s


def test_suggest_tasks_basic():
    text = "We should write the report. Call Alice. Todo: prepare slides."
    suggestions = suggest_tasks(text, max_suggestions=5)
    assert isinstance(suggestions, list)
    assert any("write" in s["title"].lower() or "todo" in s["title"].lower() for s in suggestions)
