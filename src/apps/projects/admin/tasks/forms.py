from django import forms

from core.admin.forms import ImprovedModelForm
from apps.users.models.users import User
from apps.projects.models.tasks import Task
from apps.projects.models.projects import Project
from apps.workspace.models.workspace_config import TaskState


class TaskAdminForm(ImprovedModelForm):
    class Meta:
        model = Task
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        workspace = kwargs.get("instance").workspace
        self.fields["assignees"].queryset = User.objects.filter(
            workspace_memberships__workspace=workspace
        )
        self.fields["state"].queryset = TaskState.objects.filter(workspace=workspace)
        self.fields["project"].queryset = Project.objects.filter(workspace=workspace)
        self.fields["priority"].widget = forms.Select(choices=[
            (None, "------"),
            (1, 'Low'),
            (2, 'Medium'),
            (3, 'High'),
        ])


class TaskInlineAdminForm(ImprovedModelForm):
    class Meta:
        model = Task
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")
        if instance:
            workspace = instance.workspace
            self.fields["state"].queryset = TaskState.objects.filter(workspace=workspace)