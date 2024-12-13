from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

class Lecturer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    names = models.CharField(max_length=200)
    faculty = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.names} - {self.faculty}"

    @property
    def username(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email

    @property
    def password(self):
        return self.user.password

class Lecture(models.Model):
    lecturer = models.ForeignKey(
        Lecturer, 
        on_delete=models.CASCADE,
        default=1  # Default to first lecturer, adjust as needed
    )
    unit_code = models.CharField(max_length=20)
    unit_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.unit_code} - {self.unit_name}"

class Timetable(models.Model):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    unit_code = models.CharField(max_length=20)
    unit_name = models.CharField(max_length=100)
    venue = models.CharField(max_length=50)
    start_time = models.TimeField()
    day = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.unit_code} - {self.unit_name}"
