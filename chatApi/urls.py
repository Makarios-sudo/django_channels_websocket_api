from django.urls import path
from .views import UserDetailAPI,RegisterUserAPIView,UserList
from . import views



urlpatterns = [
    path('register',RegisterUserAPIView.as_view()),

    path("get-details",UserDetailAPI.as_view()),
    path("users", UserList.as_view(), name="user_list"),
    path("new_chat", views.send_message, name="new_chat"),
    path("all_chat", views.get_messages, name="all_chats"),
    path("chat/<str:id>/", views.get_message, name="chats")

]