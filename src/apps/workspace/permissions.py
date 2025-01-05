from functools import wraps
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.workspace.constant import RoleChoices
from apps.workspace.models.workspace import WorkspaceMember


class IsUsersConfig(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsWorkspaceMember(IsAuthenticated):
    def has_permission(self, request, view):
        if "workspace_id" in view.kwargs:
            workspace_id = view.kwargs["workspace_id"]
            self.user = WorkspaceMember.objects.filter(
                workspace_id=workspace_id, user_id=request.user.id
            ).first()
            print("Вызов IsWorkspaceMember")
            return bool(self.user)
        return True


class IsWorkspaceManager(IsWorkspaceMember):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return self.user.role >= RoleChoices.MANAGER


class IsWorkspaceAdmin(IsWorkspaceMember):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        return self.user.role >= RoleChoices.ADMIN
        


class IsWorkspaceOwner(IsWorkspaceMember):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        return self.user.role >= RoleChoices.OWNER
    

def workspace_permission_by_role(member_role: int):

    def decorator(view_func):

        @wraps(view_func)
        def _wrapped_view(instance, request, *args, **kwargs):
            user = request.user
            workspace_id = kwargs.get("workspace_id")

            user_member = WorkspaceMember.objects.filter(
                workspace_id=workspace_id, 
                user_id=user.id,
                role__gte=member_role,
            ).exists()

            if user_member:
                return view_func(instance, request, *args, **kwargs)
            else:
                return Response(
                    data="You do not have permission",
                    status=status.HTTP_403_FORBIDDEN
                )

        return _wrapped_view
        
    return decorator