from celery import shared_task
from django.contrib.auth import get_user_model
from django.core import serializers

from apps.activitylog.services.log_creator_m2m import TaskAssigneesLogCreator, TaskTagsLogCreator
from apps.activitylog.services.task_log_creator import TaskLogCreator
from apps.projects.models.tasks import Task

User = get_user_model()


@shared_task
def create_task_log(instance_id, update_fields):
    try:
        instance = Task.objects.get(id=instance_id)
    except Task.DoesNotExist:
        instance = Task.archive_objects.get(id=instance_id)

    tasks_logs = TaskLogCreator(
        task=instance,
        update_fields=update_fields,
    )
    tasks_logs = tasks_logs()
    serializered_logs = serializers.serialize('json', tasks_logs)
    return serializered_logs

@shared_task
def create_task_tags_log(task_id, objects_ids, action):
    try:
        instance = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        instance = Task.archive_objects.get(id=task_id)

    task_log = TaskTagsLogCreator(
        task=instance,
        action=action,
        detailed_information=None,
        objects_ids=objects_ids
    )
    task_log = task_log()
    serializered_logs = serializers.serialize('json', task_log)
    return serializered_logs

@shared_task
def create_task_assignees_log(task_id, objects_ids, action):
    try:
        instance = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        instance = Task.archive_objects.get(id=task_id)

    task_log = TaskAssigneesLogCreator(
        task=instance,
        action=action,
        detailed_information=None,
        objects_ids=objects_ids
    )
    task_log = task_log()
    serializered_logs = serializers.serialize('json', task_log)
    return serializered_logs