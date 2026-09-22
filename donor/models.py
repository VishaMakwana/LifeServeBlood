from django.db import models

# Create your models here.
from django.contrib.auth.models import User
 


class Donor(models.Model):

    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    BLOOD_GROUPS = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )

    STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    age = models.PositiveIntegerField()

    gender = models.CharField(
        max_length=10,
        choices=GENDER
    )

    blood_group = models.CharField(
        max_length=5,
        choices=BLOOD_GROUPS
    )

    address = models.TextField()

    city = models.CharField(max_length=50)

    state = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)

    profile_photo = models.ImageField(
        upload_to="donors/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default="Pending"
    )

    def __str__(self):
        return self.user.first_name



