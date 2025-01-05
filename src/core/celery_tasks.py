from celery import shared_task

@shared_task
def trace_last_user_request(user_id):
    from django.utils.timezone import now
    from django.contrib.auth import get_user_model
    from django.core.cache import cache

    User = get_user_model()

    try:
        current_time = now()
        user = User.objects.get(pk=user_id)
        user.last_request = current_time
        user.save()
        cache.set(user_id, current_time, timeout=3600)
    except User.DoesNotExist:
        pass

    