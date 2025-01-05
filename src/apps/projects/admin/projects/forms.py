from django import forms

from core.admin.forms import ImprovedModelForm
from apps.users.models.users import User
from apps.projects.models.projects import Project
from apps.workspace.models.workspace_config import ProjectState



class ProjectAdminForm(ImprovedModelForm):
    task_count = forms.IntegerField(label="Active task count", required=False)

    class Meta:
        model = Project
        fields = (
            "name", 
            "manager", 
            "workspace", 
            "description", 
            "state", 
            "date_start", 
            "date_end",
            "task_count",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")
        if instance:
            workspace = instance.workspace

            self.fields["manager"].queryset = User.objects.filter(
                workspace_memberships__workspace=workspace
            )
            self.fields["state"].queryset = ProjectState.objects.filter(workspace=workspace)

            self.initial['task_count'] = instance.tasks.count()
            self.fields['task_count'].widget.attrs['readonly'] = True