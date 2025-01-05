from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.notification.views import NotificationView, SendNotificationView

router = DefaultRouter()

router.register(r'user/notification', NotificationView, 'user-notifications')
router.register(r'workspace/(?P<workspace_id>\d+)/send-notifications', SendNotificationView, 'send-notifications')

urlpatterns = [
    path('', include(router.urls)),

]
