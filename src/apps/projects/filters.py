import django_filters

from apps.projects.models import projects, tasks


class ProjectFilter(django_filters.FilterSet):
    user_is_author = django_filters.BooleanFilter(
        "user_is_author", label="The user is the author"
    )

    user_is_manager = django_filters.BooleanFilter(
        "user_is_manager", label="The user is the manager"
    )

    class Meta:
        model = projects.Project
        fields = (
            "user_is_author",
            "user_is_manager",
            "state",
        )


class BaseTaskFilter(django_filters.FilterSet):

    tags = django_filters.CharFilter(
        "tags__name", method="filter_tags", label="Tags", distinct=True
    )

    class Meta:
        model = tasks.Task
        fields = ("tags", "state", "module", "priority", "created_by")

    def filter_tags(self, queryset, name, value):
        tags = value.split(",")

        return queryset.filter(tags__name__in=tags)


class DashboardTaskFilter(BaseTaskFilter):

    class Meta(BaseTaskFilter.Meta):
        fields = BaseTaskFilter.Meta.fields + ("project",)


class TaskFilter(BaseTaskFilter):

    assignees = django_filters.BooleanFilter(
        "user_permormer", method="is_user_performer", label="Is user performer"
    )

    class Meta(BaseTaskFilter.Meta):
        fields = BaseTaskFilter.Meta.fields + ("assignees",)

    def is_user_performer(self, queryset, name, value):
        user = self.request.user

        return (
            queryset.filter(assignees=user)
            if value
            else queryset.exclude(assignees=user)
        )
