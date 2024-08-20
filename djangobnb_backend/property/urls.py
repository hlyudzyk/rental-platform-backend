from django.urls import path

from . import api

urlpatterns = [
  path('',api.properties_list,name='api_properties_list'),
  path('categories/',api.categories_list,name='api_categories_list'),
  path('create/',api.create_property,name='api_create_property'),
  path('<uuid:pk>/', api.property_detail, name='api_property_detail'),
  path('<uuid:pk>/book/', api.book_property, name='api_book_property'),
  path('<uuid:pk>/reservations/', api.property_reservations, name='api_property_reservations'),
  path('<uuid:pk>/mark-favorite/', api.mark_favorite, name='api_mark_favorite'),


]