from rest_framework import serializers

from todo.models import TodoList, TodoItem

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = '__all__'

class ListSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = TodoList
        fields = '__all__'