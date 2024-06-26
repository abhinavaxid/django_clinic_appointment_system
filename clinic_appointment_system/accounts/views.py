from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from .models import Appointment, Patient
from django.contrib.auth import logout
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        gender = request.POST['gender']
        dob = request.POST['dob']
        age = request.POST['age']
        address = request.POST['address']
        contact_number = request.POST['contact_number']
        email = request.POST['email']

        user = User.objects.create_user(username=email, password='Change@123', email=email, first_name=first_name, last_name=last_name)
        user.save()

        patient = Patient(user=user, gender=gender, dob=dob, age=age, address=address, contact_number=contact_number)
        patient.save()

        send_mail(
    'Welcome to Clinic Appointment System',
    f'Your username is {email} and your password is Change@123',
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
)

        messages.success(request, 'Signup successful! Check your email for login details.')
        return redirect('login')

    return render(request, 'signup.html')



def login_view(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
        except MultiValueDictKeyError:
            return HttpResponse('Please enter both username and password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Invalid credentials')

    return render(request, 'login.html')

@login_required
def home(request):
    user = request.user
    appointments = Appointment.objects.filter(user=user).order_by('appointment_date')
    total_bookings = appointments.count()
    next_booking = appointments.first().appointment_date if total_bookings > 0 else None

    patient = Patient.objects.get(user=request.user)

    if request.method == 'POST':
        appointment_date = request.POST['appointment_date']
        appointment_time = request.POST['appointment_time']
        doctor_name = request.POST['doctor_name']
        purpose = request.POST['purpose']
        
        Appointment.objects.create(
            user=request.user,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            doctor_name=doctor_name,
            purpose=purpose
        )
        messages.success(request, 'Appointment booked successfully!')
        return JsonResponse({'success': True})

    context = {
        'total_bookings': total_bookings,
        'next_booking': next_booking,
        'first_name': patient.user.first_name,
        'last_name': patient.user.last_name,
        'gender': patient.gender,
        'dob': patient.dob,
        'age': patient.age,
        'appointments': appointments, 
    }
    return render(request, 'home.html', context)




@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(user=request.user).order_by('appointment_date')
    return render(request, 'my_appointments.html', {'appointments': appointments})


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def clinic_appointments(request):
    if not request.user.is_staff: 
        return redirect('home')

    appointments = Appointment.objects.all().order_by('appointment_date', 'appointment_time')
    doctor_names = Appointment.objects.values_list('doctor_name', flat=True).distinct()

    if request.method == 'POST':
        appointment_date = request.POST.get('appointment_date')
        doctor_name = request.POST.get('doctor_name')

        if appointment_date:
            appointments = appointments.filter(appointment_date=appointment_date)
        if doctor_name:
            appointments = appointments.filter(doctor_name=doctor_name)

    context = {
        'appointments': appointments,
        'doctor_names': doctor_names,
    }
    return render(request, 'clinic_appointments.html', context)