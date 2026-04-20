from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..models import Task
from .serializers import TaskSerializer

# Listet alle Tasks auf oder erstellt eine neue
class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # permission_classes = [IsAuthenticated] # Später aktivieren für Sicherheit

# Listet nur die Tasks auf, die dem aktuell eingeloggten User gehören
class TasksAssignedToMe(generics.ListAPIView):
    serializer_class = TaskSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assigned_to=user)