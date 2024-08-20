from django.contrib import admin
from .models import Property,Reservation,Category

admin.site.register(Property)
admin.site.register(Reservation)
admin.site.register(Category)