from typing import Any

from django.db.models import QuerySet
from django.http.request import HttpRequest

from apps.projects.models.tasks import Task
from django.contrib.admin import SimpleListFilter


from apps.workspace.constant import TaskStateChoices


class TaskStateFilter(SimpleListFilter):
    title = "State"
    parameter_name = "state"

    def lookups(self, request, model_admin):
        return TaskStateChoices.CHOICES + [("_", "Without state")]

    def queryset(self, request: HttpRequest, queryset: QuerySet[Task]) -> QuerySet[Task] | None:
        value = self.value()

        if value == "_":
            return queryset.filter(state=None)

        if value:
            return queryset.filter(state__type=value)


class TaskPriorityFilter(SimpleListFilter):
    title = "Priority"
    parameter_name = "priority"

    def lookups(self, request, model_admin):
        return [
            (1, "Low"),
            (2, "Medium"),
            (3, "High"),
            ("_", "Without priority")
        ]

    def queryset(self, request: HttpRequest, queryset: QuerySet[Task]) -> QuerySet[Task] | None:
        value = self.value()

        if value == "_":
            return queryset.filter(priority=None)

        if value:
            return queryset.filter(priority=value)
