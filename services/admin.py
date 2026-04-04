from django.contrib import admin
from .models import Service, Booking,Category
from .models import Professional

admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(Professional)
