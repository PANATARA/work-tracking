from drf_spectacular.utils import extend_schema, extend_schema_view

task_log_activity = extend_schema_view(

    list=extend_schema(
        tags=["Workspace -> Projects -> Tasks"],
        summary="Task logs", 
    ),
)


user_tasks_logs_activities = extend_schema(
    tags=["User -> Task logs"],
    summary="Gets the all task logs triggered by the current user",
)


user_recent_tasks_logs_activities = extend_schema(
    tags=["User -> Task logs"],
    summary="Gets the most recent 10 task logs triggered by the current user",
)
