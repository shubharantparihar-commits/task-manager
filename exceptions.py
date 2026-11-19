class TaskNotFoundError(Exception):
    """Raised when no saved task has the requested id."""


class InvalidInputError(Exception):
    """Raised when a title, status, priority, or file is not usable."""
