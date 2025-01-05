from django import forms

from core.admin.forms import ImprovedModelForm
from apps.projects.models.modules import Module
from apps.users.models.users import User
from apps.workspace.models.workspace_config import ProjectState



class ModuleAdminForm(ImprovedModelForm):
    task_count = forms.IntegerField(label="Active task count", required=False)

    class Meta:
        model = Module
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")
        if instance:
            self.initial['task_count'] = instance.tasks.count()
            self.fields['task_count'].widget.attrs['readonly'] = True