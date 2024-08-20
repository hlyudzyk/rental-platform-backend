from django.forms import forms
from django.http import JsonResponse

from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework_simplejwt.tokens import AccessToken
from .forms import PropertyForm
from .models import Property, Reservation, Category
from .serializers import PropertiesListSerializer, PropertyDetailSerializer, \
  ReservationsListSerializer, CategorySerializer
from useraccount.models import User

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_list(request):
  try:
    token = request.META['HTTP_AUTHORIZATION'].split('Bearer ')[1]
    token = AccessToken(token)
    user_id = token.payload['user_id']
    user = User.objects.get(pk=user_id)

  except Exception as e:
    user = None

  properties = Property.objects.all()
  favorited = []

  is_favorites = request.GET.get('is_favorites','')
  host_id = request.GET.get('host_id','')
  country = request.GET.get('country','')
  category = request.GET.get('category','')
  checkin_date = request.GET.get('checkin_date','')
  checkout_date = request.GET.get('checkout_date','')
  bedrooms = request.GET.get('bedrooms','')
  bathrooms = request.GET.get('bathrooms','')
  guests = request.GET.get('guests','')

  if host_id:
    properties = properties.filter(host_id=host_id)

  if is_favorites:
    properties = properties.filter(favorited__in=[user])

  if checkin_date and checkout_date:
    exact_matches = (Reservation.objects.all().filter(checkin=checkin_date) |
                     Reservation.objects.all().filter(checkout=checkout_date))

    overlap_matches = Reservation.objects.all().filter(checkin__lte=checkout_date,checkout__gte=checkin_date)

    all_matches = []
    for reservation in exact_matches | overlap_matches:
      all_matches.append(reservation.property_id)

    properties = properties.exclude(id__in=all_matches)

  if guests:
    properties = properties.filter(guests__gte=guests)

  if bedrooms:
    properties = properties.filter(bedrooms__gte=bedrooms)

  if bathrooms:
    properties = properties.filter(bathrooms__gte=bathrooms)

  if country:
    properties = properties.filter(country=country)

  if category and category != 'undefined':
    properties = properties.filter(category__slug=category)
  if user:
    for property in properties:
      if user in property.favorited.all():
        favorited.append(property.id)

  serializer = PropertiesListSerializer(properties,many=True)
  return JsonResponse({
    'data':serializer.data,
    'favorites':favorited
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
        created_by=request.user
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