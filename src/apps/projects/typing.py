from datetime import datetime
from typing import Optional, TypedDict

from apps.projects.models.modules import Module
from apps.projects.models.tags import TaskTag
from apps.users.models.users import User
from apps.workspace.models.workspace_config import ProjectState, TaskState


class ProjectData(TypedDict):
    name: Optional[str] = "Project"
    description: Optional[str] = None
    manager: Optional[int | User] = None
    state: Optional[int | ProjectState] = None
    date_start: Optional[datetime] = None
    date_end: Optional[datetime] = None


class TaskData(TypedDict):
    title: Optional[str] = "Task"
    description: Optional[str] = None
    priority: Optional[int] = None
    deadline: Optional[datetime] = None
    state_id: Optional[int | TaskState] = None
    module_id: Optional[int | Module] = None
    assignees: Optional[int | User] = []
    tags: Optional[str | int | TaskTag] = []
