from django.urls import include, path
from . import controller

app_name = 'account'

urlpatterns = [
    path('calendar/', controller.Calendar.as_view())
]