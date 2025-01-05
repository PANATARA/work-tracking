class ModuleChoice:
    CANCELLED = 0
    PAUSED = 1
    IN_BACKLOG = 2
    PLANNED = 3
    IN_PROGRESS = 4
    COMPLETED = 5

    CHOICES = [
        (IN_BACKLOG, "Backlog"),
        (PLANNED, "Planned"),
        (IN_PROGRESS, "In Progress"),
        (PAUSED, "Paused"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
    ]
