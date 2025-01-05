from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from apps.offers.schema import workspace_offer_schema, user_offer_schema
from apps.offers.filters import OfferFilter
from apps.offers.models.offers import Offer
from apps.offers.serializers import offers
from apps.workspace.permissions import IsWorkspaceAdmin


@workspace_offer_schema
class WorkspaceOfferView(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin):
    permission_classes = [IsWorkspaceAdmin]

    http_method_names = ["get", "patch", "post"]
    lookup_url_kwarg = "offer_id"

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    )
    filterset_class = OfferFilter
    search_fields = [
        "user__username",
        "message_text",
    ]
    ordering = "-created_at"

    def get_serializer_class(self):
        if self.action == "create":
            return offers.AdminOfferCreateSerializer
        if self.action == "partial_update":
            return offers.AdminOfferUpdateSerializer
        if self.action == "list":
            return offers.AdminOfferListSerializer

    def get_queryset(self):
        workspace_id = self.kwargs.get("workspace_id")
        return Offer.objects.filter(
            workspace=workspace_id
        ).select_related(
            "workspace",
            "user",
        )


    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        kwargs["context"].update({"workspace_id": self.kwargs.get("workspace_id")})
        return super().get_serializer(*args, **kwargs)


@user_offer_schema
class UserOfferView(GenericViewSet, ListModelMixin, UpdateModelMixin):
    permission_classes = [IsAuthenticated]

    http_method_names = ("get", "patch")
    lookup_url_kwarg = "offer_id"

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    )
    filterset_class = OfferFilter
    search_fields = [
        "workspace__name",
        "message_text",
    ]
    ordering = "-created_at"

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return offers.UserOfferListSerializer
        if self.action == "partial_update":
            return offers.UserOfferUpdateSerializer

        return super().get_serializer_class()

    def get_queryset(self):
        user = self.request.user
        return Offer.objects.filter(
            user=user
        ).select_related(
            "workspace",
            "user",
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_read_by_user = True
        instance.save(update_fields=["is_read_by_user"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
