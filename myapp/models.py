from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Student(models.Model):
    name = models.CharField(max_length=100)
    roll = models.IntegerField(unique=True)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Token(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)  # Assuming 6-digit OTP
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Token for {self.student.name} - OTP: {self.otp}"
    
class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Allow null to avoid issues
    otp = models.CharField(max_length=6)
    expires_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"OTP for {self.user.username} - OTP: {self.otp}"
