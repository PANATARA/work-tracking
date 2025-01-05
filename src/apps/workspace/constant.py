class LayoutChoices:
    LIST = "LIST"
    BOARD = "BOARD"
    CALENDAR = "CALENDAR"
    TABLE = "TABLE"
    TIMELINE = "TIMELINE"

    CHOICES = [
        (LIST, "list"),
        (BOARD, "board"),
        (CALENDAR, "calendar"),
        (TABLE, "table"),
        (TIMELINE, "timeline"),
    ]


class OrderChoices:
    UPDATED_AT = "UPDATED_AT"
    CREATED_AT = "CREATED_AT"
    START_DATE = "START_DATE"
    DEADLINE = "DEADLINE"
    PRIORITY = "PRIORITY"

    CHOICES = [
        (UPDATED_AT, "-updated_at"),
        (CREATED_AT, "-created_at"),
        (START_DATE, "-open_date"),
        (DEADLINE, "-deadline"),
        (PRIORITY, "priority"),
    ]


class GroupChoices:
    STATE = "STATE"
    PRIORITY = "PRIORITY"
    MODULE = "MODULE"
    TAG = "TAG"
    ASSIGNEE = "ASSIGNEE"
    CREATED_BY = "CREATED_BY"

    CHOICES = [
        (STATE, "state"),
        (PRIORITY, "priority"),
        (MODULE, "module"),
        (TAG, "tag"),
        (ASSIGNEE, "assignee"),
        (CREATED_BY, "created_by"),
    ]


class RoleChoices:
    OWNER = 5
    ADMIN = 4
    MANAGER = 3
    MEMBER = 2
    OBSERVER = 1

    CHOICES = [
        (OWNER, "Owner"),
        (ADMIN, "Admin"),
        (MANAGER, "Manager"),
        (MEMBER, "Member"),
        (OBSERVER, "Observer"),
    ]


class ProjectStateChoices:
    DRAFT = 1
    PLANNED = 2
    STARTED = 3
    PAUSED = 4
    DONE = 5
    CANCELLED = 0

    CHOICES = [
        (DRAFT, "Draft"),
        (PLANNED, "Planned"),
        (STARTED, "Started"),
        (PAUSED, "Paused"),
        (DONE, "Done"),
        (CANCELLED, "Cancelled"),
    ]

    DEFAULT_STATE = {
        "Draft": DRAFT,
        "Planned": PLANNED,
        "Started": STARTED,
        "Paused": PAUSED,
        "Done": DONE,
        "Cancelled": CANCELLED,
    }


class TaskStateChoices:
    IN_BACKLOG = 1
    NOT_STARTED = 2
    IN_PROGRESS = 3
    COMPLETED = 4

    CHOICES = [
        (IN_BACKLOG, "In Backlog"),
        (NOT_STARTED, "Unstarted"),
        (IN_PROGRESS, "In Progress"),
        (COMPLETED, "Complete"),
    ]

    DEFAULT_STATE = {
        "In Backlog": IN_BACKLOG,
        "Unstarted": NOT_STARTED,
        "In Progress": IN_PROGRESS,
        "Complete": COMPLETED,
    }


class ArchiveTaskAfterChoices:
    DAYS_1 = 1
    DAYS_3 = 3
    DAYS_7 = 7
    DAYS_14 = 14

    CHOICES = [
        (DAYS_1, "1 day"),
        (DAYS_3, "3 days"),
        (DAYS_7, "7 days"),
        (DAYS_14, "14 days"),
    ]
