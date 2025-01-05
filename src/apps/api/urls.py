from django.urls import path
from rest_framework_simplejwt import views

from apps.api.spectacular.urls import urlpatterns as doc_urls
from apps.api.views import CustomTokenObtainPairView

from apps.users.urls import urlpatterns as user_urls
from apps.workspace.urls import urlpatterns as workspace_urls
from apps.projects.urls import urlpatterns as project_urls
from apps.offers.urls import urlpatterns as offer_urls
from apps.notification.urls import urlpatterns as notification_urls
from apps.activitylog.urls import urlpatterns as log_urls

app_name = 'api'

urlpatterns = [
    path('auth/jwt/create', CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path('auth/jwt/refresh', views.TokenRefreshView.as_view(), name="jwt-refresh"),
    path('auth/jwt/verify', views.TokenVerifyView.as_view(), name="jwt-verify"),
]

urlpatterns += doc_urls
urlpatterns += user_urls
urlpatterns += workspace_urls
urlpatterns += project_urls
urlpatterns += offer_urls
urlpatterns += notification_urls
urlpatterns += log_urls
