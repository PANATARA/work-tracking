from dataclasses import dataclass

from core.services.baseservice import BaseService
from apps.offers.models.offers import Offer
from apps.workspace.constant import RoleChoices
from apps.workspace.services.workspace_member import WorkspaceMemberService

@dataclass
class OfferService(BaseService):
    offer: Offer

    def execute(self) -> None:
        pass
    
    @staticmethod
    def generate_message(role: int, message: str|None) -> str:
        if not message:
            role_name = dict(RoleChoices.CHOICES).get(role, 'Unknown')
            message = f"We invite you to join our team for the role {role_name}"
        return message

    @staticmethod
    def add_user_to_workspace_by_offer(offer: Offer) -> None:
        user_with_role = [
            {"user": offer.user, "role": offer.user_role},
        ]
        WorkspaceMemberService(offer.workspace, user_with_role)()
