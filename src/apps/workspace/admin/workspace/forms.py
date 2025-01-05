from django import forms

from core.admin.forms import ImprovedModelForm
from apps.users.models.users import User
from apps.projects.models.projects import Project
from apps.workspace.constant import RoleChoices
from apps.workspace.models.workspace import Workspace, WorkspaceMember
from apps.workspace.models.workspace_config import TaskState


class WorkspaceAdminForm(ImprovedModelForm):
    class Meta:
        model = Workspace
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        workspace = kwargs.get("instance")
        self.fields["owner"].queryset = User.objects.filter(
            workspace_memberships__workspace=workspace
        )


class WorkspaceMemberInlineAdminForm(ImprovedModelForm):
    class Meta:
        model = WorkspaceMember
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")
        if instance and instance.role == RoleChoices.OWNER:
            self.fields["role"].widget.attrs.update({
                "disabled": True
            })