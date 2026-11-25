# envelope:control art14.oversight v1
"""Human oversight gate (EU AI Act Article 14). A person must approve before the action runs."""
from typing import Optional


class ApprovalRequired(Exception):
    pass


def require_human_approval(action: str, approved_by: Optional[str]) -> None:
    if not approved_by:
        raise ApprovalRequired(f"'{action}' needs a person's approval before it runs")
