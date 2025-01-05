from rest_framework.exceptions import ValidationError


class TaskUtils:

    @staticmethod
    def transfer_tasks_between_modules(new_module, old_module, tasks=None):
        """
        This method transfers tasks from one module
        to another module of the same project
        """
        if old_module.project == new_module.project:
            if not tasks:
                tasks = old_module.task.all()

            for task in tasks:
                task.module = new_module
                task.save()

            return tasks
        else:
            raise ValidationError("These modules do not belong to the same project")
