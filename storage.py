import json
from pathlib import Path

from exceptions import InvalidInputError
from models import Task


def load_tasks(path: Path) -> list[Task]:
    if not path.exists():
        return []
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise InvalidInputError("tasks.json is not valid JSON.") from error
    if not isinstance(raw, list):
        raise InvalidInputError("tasks.json must contain a list.")
    tasks: list[Task] = []
    for item in raw:
        if not isinstance(item, dict):
            raise InvalidInputError("Each task in tasks.json must be an object.")
        tasks.append(Task.from_dict(item))
    return tasks


def save_tasks(tasks: list[Task], path: Path) -> None:
    rows = [task.to_dict() for task in tasks]
    path.write_text(json.dumps(rows, indent=2), encoding="utf-8")
