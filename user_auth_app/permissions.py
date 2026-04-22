from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Erlaubt nur dem Besitzer (owner) oder einem Admin das Bearbeiten/Löschen.
    Jeder darf die Daten ansehen (GET).
    """
    def has_object_permission(self, request, view, obj):
        # Lesezugriff ist für jeden erlaubt (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Schreibzugriff (PUT, PATCH, DELETE)
        # Prüfe, ob der User Admin ist oder ob ihm das Objekt gehört
        is_owner = bool(obj.owner == request.user)
        is_admin = bool(request.user and request.user.is_superuser)
        
        return is_owner or is_admin