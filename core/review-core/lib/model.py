"""
review-core / model — normalized Item across all channels (ClickUp, WhatsApp, Gmail).

Goal: one data shape so report/ownership logic is channel-agnostic.
"""
from dataclasses import dataclass, field, asdict
from typing import Optional, Any


@dataclass
class Item:
    source: str                      # "clickup" | "whatsapp" | "gmail"
    kind: str                        # "task" | "message" | "email" | "plan_item"
    title: str
    owner: Optional[str] = None      # assignee / requester
    counterpart: Optional[str] = None  # other side (client, list, group, sender)
    due: Optional[str] = None        # ISO date or None
    status: Optional[str] = None
    priority: Optional[str] = None   # "urgent"|"high"|"normal"|"low"|None
    url: Optional[str] = None
    container: Optional[str] = None  # list / space / group / thread
    mine: Optional[bool] = None      # owned by me (ownership, set by the agent)
    raw: Any = field(default=None, repr=False)

    def to_dict(self):
        d = asdict(self)
        d.pop('raw', None)
        return d


def from_clickup_task(t, container=None):
    pr = (t.get('priority') or {})
    assignees = [a.get('username') for a in t.get('assignees', [])]
    return Item(
        source='clickup', kind='task',
        title=t.get('name', '?'),
        owner=', '.join(assignees) or None,
        counterpart=(t.get('list') or {}).get('name') or container,
        due=_ms_to_iso(t.get('due_date')),
        status=(t.get('status') or {}).get('status'),
        priority=(pr.get('priority') if isinstance(pr, dict) else None),
        url=t.get('url'),
        container=container or (t.get('list') or {}).get('name'),
        raw=t,
    )


def _ms_to_iso(ms):
    if not ms:
        return None
    import datetime
    try:
        return datetime.date.fromtimestamp(int(ms) / 1000).isoformat()
    except (TypeError, ValueError):
        return None
