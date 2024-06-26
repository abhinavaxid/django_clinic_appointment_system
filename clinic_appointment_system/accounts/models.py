from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    age = models.IntegerField()
    address = models.TextField()
    contact_number = models.CharField(max_length=15)

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField(default='00:00:00')
    doctor_name = models.CharField(max_length=100,default='Default Doctor')
    purpose = models.TextField(default='Default Purpose')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.appointment_date} {self.appointment_time} with {self.doctor_name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    dob = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)


