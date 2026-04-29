from rest_framework import permissions


class IsBoardMember(permissions.BasePermission):
    """
    Prüft ob der User Mitglied (oder Owner) des Boards ist,
    zu dem die Task gehört. Wird bei POST auf /api/tasks/ genutzt.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        board_id = request.data.get('board')
        if not board_id:
            return False

        from boards_app.models import Board
        try:
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            return False

        is_owner = board.owner == request.user
        is_member = board.members.filter(id=request.user.id).exists()
        return is_owner or is_member


class IsTaskOwnerOrBoardOwner(permissions.BasePermission):
    """
    Für DELETE auf eine einzelne Task:
    Nur der Task-Ersteller (owner) oder der Board-Owner darf löschen.
    Für PUT/PATCH: Jedes Board-Mitglied darf bearbeiten.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ('PUT', 'PATCH'):
            board = obj.board
            is_board_owner = board.owner == request.user
            is_member = board.members.filter(id=request.user.id).exists()
            return is_board_owner or is_member

        if request.method == 'DELETE':
            is_task_owner = obj.owner == request.user
            is_board_owner = obj.board.owner == request.user
            return is_task_owner or is_board_owner

        return False


class IsCommentAuthor(permissions.BasePermission):
    """
    Für DELETE auf einen Kommentar:
    Nur der Autor des Kommentars darf ihn löschen.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
