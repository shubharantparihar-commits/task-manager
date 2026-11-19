# Task manager

A command-line task list. Tasks are stored in `tasks.json`.

## Run

From this folder, with the Day 1 virtual environment:

```powershell
C:\Users\Shubharant\Desktop\Python\Day1_3\.venv1\Scripts\python.exe main.py
```

Commands: `add`, `list`, `update`, `delete`, `done`, `quit`.

`list` asks for an optional status (`todo`, `in_progress`, `done`) and an optional priority (`low`, `medium`, `high`). Leave either one blank to skip that filter. Results are sorted by creation time, oldest first.

A missing task id prints an error and returns to the prompt. A bad status, priority, or damaged `tasks.json` does the same.
