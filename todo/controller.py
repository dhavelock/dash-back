from todo.models import TodoList, TodoItem
from todo.serializers import ListSerializer, ItemSerializer

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from todo.sms import sms

class Lists(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        # get request data
        user = request.user
        lists = user.lists

        # create serializer
        listSerializer = ListSerializer(lists, many=True)

        # send response
        response = {
            "lists": listSerializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class List(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        # get request data
        list_id = request.data.get('list', None)
        user = request.user

        # get objects from db
        todolist = get_object_or_404(TodoList, pk=list_id)
        items = todolist.items

        # create serializer
        listSerializer = ListSerializer(todolist)

        # send response
        response = {
            "list": listSerializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        # get request data
        name = request.data.get('name', '')
        user = request.user

        # create object and serializer
        todolist = TodoList.objects.create(name=name, user=user)
        listSerializer = ListSerializer(todolist)

        # send response
        response = {
            "list": listSerializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def delete(self, request):
        # get request data
        list_id = request.data.get('list', None)
        user = request.user

        print('list id', list_id)

        # get list object
        todolist = get_object_or_404(TodoList, pk=list_id)
        print(todolist)
        todolist.delete();

        return Response({"message": "success"}, status=status.HTTP_200_OK)
        

class Item(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    # Get a Todo Item by ID
    def get(self, request):
        # get object and serializer
        item_id = request.data.get('item', None)
        item = get_object_or_404(TodoItem, pk=item_id)
        itemSerializer = ItemSerializer(item)

        # send response
        response = {
            "item": itemSerializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    # Create a new Todo Item
    def post(self, request):
        # get request data
        list_id = request.data.get('list', None)
        todolist = get_object_or_404(TodoList, pk=list_id)
        title = request.data.get('title', '')
        description = request.data.get('description', '')
        deadline = request.data.get('deadline', None)

        # create object and serializer
        todoItem = TodoItem.objects.create(todolist=todolist, title=title, description=description, deadline=deadline)
        itemSerializer = ItemSerializer(todoItem)

        # send response
        response = {
            "item": itemSerializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    # Delete a Todo Item by ID
    def delete(self, request):
        # get request data
        item_pk = request.data.get('id', '')

        # delete object
        todoItem = TodoItem.objects.get(pk=item_pk)
        todolist = todoItem.todolist
        todoItem.delete()

        # create serializer of list w/o item
        listSerializer = ListSerializer(todolist)

        # send response
        response = {
            "list": listSerializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)

class Sms(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        print('SMS')
        request = request.data.dict()
        print(request)

        body = request.get('Body', '')
        cmd = body.split()[0]

        if cmd.lower() == 'add':
            sms.addTodoItem(request)

        elif cmd.lower() == 'list':
            sms.getLists(request)

        return Response({"message": "success"}, status=status.HTTP_200_OK)
