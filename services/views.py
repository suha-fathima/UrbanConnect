from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Service, Booking,Category
from .forms import BookingForm
from decimal import Decimal
from datetime import datetime
from datetime import date
from django.contrib import messages   # add at top of file
from django.db.models import Q
from .models import Service, Category
from .models import Professional
from django.shortcuts import render
from .models import Request
@login_required
def home(request):
    query = request.GET.get('q')

    services = Service.objects.all()
    categories = Category.objects.all()
    professionals = Professional.objects.all()  # ⭐ ADD THIS

    if query:
        services = Service.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

        categories = Category.objects.filter(
            name__icontains=query
        )

        professionals = Professional.objects.filter(
    Q(name__icontains=query) |
    Q(category__name__icontains=query)
)

    return render(request, 'services/home.html', {
        'services': services,
        'categories': categories,
        'professionals': professionals,   # ⭐ ADD THIS
        'query': query
    })

@login_required
def service_list(request):
    services = Service.objects.all()
    return render(request, 'services/service_list.html', {'services': services})

@login_required(login_url='/accounts/login/')
# def book_service(request, service_id):
#     service = get_object_or_404(Service, id=service_id)

#     if request.method == "POST":
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             booking = form.save(commit=False)
#             booking.user = request.user
#             booking.service = service
#             booking.save()
#             return redirect('dashboard')
#     else:
#         form = BookingForm()

#     return render(request, 'services/book_service.html', {
#         'form': form,
#         'service': service
#     })

def book_service(request, service_id):
    cart = request.session.get('cart', [])

    service_id = int(service_id)
    cart = request.session.get('cart', [])

    if service_id not in cart:
        cart.append(service_id)

    request.session['cart'] = cart
    messages.success(request, "Service added to cart 🛒")

    return redirect('dashboard')


@login_required
def checkout(request):
    if request.method == "POST":
        cart = request.session.get('cart', [])
        services = Service.objects.filter(id__in=cart)

        for i, service_id in enumerate(cart, start=1):
            service_id = request.POST.get(f"service_id_{i}")
            service = Service.objects.get(id=service_id)
            pro_id = request.POST.get(f"professional_{i}")
            professional = None
            if pro_id:
                try:
                    professional = Professional.objects.get(id=pro_id)
                except Professional.DoesNotExist:
                    professional = None

            date_value = request.POST.get(f"date_{i}")
            time_value = request.POST.get(f"time_{i}")
            

            if date_value and time_value:
                date_obj = datetime.strptime(date_value, "%Y-%m-%d").date()
                time_obj = datetime.strptime(time_value, "%H:%M").time()
                if not Booking.objects.filter(
                    user=request.user,
                    service=service,
                    appointment_date=date_obj,
                    appointment_time=time_obj
                    ).exists():
                    Booking.objects.create(
            user=request.user,
            service=service,
            professional=professional, 
            appointment_date=date_obj,
            appointment_time=time_obj,
            status="Pending"
        )

        request.session['cart'] = []
        return redirect('payment')

    return redirect('dashboard')

from django.contrib.auth.decorators import login_required
from .models import Booking


@login_required

def dashboard(request):
    cart = request.session.get('cart', [])

    services = Service.objects.filter(id__in=cart)
    professionals = Professional.objects.all()  

    subtotal = sum([s.price for s in services], Decimal('0.00'))
    tax = (subtotal * Decimal('0.10')).quantize(Decimal('0.01'))
    total = subtotal + tax

    return render(request, "services/dashboard.html", {
        "services": services,
        "subtotal": subtotal,
        "tax": tax,
        "total": total,
        "professionals": professionals, 
    })



from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            messages.success(request, "Account created! Please login.") 
            return redirect('login')

    return render(request, "services/signup.html")

from django.contrib.auth import login, authenticate

from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # <-- redirect after login
    else:
        form = AuthenticationForm()
    return render(request, 'services/login.html', {'form': form})


