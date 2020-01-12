from django.db import models
from django.contrib.auth.models import User

class TodoList(models.Model):
    user = models.ForeignKey(User, default=None, blank=True, null=True, related_name='lists', on_delete=models.SET_NULL)
    name = models.CharField(default='', max_length=256, blank=True, null=True)

    def __str__(self):
        return self.name

class TodoItem(models.Model):
    todolist = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(default='', max_length=256, blank=True, null=True)
    description = models.CharField(default='', max_length=512, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return self.title