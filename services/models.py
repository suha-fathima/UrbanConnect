from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)  # 👈 ADD THIS

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Service(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='services/', null=True, blank=True)

    def __str__(self):
        return self.title


from django.contrib.auth.models import User

from django.utils import timezone

class Professional(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    service = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # 🔥 NEW FIELDS
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.0)
    location = models.CharField(max_length=100, default="Udupi")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=500)
    image = models.ImageField(upload_to='professionals/', null=True, blank=True)
    
    availability = models.BooleanField(default=True)  # available or not

    def __str__(self):
        return self.name

class Booking(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    professional = models.ForeignKey(
    Professional,
    on_delete=models.SET_NULL,
    null=True,
    blank=True
)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    

    def __str__(self):
        return f"{self.user.username} - {self.service.title}"



from django.db import models
from django.contrib.auth.models import User

class Request(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Closed', 'Closed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
    

# models.py
from django.db import models

class Review(models.Model):
    name = models.CharField(max_length=100, default="Anonymous")
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)