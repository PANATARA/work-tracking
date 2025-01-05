from dataclasses import dataclass
from django.core.exceptions import ValidationError

from core.services.baseservice import BaseService
from apps.projects.models.tasks import Task
from apps.projects.models.modules import Module


@dataclass
class TransferTasksService(BaseService):
    tasks_ids: list[int]
    module_id: int

    def execute(self) -> str:
        total_transfered_tasks = self.transfer_tasks_between_modules()
        return f"{total_transfered_tasks} tasks were transfered to module"

    def transfer_tasks_between_modules(self) -> int:
        return Task.objects.filter(id__in=self.tasks_ids).update(
            module_id=self.module_id
        )

    def validate(self) -> None:
        module = Module.objects.get(pk=self.module_id)
        if not module:
            raise ValidationError("Module not found")

        for task in self.tasks_ids:
            if not Task.objects.filter(id=task, project=module.project).exists():
                raise ValidationError("Task not found")

        return super().validate()
