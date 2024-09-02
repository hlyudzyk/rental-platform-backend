from django.db.models import Q
from django.forms import forms
from django.http import JsonResponse

from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from .forms import PropertyForm
from .models import Property, Reservation, Category
from .serializers import PropertiesListSerializer, PropertyDetailSerializer, \
  ReservationsListSerializer, CategorySerializer
from useraccount.models import User
from .filters import PropertyFilter

def get_authenticated_user(request):
  try:
    token = request.META.get('HTTP_AUTHORIZATION', '').split('Bearer ')[1]
    token = AccessToken(token)
    user_id = token.payload.get('user_id')
    return User.objects.get(pk=user_id)
  except (IndexError, KeyError, User.DoesNotExist, AuthenticationFailed):
    return None


def get_favorited_properties(properties, user):
  if not user:
    return []
  return [property.id for property in properties if user in property.favorited.all()]



@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_list(request):
  user = get_authenticated_user(request)
  properties = Property.objects.all()

  filtered_properties = PropertyFilter(properties, request.GET, user).apply_filters()

  favorited = get_favorited_properties(filtered_properties, user)

  serializer = PropertiesListSerializer(filtered_properties, many=True)

  return JsonResponse({
    'data': serializer.data,
    'favorites': favorited
  })


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def categories_list(request):
  categories = Category.objects.all()
  serializer = CategorySerializer(categories,many=True)

  return JsonResponse(serializer.data,safe=False)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def property_detail(request, pk):
  properties = Property.objects.get(pk=pk)
  serializer = PropertyDetailSerializer(properties,many=False)
  return JsonResponse(serializer.data)

@api_view(['POST','FILES'])
def create_property(request):
  form = PropertyForm(request.POST, request.FILES)

  if form.is_valid():
    new_property = form.save(commit=False)
    new_property.host = request.user
    new_property.save()
    return JsonResponse({"success": True})

  else:
    print("Error: ", form.errors, form.non_field_errors)
    return JsonResponse({"errors":form.errors.as_json()}, status=400)


@api_view(['POST'])
def book_property(request, pk):
  try:
    checkin = request.POST.get('checkin','')
    checkout = request.POST.get('checkout','')
    number_of_nights = request.POST.get('number_of_nights','')
    total_price = request.POST.get('total_price','')
    guests = request.POST.get('guests','')

    property_to_reserve = Property.objects.get(pk=pk)

    Reservation.objects.create(
        property=property_to_reserve,
        checkin=checkin,
        checkout=checkout,
        number_of_nights=number_of_nights,
        total_price=total_price,
        guests=guests,
        created_by=request.user,
        status=Reservation.Status.PENDING
    )

    return JsonResponse({"success":True})

  except Exception as e:
    print('Error ', e)
    return JsonResponse({"success":False})


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def property_reservations(request, pk):
  requested_property = Property.objects.get(pk=pk)

  reservations = requested_property.reservations.all()

  serializer = ReservationsListSerializer(reservations,many=True)

  return JsonResponse(serializer.data,safe=False)


@api_view(['POST'])
def mark_favorite(request,pk):
  requested_property = Property.objects.get(pk=pk)

  if request.user in requested_property.favorited.all():
    requested_property.favorited.remove(request.user)
    return JsonResponse({'is_favorite':False})

  else:
    requested_property.favorited.add(request.user)
    return JsonResponse({'is_favorite':True})