# django_clinic_appointment_system
## Project Overview

The Clinic Appointment System is a web application developed using Python Django framework. It allows patients to register, book appointments, and manage their appointments online. Clinic staff can view and manage patient appointments through a secure interface.

## Project Architecture

### Components

- **Models**: Define database schema and relationships.
- **Views**: Handle user interface logic and rendering templates.
- **Templates**: HTML files with Django template language.
- **Forms**: Django forms for data validation.
- **URLs**: Define URL patterns to map to views.
- **Settings**: Configuration settings including database settings, email configurations, etc.

### Setup Instructions

#### Clone the Repository
git clone https://github.com/abhinavaxid/django_clinic_appointment_system <br>

### Install Dependencies <br>
pip install -r requirements.txt

### Start server
run the command
python manage.py runserver

### Email Configuration
Configure email settings in settings.py for sending signup notifications.<br>

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' <br>
EMAIL_HOST = 'smtp.gmail.com' <br>
EMAIL_PORT = 587 <br>
EMAIL_USE_TLS = True <br>
EMAIL_HOST_USER = 'example@gmail.com' <br>
EMAIL_HOST_PASSWORD = 'gmailAppPassword' <br>

Replace the 'example@gmail.com' with your email and 'gmailAppPassword' with the actual 16 character app password.<br>
You can generate the the app password at the your google account settings. <br>

###For staff login
To view as a clinic user, create a super user <br>
python manage.py createsuperuser <br>

Run the server after complete setup. <br>
Redirect to 127.0.0.1:8000/admin <br>
Login as a admin using the superuser username and password, the click the view site at the nav bar of the django admin panel. <br>
Now you can access all patient appointments with filters for Date and Doctor <br>

