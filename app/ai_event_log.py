# envelope:control art12.logging v1
"""Structured event log for model calls (EU AI Act Article 12). Records metadata, not prompt text."""
import json
import logging
import time
import uuid

_log = logging.getLogger("ai_events")


def log_model_call(model: str, purpose: str, outcome: str, latency_ms: float, **meta) -> str:
    event_id = str(uuid.uuid4())
    _log.info(json.dumps({"event": "model_call", "id": event_id, "ts": time.time(), "model": model, "purpose": purpose, "outcome": outcome, "latency_ms": round(latency_ms, 1), **meta}))
    return event_id
