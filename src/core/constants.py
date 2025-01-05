from apps.activitylog.models import TaskActivityLog
from apps.activitylog.serializers import ListTaskLogsSerializer
from apps.projects.models.modules import Module
from apps.projects.models.projects import Project
from apps.projects.models.tasks import Task
from apps.projects.serializers.modules import ModuleShortReadOnlySerializer
from apps.projects.serializers.projects import ProjectShortReadOnlySerializer
from apps.projects.serializers.tasks import TaskShortReadOnlySerializer
from apps.workspace.models.workspace import Workspace
from apps.workspace.serializers.workspace import WorkspaceShortSerializer


def get_entity_model(entity_type):
    entity_map = {
        "workspace": Workspace,
        "project": Project,
        "module": Module,
        "task": Task,
    }
    return entity_map.get(entity_type)

def get_entity_model_and_serializer(entity_type):
    entity_map = {
        "workspace": (Workspace, WorkspaceShortSerializer),
        "project": (Project, ProjectShortReadOnlySerializer),
        "module": (Module, ModuleShortReadOnlySerializer),
        "task": (Task, TaskShortReadOnlySerializer),
        "task_log": (TaskActivityLog, ListTaskLogsSerializer),
    }
    return entity_map.get(entity_type, (None, None))