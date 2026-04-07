from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
     path('accounts/login/',auth_views.LoginView.as_view(
            template_name='services/login.html'),name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home, name='home'),
    path('book/<int:service_id>/', views.book_service, name='book_service'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('services/<slug:slug>/', views.services_by_category, name='services_by_category'),
    path('services/', views.all_services, name='all_services'),
    path('register-professional/', views.register_professional, name='register_professional'),
    path('pro-success/', views.pro_success, name='pro_success'),
     path('about/', views.about, name='about'),
     path('delete-service/<int:id>/', views.delete_service, name='delete_service'),
    path('investors/', views.investors, name='investors'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('anti-discrimination/', views.anti_discrimination, name='anti_discrimination'),
    
    path('reviews/', views.reviews, name='reviews'),
    path('categories/', views.categories, name='categories'),
    path('contact/', views.contact, name='contact'),
    path('category/<slug:slug>/', views.services_by_category, name='services_by_category'),
    path('profile/', views.profile, name='profile'),

     path('forgot-password/', 
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset.html'
         ), 
         name='password_reset'),

    path('forgot-password/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ), 
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),

    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
         path('edit-profile/', views.edit_profile, name='edit_profile'),
         path('password_change/', auth_views.PasswordChangeView.as_view(template_name='services/change_password.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='services/change_password_done.html'), name='password_change_done'),
   
    path('my-requests/', views.my_requests, name='my_requests'),
      path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='services/login.html'), name='login'),


]


