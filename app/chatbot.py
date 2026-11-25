from app.ai_disclosure import with_ai_disclosure  # envelope: Art. 50(1)
"""Ava: candidate-facing recruiting assistant for TalentScreen."""
import json
import os

from app.screening import score_candidate

MODEL = os.environ.get("TALENTSCREEN_MODEL", "claude-sonnet-5-5")

WELCOME_MESSAGE = with_ai_disclosure("Hi, I'm Ava from TalentScreen. Tell me about the role you're applying for and I'll check your application.")

SYSTEM_PROMPT = (
    "You are Ava, a recruiting assistant. Answer candidates' questions about their application. "
    "Use the tools to shortlist or reject candidates based on their screening score."
)

TOOLS = [
    {
        "name": "shortlist_candidate",
        "description": "Move a candidate to the interview shortlist.",
        "input_schema": {"type": "object", "properties": {"candidate_id": {"type": "string"}}, "required": ["candidate_id"]},
    },
    {
        "name": "reject_candidate",
        "description": "Reject a candidate's application.",
        "input_schema": {"type": "object", "properties": {"candidate_id": {"type": "string"}, "reason": {"type": "string"}}, "required": ["candidate_id"]},
    },
]

DECISIONS = {}


def _client():
    import anthropic

    return anthropic.Anthropic()


def execute_tool(name, args):
    """Run a tool the model asked for. Decisions take effect immediately."""
    if name == "shortlist_candidate":
        DECISIONS[args["candidate_id"]] = "shortlisted"
        return {"ok": True, "status": "shortlisted"}
    if name == "reject_candidate":
        DECISIONS[args["candidate_id"]] = "rejected"
        return {"ok": True, "status": "rejected", "reason": args.get("reason", "")}
    raise ValueError(f"unknown tool {name}")


def reply(history, candidate=None, client=None):
    """Return Ava's next message for a conversation history (list of {role, content})."""
    client = client or _client()
    system = SYSTEM_PROMPT
    if candidate is not None:
        system += f"\nCandidate {candidate['id']} screening score: {score_candidate(candidate):.2f}"
    response = client.messages.create(
        model=MODEL,
        max_tokens=600,
        system=system,
        tools=TOOLS,
        messages=history,
    )
    texts = []
    for block in response.content:
        if block.type == "tool_use":
            try:
                result = execute_tool(block.name, block.input)
            except Exception as exc:  # keep the conversation going if an action is refused
                result = {"ok": False, "error": str(exc)}
            texts.append(f"[{block.name}: {json.dumps(result)}]")
        elif block.type == "text":
            texts.append(block.text)
    return "\n".join(texts)


def start_conversation():
    return WELCOME_MESSAGE
