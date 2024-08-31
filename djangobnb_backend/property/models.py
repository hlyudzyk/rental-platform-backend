import uuid

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify

from useraccount.models import User


class Category(models.Model):
  id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
  name = models.CharField(max_length=100)
  slug = models.SlugField(max_length=100, unique=True,blank=True)
  image = models.ImageField(upload_to='uploads/categories')

  def image_url(self):
    return f'{settings.WEBSITE_URL}{self.image.url}'

  def __str__(self):
    return self.name


  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.name)
    super().save(*args, **kwargs)


class Property(models.Model):
  id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
  title = models.CharField(max_length=255)
  description = models.TextField()
  price_per_night = models.IntegerField()
  bedrooms = models.IntegerField()
  bathrooms = models.IntegerField()
  guests = models.IntegerField()
  country = models.CharField(max_length=255)
  country_code = models.CharField(max_length=18)
  category = models.ForeignKey(Category,related_name='properties',on_delete=models.CASCADE)
  favorited = models.ManyToManyField(User,related_name='favorites',blank=True)
  image = models.ImageField(upload_to='uploads/properties')
  host = models.ForeignKey(User,related_name='properties',on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)

  def image_url(self):
    return f'{settings.WEBSITE_URL}{self.image.url}'


class Reservation(models.Model):
  id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
  property = models.ForeignKey(Property,related_name='reservations',on_delete=models.CASCADE)
  checkin = models.DateField()
  checkout = models.DateField()
  number_of_nights = models.IntegerField()
  guests = models.IntegerField()
  total_price = models.FloatField()
  created_by = models.ForeignKey(User,related_name='reservations',on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)

