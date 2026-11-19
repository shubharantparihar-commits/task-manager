from pathlib import Path

from exceptions import InvalidInputError, TaskNotFoundError
from manager import TaskManager, parse_priority, parse_status
from models import Task


def format_task(task: Task) -> str:
    created = task.created_at.isoformat(timespec="seconds")
    return (
        f"{task.task_id} | {task.title} | {task.status.value} | "
        f"{task.priority.value} | {created} | {task.description}"
    )


def read_line(prompt: str) -> str:
    return input(prompt).strip()


def read_task_id(prompt: str) -> int:
    text = read_line(prompt)
    try:
        return int(text)
    except ValueError as error:
        raise InvalidInputError("Task id must be a whole number.") from error


def print_tasks(tasks: list[Task]) -> None:
    if not tasks:
        print("No tasks.")
        return
    for task in tasks:
        print(format_task(task))


def handle(manager: TaskManager, command: str) -> bool:
    if command == "quit":
        print("Bye")
        return False
    if command == "add":
        title = read_line("Title: ")
        description = read_line("Description: ")
        priority = read_line("Priority (low, medium, high): ")
        task = manager.add_task(title, description, priority)
        print("Added")
        print(format_task(task))
        return True
    if command == "list":
        status_text = read_line("Status filter (blank for all): ")
        priority_text = read_line("Priority filter (blank for all): ")
        status = parse_status(status_text) if status_text else None
        priority = parse_priority(priority_text) if priority_text else None
        print_tasks(manager.list_tasks(status, priority))
        return True
    if command == "update":
        task_id = read_task_id("Task id: ")
        title = read_line("New title (blank to keep): ")
        description = read_line("New description (blank to keep): ")
        status = read_line("New status (blank to keep): ")
        priority = read_line("New priority (blank to keep): ")
        task = manager.update_task(
            task_id,
            title if title else None,
            description if description else None,
            status if status else None,
            priority if priority else None,
        )
        print("Updated")
        print(format_task(task))
        return True
    if command == "delete":
        task_id = read_task_id("Task id: ")
        task = manager.delete_task(task_id)
        print(f"Deleted {task.task_id} {task.title}")
        return True
    if command == "done":
        task_id = read_task_id("Task id: ")
        task = manager.mark_done(task_id)
        print("Marked done")
        print(format_task(task))
        return True
    print("Commands: add, list, update, delete, done, quit")
    return True


def main() -> None:
    path = Path("tasks.json")
    try:
        manager = TaskManager(path)
    except InvalidInputError as error:
        print(error)
        return
    print("Task manager. Commands: add, list, update, delete, done, quit")
    while True:
        try:
            command = read_line("> ").lower()
            should_continue = handle(manager, command)
        except (TaskNotFoundError, InvalidInputError) as error:
            print(error)
            continue
        except KeyboardInterrupt:
            print("\nBye")
            return
        if not should_continue:
            return
