import django_filters

from apps.offers.constants import STATUS_CHOICES_OFFER
from apps.offers.models import offers


class OfferFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        "status", label="Offer status", choices=STATUS_CHOICES_OFFER
    )

    class Meta:
        model = offers.Offer
        fields = ("status",)