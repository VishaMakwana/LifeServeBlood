

# Create your models here.
from django.db import models
from donor.models import Donor
from patient.models import Patient


class BloodStock(models.Model):

    BLOOD_GROUPS = [

        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),

    ]

    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS)

    units = models.PositiveIntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.blood_group


class BloodRequest(models.Model):

    STATUS = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    blood_group = models.CharField(max_length=5)

    units = models.PositiveIntegerField()

    hospital = models.CharField(
        max_length=100,
        default="Unknown Hospital"
    )

    reason = models.TextField(
        default="No Reason"
    )

    request_date = models.DateField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default="Pending"
    )

    def __str__(self):
        return f"{self.patient.user.first_name} - {self.blood_group}"

class DonationRequest(models.Model):

    STATUS = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    donor = models.ForeignKey(
        Donor,
        on_delete=models.CASCADE
    )

    blood_group = models.CharField(max_length=5)

    units = models.PositiveIntegerField(default=1)

    donation_date = models.DateField(
        auto_now_add=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default="Pending"
    )

    def __str__(self):
        return f"{self.donor.user.first_name} - {self.blood_group}"