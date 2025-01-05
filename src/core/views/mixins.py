# Description: Custom mixins for views.

class BasePermissionByActionView:
    """This mixin allows you to set different permissions for different actions in a view."""
    
    def get_permissions(self):
        # Check for the presence of permission_classes and permission_classes_by_action attributes
        assert hasattr(self, "permission_classes") or hasattr(
            self, "permission_classes_by_action"
        ), (
            '"%s" must include either `permission_classes` or '
            "`permission_classes_by_action`, or override the "
            "`get_permissions()` method." % self.__class__.__name__
        )

        # Safely check for self.permission_classes_by_action and a valid self.action value
        if hasattr(self, "permission_classes_by_action") and hasattr(self, "action"):
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]

        # Use default permission_classes if conditions are not met
        return super().get_permissions()


class BasePermissionByHTTPMethod:
    """This mixin allows you to set different permissions for different HTTP methods in a view."""

    def get_permissions(self):
        # Check for the presence of permission_classes and permission_classes_by_method attributes
        assert hasattr(self, "permission_classes") or hasattr(
            self, "permission_classes_by_method"
        ), (
            '"%s" must include either `permission_classes` or '
            "`permission_classes_by_method`, or override the "
            "`get_permissions()` method." % self.__class__.__name__
        )

        # Safely check for self.permission_classes_by_method and a valid self.method value
        if hasattr(self, "permission_classes_by_method") and hasattr(self.request, "method"):
            return [
                permission()
                for permission in self.permission_classes_by_method.get(self.request.method)
            ]

        # Use default permission_classes if conditions are not met
        return [permission() for permission in getattr(self, "permission_classes", [])]