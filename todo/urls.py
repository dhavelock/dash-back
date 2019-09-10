from django.urls import include, path
from . import controller

app_name = 'todo'

urlpatterns = [
    path('list/', controller.List.as_view()),
    path('lists/', controller.Lists.as_view()),
    path('item/', controller.Item.as_view())
]