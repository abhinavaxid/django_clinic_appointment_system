from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),  # Add this line
    path('logout/', views.logout_view, name='logout'),
    path('clinic_appointments/', views.clinic_appointments, name='clinic_appointments'),
]
