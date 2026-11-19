from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from exceptions import InvalidInputError


class Status(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    task_id: int
    title: str
    description: str
    status: Status
    priority: Priority
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict[str, str | int]:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, raw: dict[str, object]) -> "Task":
        try:
            return cls(
                task_id=int(raw["task_id"]),
                title=str(raw["title"]),
                description=str(raw["description"]),
                status=Status(str(raw["status"])),
                priority=Priority(str(raw["priority"])),
                created_at=datetime.fromisoformat(str(raw["created_at"])),
            )
        except (KeyError, TypeError, ValueError) as error:
            raise InvalidInputError(
                "A task record is missing a field or has a bad value."
            ) from error
