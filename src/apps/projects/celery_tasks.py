from celery import shared_task
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.utils import timezone

from apps.projects.models.tasks import Task

"""Management"""
def create_task_to_archive_completed_tasks():
    PeriodicTask.objects.create(
        name="Archive_completed_tasks",
        task="archive_completed_tasks",
        interval=IntervalSchedule.objects.get(every=10, period="seconds"),
        start_time=timezone.now(),
    )


@shared_task(name="archive_completed_tasks")
def archive_completed_tasks():
    """Archiving completed tasks"""
    current_time = timezone.now()
    Task.objects.filter(
        archive_at__gte=current_time,
        workspace__configuration__archive_completed_task=True,
    ).update(is_archive=True)
"""Management"""


@shared_task
def subscribe_user_task(users_id, task_id):
    from apps.projects.services.tasks_subscribe import SubscribeUserToTaskService

    SubscribeUserToTaskService(users=users_id, task=task_id)()


@shared_task
def unsubscribe_user_task(users_id, task_id):
    from apps.projects.services.tasks_subscribe import UnsubscribeUserToTaskService

    UnsubscribeUserToTaskService(users=users_id, task=task_id)()