from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully 👋")
    return redirect('login')


from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

@login_required
def payment(request):
    if request.method == "POST":
        payment_method = request.POST.get("payment_method")

        # Get all pending bookings
        bookings = Booking.objects.filter(user=request.user, status="Pending")

        for booking in bookings:
            booking.status = "Confirmed"
            booking.save()

        # ✅ ADD THIS PART (SUCCESS MESSAGES)
        if payment_method == "cod":
            messages.success(request, "Order placed successfully with Cash on Delivery! 💵")

        elif payment_method == "card":
            messages.success(request, "Payment successful via Card! 💳")

        elif payment_method == "upi":
            messages.success(request, "Payment successful via UPI! 📱")

        else:
            messages.success(request, "Payment successful! 🎉")

        return redirect('my_bookings')
    return render(request, "services/payment.html")


from django.contrib.auth.decorators import login_required

from decimal import Decimal   # ✅ ADD THIS

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-id')

    for booking in bookings:
        price = booking.service.price
        tax = price * Decimal('0.10')   # ✅ FIXED
        booking.tax = tax
        booking.total_price = price + tax

    return render(request, "services/my_bookings.html", {
        "bookings": bookings
    })

from django.shortcuts import render, get_object_or_404
from .models import Category, Service

def services_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    services = Service.objects.filter(category=category)

    return render(request, 'services/services_by_category.html', {
        'category': category,
        'services': services
    })

from .models import Category, Service



def all_services(request):
    services = Service.objects.all()
    return render(request, 'services/all_services.html', {'services': services})

from django.contrib.auth import logout
from django.shortcuts import redirect



from .forms import ProfessionalForm

def register_professional(request):
    if request.method == 'POST':
        form = ProfessionalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'services/pro_success.html')  # redirect after submit
    else:
        form = ProfessionalForm()

    return render(request, 'services/register_professional.html', {'form': form})



def pro_success(request):
    return render(request, 'services/pro_success.html')



def about(request):
    return render(request, 'services/about.html')


from django.shortcuts import redirect
from django.contrib import messages
@login_required
def delete_service(request, id):
    if request.method == "POST":
        cart = request.session.get('cart', [])

        if id in cart:
            cart.remove(id)
            request.session['cart'] = cart
            messages.success(request, "Service removed from cart 🗑️")

    return redirect('my_bookings')


def investors(request):
    return render(request, 'footer/investors.html')

def terms(request):
    return render(request, 'footer/terms.html')

def privacy(request):
    return render(request, 'footer/privacy.html')

def anti_discrimination(request):
    return render(request, 'footer/anti_discrimination.html')

def reviews(request):
    return render(request, 'footer/reviews.html')

def categories(request):
    categories = Category.objects.all()
    return render(request, 'footer/categories.html', {
        'categories': categories
    })

def contact(request):
    return render(request, 'footer/contact.html')

from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, "services/profile.html")


from django.http import JsonResponse
import json
from .models import ChatMessage
from django.contrib.auth.models import User

def send_message(request):
    data = json.loads(request.body)

    receiver = User.objects.get(username=data['professional'])

    ChatMessage.objects.create(
        sender=request.user,
        receiver=receiver,
        message=data['message']
    )

    return JsonResponse({"status": "ok"})


def get_messages(request):
    pro = request.GET.get("professional")

    receiver = User.objects.get(username=pro)

    messages = ChatMessage.objects.filter(
        sender__in=[request.user, receiver],
        receiver__in=[request.user, receiver]
    ).order_by("timestamp")

    data = []

    for m in messages:
        data.append({
            "text": m.message,
            "sender": "user" if m.sender == request.user else "pro"
        })

    return JsonResponse({"messages": data})



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # redirect back to profile page
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'services/edit_profile.html', {'form': form})


def my_requests(request):
    user_requests = Request.objects.filter(user=request.user)
    return render(request, 'services/my_requests.html', {'requests': user_requests})