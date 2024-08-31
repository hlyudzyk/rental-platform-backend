from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

from .forms import EditUserAccountForm
from .serializers import UserDetailSerializer
from .models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from property.serializers import ReservationsListSerializer

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def host_detail(request,pk):
  user = User.objects.get(pk=pk)
  serializer = UserDetailSerializer(user,many=False)
  return JsonResponse(serializer.data,safe=False)

@api_view(['GET'])
def reservations_list(request):
  reservations = request.user.reservations.all()
  serializer = ReservationsListSerializer(reservations,many=True)
  return JsonResponse(serializer.data,safe=False)

@api_view(['POST','FILES'])
def edit_account(request):
  form = EditUserAccountForm(request.POST, request.FILES)

  if form.is_valid():
    cd = form.cleaned_data
    user = User.objects.get(pk=request.user.id)

    name = cd['name']
    description = cd['description']
    avatar = cd['avatar']

    if name:
      user.name = name

    if description:
      user.description = description

    if avatar:
      user.avatar = avatar

    user.save()

    serializer = UserDetailSerializer(user,many=False)
    return JsonResponse(serializer.data,safe=False)


  return JsonResponse({"errors": form.errors.as_json()}, status=400)

