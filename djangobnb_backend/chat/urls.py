from django.urls import path
from . import api

urlpatterns = [
  path('',api.conversations_list,name="api_conversations_list"),
  path('<uuid:pk>/',api.conversation_detail,name="api_conversation_detail"),
  path('start/<uuid:user_id>/',api.start_conversation,name="api_start_conversation")
]