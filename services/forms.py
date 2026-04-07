from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['appointment_date']

from django import forms
from .models import Professional

class ProfessionalForm(forms.ModelForm):
    class Meta:
        model = Professional
        fields = '__all__'



from django import forms
from django.contrib.auth.models import User

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']