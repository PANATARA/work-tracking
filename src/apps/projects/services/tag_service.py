from dataclasses import dataclass

from core.services.baseservice import BaseService
from apps.projects.models.tags import TaskTag


@dataclass
class TagService(BaseService):
    raw_tags: list[str]

    @staticmethod
    def get_tags_entity_by_string(raw_tags: list[str]) -> list[TaskTag]:
        """
        Retrieve or create tags from raw tag names.
        """
        tags = []
        for raw_tag in raw_tags:
            tag_name = raw_tag.strip().lower()
            tag, _ = TaskTag.objects.get_or_create(name=tag_name)
            tags.append(tag)

        return tags
