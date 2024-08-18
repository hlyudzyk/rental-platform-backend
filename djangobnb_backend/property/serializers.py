from rest_framework import serializers

from .models import Property, Reservation
from useraccount.serializers import UserDetailSerializer


class PropertiesListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Property
    fields = [
      'id', 'title', 'price_per_night', 'image_url'
    ]

class PropertyDetailSerializer(serializers.ModelSerializer):
  host = UserDetailSerializer(read_only=True,many=False)
  class Meta:
    model = Property
    fields = [
      'id', 'title','description',
      'price_per_night', 'image_url',
      'bathrooms','bedrooms','guests','host'

    ]

class ReservationsListSerializer(serializers.ModelSerializer):

  property = PropertiesListSerializer(read_only=True,many=False)
  class Meta:
    model = Reservation
    fields = (
      'id', 'number_of_nights', 'checkin', 'checkout', 'total_price','property'
    )

