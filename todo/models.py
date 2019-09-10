from django.db import models

class TodoList(models.Model):
    name = models.CharField(default='', max_length=256, blank=True, null=True)

    def __str__(self):
        return self.name

class TodoItem(models.Model):
    todolist = models.ForeignKey(TodoList, null=True, blank=True, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(default='', max_length=256, blank=True, null=True)
    description = models.CharField(default='', max_length=512, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title