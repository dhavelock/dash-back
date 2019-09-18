from django.contrib.auth.models import User
from accounts.models import Profile
from todo.models import TodoList, TodoItem
from todo.serializers import ListSerializer, ItemSerializer

from rest_framework.response import Response
from rest_framework import status

class Sms():
    def getLists(self, sms):
        phone_number = sms.get('From', '')
        phone_number = phone_number[2:] # trim +1 extension
        profile = Profile.objects.get(phone_number=phone_number)
        user = User.objects.get(profile=profile)

        lists = user.lists

        # create serializer
        listSerializer = ListSerializer(lists, many=True)

        # send response
        response = {
            "lists": listSerializer.data
        }

        print("response", response)
        return Response(response, status=status.HTTP_200_OK)

    def addTodoItem(self, sms):

        phone_number = sms.get('From', '')
        phone_number = phone_number[2:] # trim +1 extension
        profile = Profile.objects.get(phone_number=phone_number)
        user = User.objects.get(profile=profile)

        # get args
        body = sms.get('Body', '')
        args = body.split()

        list_name = args[1]
        title = args[2]
        lists = user.lists

        todo_list = None

        for l in lists:
            if l.name == list_name:
                todo_list = l
        
        # create object and serializer
        if todo_list is None:
            return Response({"message": "list not found"}, status=status.HTTP_400_BAD_REQUEST)

        todoItem = TodoItem.objects.create(todolist=todo_list, title=title)
        itemSerializer = ItemSerializer(todoItem)

        # send response
        response = {
            "item": itemSerializer.data
        }
        print("response", response)
        return Response(response, status=status.HTTP_200_OK)

sms = Sms()