from drf_spectacular.utils import extend_schema, extend_schema_view


notification_schema = extend_schema_view(

    list=extend_schema(
        tags=["User -> Notifications"],
        summary="Retrieve User's Notifications",
        description="Fetch a list of all notifications for the current user. This endpoint provides details about each notification, including type, message, and status (read/unread).",
    ),

    retrieve=extend_schema(
        tags=["User -> Notifications"],
        summary="Retrieve Notification Details",
        description="Fetch detailed information about a specific notification. This endpoint returns the notification's full message, timestamp, and any relevant metadata.",
    ),

    destroy=extend_schema(
        tags=["User -> Notifications"],
        summary="Delete Notification",
        description="Permanently delete the specified notification. This action removes the notification from the user's inbox and cannot be undone.",
    ),
)


send_notification_schema = extend_schema_view(

    create=extend_schema(
        tags=["User -> Notifications"],
        summary="Sending notifications to members of the same workspace",
        description="",
    )

)
