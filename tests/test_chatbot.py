from types import SimpleNamespace

from app import chatbot


class FakeClient:
    def __init__(self, content):
        self.messages = SimpleNamespace(create=lambda **kw: SimpleNamespace(model=kw["model"], content=content))


def test_welcome_message_mentions_ava():
    assert "Ava" in chatbot.start_conversation()


def test_text_reply():
    c = FakeClient([SimpleNamespace(type="text", text="Thanks for applying!")])
    assert chatbot.reply([{"role": "user", "content": "hi"}], client=c) == "Thanks for applying!"


def test_tool_call_is_reported():
    c = FakeClient([SimpleNamespace(type="tool_use", name="shortlist_candidate", input={"candidate_id": "C1"})])
    out = chatbot.reply([{"role": "user", "content": "am I through?"}], client=c)
    assert "shortlist_candidate" in out
