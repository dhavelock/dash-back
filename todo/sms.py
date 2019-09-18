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
        user = profile.user

        # get args
        body = sms.get('Body', '')
        args = body.split()
        cmd = args[0]
        list_name = args[1]
        title = body[len(cmd) + len(list_name) + 2:] 

        # get the user's lists
        lists = user.lists
        listSerializer = ListSerializer(lists, many=True)

        todo_list_pk = None

        # get list pk from the user's lists
        for l in listSerializer.data:
            if l['name'].lower() == list_name.lower():
                todo_list_pk = l['id']
        
        # check if list exists
        if todo_list_pk is None:
            return Response({"message": "list not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the todo item
        todo_list = TodoList.objects.get(pk=todo_list_pk)
        todoItem = TodoItem.objects.create(todolist=todo_list, title=title)
        itemSerializer = ItemSerializer(todoItem)

        # send response
        response = {
            "item": itemSerializer.data
        }
        print("response", response)
        return Response(response, status=status.HTTP_200_OK)

sms = Sms()