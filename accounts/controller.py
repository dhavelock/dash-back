from accounts.models import Profile

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

class Calendar(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        user = request.user
        calendar_url = user.profile.calendar_url

        return Response({'calendar_url': calendar_url}, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        calendar_url = request.data.get('calendar_url', '')
        user.profile.calendar_url = calendar_url
        user.profile.save()

        return Response({'calendar_url': calendar_url}, status=status.HTTP_200_OK)