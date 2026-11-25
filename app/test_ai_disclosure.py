from app.ai_disclosure import AI_DISCLOSURE, with_ai_disclosure


def test_disclosure_is_prefixed_once():
    out = with_ai_disclosure("Hello")
    assert out.startswith(AI_DISCLOSURE)
    assert with_ai_disclosure(out) == out
