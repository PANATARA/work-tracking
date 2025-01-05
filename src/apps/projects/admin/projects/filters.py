from django.db.models import QuerySet
from django.http.request import HttpRequest
from django.contrib.admin import SimpleListFilter

from apps.projects.models.tasks import Task
from apps.workspace.constant import ProjectStateChoices




class ProjectStateFilter(SimpleListFilter):
    title = "State"
    parameter_name = "state"

    def lookups(self, request, model_admin):
        return ProjectStateChoices.CHOICES + [("_", "Without state")]

    def queryset(self, request: HttpRequest, queryset: QuerySet[Task]) -> QuerySet[Task] | None:
        value = self.value()

        if value == "_":
            return queryset.filter(state=None)

        if value:
            return queryset.filter(state__type=value)
