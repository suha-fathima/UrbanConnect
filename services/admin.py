from django.contrib import admin
from .models import Service, Booking,Category,Review
from .models import Professional
from .models import Request



admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(Professional)
admin.site.register(Review)
admin.site.register(Request)