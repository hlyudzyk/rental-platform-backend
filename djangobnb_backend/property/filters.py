from django.db.models import Q

from .models import Reservation


class PropertyFilter:
  def __init__(self, queryset, params, user=None):
    self.queryset = queryset
    self.params = params
    self.user = user

  def filter_by_host(self):
    host_id = self.params.get('host_id')
    if host_id:
      self.queryset = self.queryset.filter(host_id=host_id)
    return self

  def filter_by_favorites(self):
    is_favorites = self.params.get('is_favorites')
    if is_favorites and self.user:
      self.queryset = self.queryset.filter(favorited__in=[self.user])
    return self

  def filter_by_availability(self):
    checkin_date = self.params.get('checkin_date')
    checkout_date = self.params.get('checkout_date')
    if checkin_date and checkout_date:
      exact_matches = (Reservation.objects.filter(checkin=checkin_date) |
                       Reservation.objects.filter(checkout=checkout_date))

      overlap_matches = Reservation.objects.filter(
        Q(checkin__lte=checkout_date) & Q(checkout__gte=checkin_date)
      )

      all_matches = exact_matches | overlap_matches
      self.queryset = self.queryset.exclude(id__in=[res.property_id for res in all_matches])
    return self

  def filter_by_guests(self):
    guests = self.params.get('guests')
    if guests:
      self.queryset = self.queryset.filter(guests__gte=guests)
    return self

  def filter_by_bedrooms(self):
    bedrooms = self.params.get('bedrooms')
    if bedrooms:
      self.queryset = self.queryset.filter(bedrooms__gte=bedrooms)
    return self

  def filter_by_bathrooms(self):
    bathrooms = self.params.get('bathrooms')
    if bathrooms:
      self.queryset = self.queryset.filter(bathrooms__gte=bathrooms)
    return self

  def filter_by_country(self):
    country = self.params.get('country')
    if country:
      self.queryset = self.queryset.filter(country=country)
    return self

  def filter_by_category(self):
    category = self.params.get('category')
    if category and category != 'undefined':
      self.queryset = self.queryset.filter(category__slug=category)
    return self

  def apply_filters(self):
    return (self.filter_by_host()
            .filter_by_favorites()
            .filter_by_availability()
            .filter_by_guests()
            .filter_by_bedrooms()
            .filter_by_bathrooms()
            .filter_by_country()
            .filter_by_category()
            .queryset)

