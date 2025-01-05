from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from celery import chain

from apps.projects.models.tasks import Task
from apps.projects.services.tasks_subscribe import SubscribeUserToTaskService
from apps.projects.celery_tasks import subscribe_user_task, unsubscribe_user_task
from apps.notification.celery_tasks import send_log_as_notification, send_task_mention_notification
from apps.activitylog.celery_tasks import (
    create_task_assignees_log,
    create_task_log,
    create_task_tags_log,
)


@receiver(post_save, sender=Task)
def task_field_changed(sender, instance, created, **kwargs):
    """Log entry about field changes"""

    update_fields = kwargs.get("update_fields", None)
    if not created and update_fields is not None:

        users_to_get_notify = SubscribeUserToTaskService.list_users_to_get_notify(
            task=instance
        )

        task_chain = chain(
            create_task_log.s(instance.id, list(update_fields)),
            send_log_as_notification.s(users_to_get_notify),
        )

        task_chain()


@receiver(m2m_changed, sender=Task.assignees.through)
def task_assignees_changed_signal(sender, instance, action, **kwargs):
    assignees_ids = kwargs.get("pk_set", [])

    if assignees_ids and action in ["post_remove", "post_add"]:

        users_to_get_notify = SubscribeUserToTaskService.list_users_to_get_notify(
            task=instance
        )

        if action == "post_add":

            # Subscribe user, and send mention notification

            subscribe_user_task.delay(list(assignees_ids), instance.id),
            send_task_mention_notification.delay(
                users_ids=list(assignees_ids),
                workspace_id=instance.workspace.id,
                notification_type=1,
                triggered_by=instance.updated_by.id,
                message="You have been added to the task assignees",
                entity_type=instance._meta.model_name,
                entity_identifier=instance.id,
            )

        if action == "post_remove":

            # Unsubscribe user
            unsubscribe_user_task.delay(list(assignees_ids), instance.id)

        # Create and send Log for task
        task_chain = chain(
            create_task_assignees_log.s(instance.id, list(assignees_ids), action),
            send_log_as_notification.s(users_to_get_notify),
        )
        task_chain()


@receiver(m2m_changed, sender=Task.tags.through)
def tags_changed(sender, instance, action, **kwargs):
    """Log entry about tags changes"""

    tags_ids = kwargs.get("pk_set", [])
    if tags_ids and action in ["post_remove", "post_add"]:

        users_to_get_notify = SubscribeUserToTaskService.list_users_to_get_notify(
            task=instance
        )

        # Create and send Log for task
        task_chain = chain(
            create_task_tags_log.s(instance.id, list(tags_ids), action),
            send_log_as_notification.s(users_to_get_notify),
        )
        task_chain()
