from django.db.models import QuerySet
from django.http.request import HttpRequest
from django.contrib.admin import SimpleListFilter

from apps.projects.models.tasks import Task




class TotalMembersFilter(SimpleListFilter):
    title = "Total members"
    parameter_name = "total_members"

    def lookups(self, request, model_admin):
        return [
            ("single", "1 Member"),
            ("small", "2 to 5 Members"),
            ("medium", "6 to 15 Members"),
            ("big", "16 to 50 Members"),
            ("large", "More than 50 Members"),
        ]

    def queryset(self, request: HttpRequest, queryset: QuerySet[Task]) -> QuerySet[Task] | None:
        value = self.value()
        if value is None:
            return queryset

        if value == "single":
            return queryset.filter(total_members__lte=1)
        if value == "small":
            return queryset.filter(total_members__gt=1, total_members__lte=5)
        if value == "medium":
            return queryset.filter(total_members__gt=5, total_members__lte=15)
        if value == "big":
            return queryset.filter(total_members__gt=15, total_members__lte=50)
        if value == "large":
            return queryset.filter(total_members__gt=50)


class TotalProjectsFilter(SimpleListFilter):
    title = "Total projects"
    parameter_name = "total_projects"

    def lookups(self, request, model_admin):
        return [
            ("single", "1 Project"),
            ("small", "2 to 5 Projects"),
            ("medium", "6 to 15 Projects"),
            ("big", "16 to 50 Projects"),
            ("large", "More than 50 Projects"),
        ]

    def queryset(self, request: HttpRequest, queryset: QuerySet[Task]) -> QuerySet[Task] | None:
        value = self.value()
        if value is None:
            return queryset

        if value == "single":
            return queryset.filter(total_projects__lte=1)
        if value == "small":
            return queryset.filter(total_projects__gt=1, total_projects__lte=5)
        if value == "medium":
            return queryset.filter(total_projects__gt=5, total_projects__lte=15)
        if value == "big":
            return queryset.filter(total_projects__gt=15, total_projects__lte=50)
        if value == "large":
            return queryset.filter(total_projects__gt=50)