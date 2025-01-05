import json
from celery import shared_task
from django.contrib.auth import get_user_model
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.utils import timezone
from datetime import timedelta

from apps.notification.models.notification import Notification
from apps.notification.services.notification_creator import NotificationCreatorService, TaskAssigneesNotificationService

User = get_user_model()

@shared_task
def send_log_as_notification(json_log, users_ids):
    logs= json.loads(json_log)
    
    if logs and users_ids:
        first_log = logs[0]
        first_field = first_log["fields"]["field"]
        num_fields_changed = len(logs)


        if num_fields_changed == 1:
            message = first_log["fields"]["detail"]
        else:
            message = f"{first_field} and {num_fields_changed - 1} other fields have been changed"

        NotificationCreatorService(
            users=users_ids,
            workspace=first_log["fields"]["workspace"],
            notification_type=1,
            message=message,
            triggered_by=first_log["fields"]["user"],
            entity_type=first_log["model"],
            entity_identifier=first_log["pk"],
        )()
    

@shared_task
def send_notification(
    users_ids,
    workspace_id,
    notification_type,
    triggered_by=None,
    message=None,
    entity_type=None,
    entity_identifier=None,
):

    notification = NotificationCreatorService(
        users=users_ids,
        workspace=workspace_id,
        notification_type=notification_type,
        triggered_by=triggered_by,
        message=message,
        entity_type=entity_type,
        entity_identifier=entity_identifier,
    )
    notification()

@shared_task
def send_task_mention_notification(
    users_ids,
    workspace_id,
    notification_type,
    triggered_by=None,
    message=None,
    entity_type=None,
    entity_identifier=None,
):

    notification = TaskAssigneesNotificationService(
        users=users_ids,
        workspace=workspace_id,
        notification_type=notification_type,
        triggered_by=triggered_by,
        message=message,
        entity_type=entity_type,
        entity_identifier=entity_identifier,
    )
    notification()


def create_task_to_delete_notifications():
    PeriodicTask.objects.create(
        name='Deleting_old_notifications',
        task='deleting_old_notifications',
        interval=IntervalSchedule.objects.get(every=1, period='days'),
        start_time=timezone.now(),
    )

@shared_task(name="deleting_old_notifications")
def deleting_old_notifications():
    """deleting notifications older than 180 days"""

    delta = timezone.now() - timedelta(days=180)
    notifications = Notification.objects.filter(created_at__lte=delta).delete()