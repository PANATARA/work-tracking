from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.projects.serializers import projects


project_schema = extend_schema_view(

    list=extend_schema(
        tags=["Workspace -> Projects"],
        summary="User's Project List", 
    ),

    retrieve=extend_schema(
        tags=["Workspace -> Projects"],
        summary="Project Details", 
    ),

    create=extend_schema(
        tags=["Workspace -> Projects"],
        summary="Create Project",
        responses={200: projects.ProjectReadOnlySerializer},
    ),

    partial_update=extend_schema(
        tags=["Workspace -> Projects"],
        summary="Partially Update Project",
        responses={200: projects.ProjectReadOnlySerializer},
    ),

    destroy=extend_schema(
        tags=["Workspace -> Projects"],
        summary="Delete Project", 
    ),

)


module_schema = extend_schema_view(

    list=extend_schema(
        tags=["Workspace -> Projects -> Modules"],
        summary="Project Modules List", 
    ),

    retrieve=extend_schema(
        tags=["Workspace -> Projects -> Modules"],
        summary="Module Details", 
    ),

    create=extend_schema(
        tags=["Workspace -> Projects -> Modules"],
        summary="Create Module", 
    ),

    update=extend_schema(
        tags=["Workspace -> Projects -> Modules"],
        summary="Update Module", 
    ),

    partial_update=extend_schema(
        tags=["Workspace -> Projects -> Modules"],
        summary="Partially Update Module", 
    ),

    destroy=extend_schema(
        summary="Delete Module", 
        tags=["Workspace -> Projects -> Modules"]
    ),
)


task_schema = extend_schema_view(
    list=extend_schema(
        tags=["Workspace -> Projects -> Tasks"],
        summary="Retrieve Task(s)",
        description=(
            "Retrieve a list of tasks within a project or a specific task if task_id is provided."
        ),
    ),
    create=extend_schema(
        tags=["Workspace -> Projects -> Tasks"],
        summary="Create Task",
        description="Create a new task within a specific project.",
    ),
    retrieve=extend_schema(
        tags=["Workspace -> Projects -> Tasks"],
        summary="Retrieve Task",
        description="Retrieve the details of a specific task.",
    ),
    partial_update=extend_schema(
        tags=["Workspace -> Projects -> Tasks"],
        summary="Update Task",
        description="Update details of a specific task.",
    ),
    destroy=extend_schema(
        tags=["Workspace -> Projects -> Tasks"],
        summary="Delete Task",
        description="Delete a specific task within a project.",
        responses={
            204: None,  # No content returned after deletion
        },
    ),
)



archived_task_schema = extend_schema_view(
    get=extend_schema(
        tags=["Workspace -> Projects -> Archived Tasks"],
        summary="Retrieve Task(s)",
        description=(
            "Retrieve a list of tasks within a project or a specific task if task_id is provided."
        ),
    ),
    delete=extend_schema(
        tags=["Workspace -> Projects -> Archived Tasks"],
        summary="Delete Task",
        description="Delete a specific task within a project.",
    ),
)


restore_archived_task = extend_schema(
    tags=["Workspace -> Projects -> Archived Tasks"],
    summary="Restore task from archived",
    description=
"""
- Unarchives the task
- Sets the archiving date to Null
- Sets the and task state date to Null
""",
)


archive_task = extend_schema(
    tags=["Workspace -> Projects -> Archived Tasks"],
    summary="Archive task",
    description=
"""
- Aarchive the task
- Sets the archiving date to current date
""",
)


transfer_task_between_module_schema = extend_schema(
    summary="Transfer tasks between modules", tags=["Workspace -> Projects -> Tasks Utils"]
)


subscribe_user_to_task_schema = extend_schema(
    summary="Subscribe the user to changes in task parameters", tags=["Workspace -> Projects -> Tasks Utils"]
)


unsubscribe_user_to_task_schema = extend_schema(
    summary="Unsubscribe the user to changes in task parameters", tags=["Workspace -> Projects -> Tasks Utils"]
)


dashboard_task = extend_schema_view(
    list=extend_schema(summary="User Task List", tags=["Dashboard"]),
)
