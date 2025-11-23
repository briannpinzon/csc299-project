from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import List, Optional
from datetime import datetime, timezone
import uuid


def _now_iso() -> str:
    # Return an ISO8601 UTC timestamp with explicit Z designator using timezone-aware datetime
    return datetime.now(timezone.utc).astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')


@dataclass
class Note:
    id: str
    title: str
    body: str
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=_now_iso)
    updated_at: str = field(default_factory=_now_iso)
    source: str = "manual"

    @staticmethod
    def create(title: str, body: str, tags: Optional[List[str]] = None, source: str = "manual") -> "Note":
        return Note(
            id=str(uuid.uuid4()),
            title=title,
            body=body,
            tags=tags or [],
            created_at=_now_iso(),
            updated_at=_now_iso(),
            source=source,
        )

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "Note":
        return Note(
            id=d.get("id"),
            title=d.get("title", ""),
            body=d.get("body", ""),
            tags=d.get("tags", []),
            created_at=d.get("created_at", _now_iso()),
            updated_at=d.get("updated_at", _now_iso()),
            source=d.get("source", "manual"),
        )


@dataclass
class Task:
    id: str
    title: str
    description: str = ""
    due_date: Optional[str] = None
    status: str = "todo"
    created_at: str = field(default_factory=_now_iso)
    updated_at: str = field(default_factory=_now_iso)
    source: str = "manual"

    @staticmethod
    def create(title: str, description: str = "", due_date: Optional[str] = None, source: str = "manual") -> "Task":
        return Task(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            due_date=due_date,
            status="todo",
            created_at=_now_iso(),
            updated_at=_now_iso(),
            source=source,
        )

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "Task":
        return Task(
            id=d.get("id"),
            title=d.get("title", ""),
            description=d.get("description", ""),
            due_date=d.get("due_date"),
            status=d.get("status", "todo"),
            created_at=d.get("created_at", _now_iso()),
            updated_at=d.get("updated_at", _now_iso()),
            source=d.get("source", "manual"),
        )


@dataclass
class AgentResult:
    id: str
    note_id: Optional[str]
    summary: str
    suggestions: List[dict]
    confidence: Optional[float] = None
    created_at: str = field(default_factory=_now_iso)

    def to_dict(self) -> dict:
        return asdict(self)
