from typing import Optional, TypedDict


class NotificationData(TypedDict):
    notification_type: Optional[int] = None
    message: Optional[str] = None
    entity_type: Optional[str] = None
    entity_identifier: Optional[int] = None
