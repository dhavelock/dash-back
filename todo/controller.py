from todo.models import TodoList, TodoItem
from todo.serializers import ListSerializer, ItemSerializer

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

class Lists(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        # get request data
        user = User.objects.get(username='dylan.havelock@gmail.com') # request.user
        lists = user.lists

        # create serializer
        listSerializer = ListSerializer(lists, many=True)

        # send response
        response = {
            "lists": listSerializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class List(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        # get request data
        list_id = request.data.get('list', None)
        user = User.objects.get(username='dylan.havelock@gmail.com') # request.user

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
        user = User.objects.get(username='dylan.havelock@gmail.com') # request.user

        # create object and serializer
        todolist = TodoList.objects.create(name=name, user=user)
        listSerializer = ListSerializer(todolist)

        # send response
        response = {
            "item": listSerializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
        

class Item(APIView):
    permission_classes = (permissions.AllowAny,)

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

    def post(self, request):
        # get request data
        list_id = request.data.get('list', None)
        todolist = get_object_or_404(TodoList, pk=list_id)
        title = request.data.get('title', '')
        description = request.data.get('description', '')

        # create object and serializer
        todoItem = TodoItem.objects.create(todolist=todolist, title=title, description=description)
        itemSerializer = ItemSerializer(todoItem)

        # send response
        response = {
            "list": itemSerializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

class Sms(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        print('SMS')
        print(request.data)
        return Response(request.data, status=status.HTTP_200_OK)