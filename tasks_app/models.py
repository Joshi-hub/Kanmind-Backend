from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    # Definition der Auswahlmöglichkeiten
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('inprogress', 'In Progress'),
        ('awaitfeedback', 'Await Feedback'),
        ('done', 'Done'),
    ]
    CATEGORY_CHOICES = [
        ('userstory', 'User Story'),
        ('technical', 'Technical'),
        ('marketing', 'Marketing'),
        ('design', 'Design'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='userstory')
    
    # Wer hat die Aufgabe erstellt?
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    # Wem ist sie zugewiesen? (Mehrere Personen möglich)
    assigned_to = models.ManyToManyField(User, related_name='assigned_tasks', blank=True)

    def __str__(self):
        return self.title

class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=200)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task.title} - {self.title}"
