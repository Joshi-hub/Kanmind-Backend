from rest_framework import permissions
from rest_framework.exceptions import NotFound 

class IsBoardMember(permissions.BasePermission):
    """Allow POST on /api/tasks/ only for members or owners of the target board."""

    def has_permission(self, request, view):
        """Return True if the user is a board member or owner."""
        if request.method in permissions.SAFE_METHODS:
            return True            
        board_id = request.data.get('board')
        if not board_id:
            return False            
        from boards_app.models import Board
        try:
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            raise NotFound(detail="Board not found.")            
        return board.owner == request.user or board.members.filter(id=request.user.id).exists()


class IsTaskOwnerOrBoardOwner(permissions.BasePermission):
    """Allow DELETE only for task owner or board owner; PATCH for any board member."""

    def has_object_permission(self, request, view, obj):
        """Check object-level permission based on HTTP method."""
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in ('PUT', 'PATCH'):
            board = obj.board
            return board.owner == request.user or board.members.filter(id=request.user.id).exists()
        if request.method == 'DELETE':
            return obj.owner == request.user or obj.board.owner == request.user
        return False


class IsBoardMemberForComment(permissions.BasePermission):
    """Allow access to task comments only for members or owners of the task's board."""

    def has_permission(self, request, view):
        """Return 403 if the user is not a member of the board the task belongs to."""
        from tasks_app.models import Task
        task_id = view.kwargs.get('task_id')
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return True  # Let the view return 404
        board = task.board
        return board.owner == request.user or board.members.filter(id=request.user.id).exists()


class IsCommentAuthor(permissions.BasePermission):
    """Allow DELETE on a comment only for its author."""

    def has_object_permission(self, request, view, obj):
        """Return True only if the requesting user authored the comment."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user