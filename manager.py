from pathlib import Path

from exceptions import InvalidInputError, TaskNotFoundError
from models import Priority, Status, Task
from storage import load_tasks, save_tasks


def require_title(title: str) -> str:
    cleaned = title.strip()
    if cleaned == "":
        raise InvalidInputError("Title cannot be empty.")
    return cleaned


def parse_status(text: str) -> Status:
    try:
        return Status(text.strip().lower())
    except ValueError as error:
        raise InvalidInputError("Status must be todo, in_progress, or done.") from error


def parse_priority(text: str) -> Priority:
    try:
        return Priority(text.strip().lower())
    except ValueError as error:
        raise InvalidInputError("Priority must be low, medium, or high.") from error


class TaskManager:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.tasks = load_tasks(path)
        if self.tasks:
            highest = max(task.task_id for task in self.tasks)
            self.next_id = highest + 1
        else:
            self.next_id = 1

    def add_task(self, title: str, description: str, priority: str) -> Task:
        cleaned_title = require_title(title)
        parsed_priority = parse_priority(priority)
        task = Task(
            task_id=self.next_id,
            title=cleaned_title,
            description=description.strip(),
            status=Status.TODO,
            priority=parsed_priority,
        )
        self.next_id = self.next_id + 1
        self.tasks.append(task)
        save_tasks(self.tasks, self.path)
        return task

    def get_task(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        raise TaskNotFoundError(f"No task with id {task_id}.")

    def list_tasks(
        self,
        status: Status | None = None,
        priority: Priority | None = None,
    ) -> list[Task]:
        chosen: list[Task] = []
        for task in self.tasks:
            status_matches = status is None or task.status == status
            priority_matches = priority is None or task.priority == priority
            if status_matches and priority_matches:
                chosen.append(task)
        chosen.sort(key=lambda task: task.created_at)
        return chosen

    def update_task(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
        status: str | None = None,
        priority: str | None = None,
    ) -> Task:
        task = self.get_task(task_id)
        if title is not None:
            task.title = require_title(title)
        if description is not None:
            task.description = description.strip()
        if status is not None:
            task.status = parse_status(status)
        if priority is not None:
            task.priority = parse_priority(priority)
        save_tasks(self.tasks, self.path)
        return task

    def delete_task(self, task_id: int) -> Task:
        task = self.get_task(task_id)
        self.tasks.remove(task)
        save_tasks(self.tasks, self.path)
        return task

    def mark_done(self, task_id: int) -> Task:
        task = self.get_task(task_id)
        task.status = Status.DONE
        save_tasks(self.tasks, self.path)
        return task
