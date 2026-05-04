from rest_framework import permissions
 
class IsOwnerOrAdmin(permissions.BasePermission):
    """Allow write access only to the object owner or a superuser admin."""
 
    def has_object_permission(self, request, view, obj):
        """Check if user is authenticated, then grant write access only to owner/admin."""
        if not request.user or not request.user.is_authenticated:
            return False
            
        if request.method in permissions.SAFE_METHODS:
            return True
            
        is_owner = getattr(obj, 'owner', None) == request.user
        is_admin = request.user.is_superuser
        
        return is_owner or is_admin