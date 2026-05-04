from rest_framework import permissions
 
class IsOwnerOrAdmin(permissions.BasePermission):
    """Allow write access only to the object owner or a superuser admin."""
 
    def has_object_permission(self, request, view, obj):
        """Grant read access to all; write access only to owner or admin."""
        
        if request.method in permissions.SAFE_METHODS:
            return True
        is_owner = obj.owner == request.user
        is_admin = request.user and request.user.is_superuser
        return is_owner or is_admin