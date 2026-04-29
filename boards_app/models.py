from django.conf import settings
from django.db import models
 
 
class Board(models.Model):
    """Repräsentiert ein Kanban-Board mit Mitgliedern und Tasks."""
 
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_boards'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='member_boards',
        blank=True
    )
 
    class Meta:
        verbose_name = 'Board'
        verbose_name_plural = 'Boards'
        ordering = ['name']
 
    def __str__(self):
        return self.name