from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.offers.views import WorkspaceOfferView, UserOfferView

router = DefaultRouter()

router.register(r'workspace/(?P<workspace_id>\d+)/offers', WorkspaceOfferView, 'offers')
router.register(r'user/offers', UserOfferView, basename='user-offers')

urlpatterns = [
    path('', include(router.urls)),

]
