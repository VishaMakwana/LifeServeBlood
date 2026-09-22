from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from blood.models import DonationRequest
from django.shortcuts import get_object_or_404
from django.contrib import messages
from accounts.models import UserProfile
from datetime import timedelta
from django.db.models import Count
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import red,gold, black
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from io import BytesIO
import qrcode
import os
from django.conf import settings
from .models import Donor
from accounts.models import Notification

# Create your views here.



@login_required
def donor_dashboard(request):

    donor = get_object_or_404(Donor, user=request.user)

    donations = DonationRequest.objects.filter(donor=donor)

    total_donations = donations.filter(status="Approved").count()

    last_donation = donations.order_by("-donation_date").first()
    recent_donations = donations.order_by("-donation_date")[:5]

    context = {
        "donor": donor,
        "total_donations": total_donations,
        "last_donation": last_donation,
        "recent_donations": recent_donations,
    }

    return render(request, "donor/dashboard.html", context)

@login_required
def donor_profile(request):

    profile = Donor.objects.get(user=request.user)
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":

        request.user.first_name = request.POST.get("fullname")
        request.user.email = request.POST.get("email")
        request.user.save()

        user_profile.phone = request.POST.get("phone")
        user_profile.save()

        profile.age = request.POST.get("age")
        profile.gender = request.POST.get("gender")
        profile.blood_group = request.POST.get("blood_group")
        profile.city = request.POST.get("city")
        profile.state = request.POST.get("state")
        profile.address = request.POST.get("address")

        if request.FILES.get("profile_photo"):
            profile.profile_photo = request.FILES["profile_photo"]

        profile.save()

        messages.success(request, "Profile Updated Successfully.")

        return redirect("donor_profile")

    context = {
        "profile": profile,
        "user_profile": user_profile,
    }

    return render(request, "donor/profile.html", context)


@login_required
def donate_blood(request):

    donor = Donor.objects.get(user=request.user)

    donations = DonationRequest.objects.filter(
        donor=donor,
        status="Approved"
    ).order_by("-donation_date")

    last_donation = donations.first()

    next_date = None
    eligible = True

    if last_donation:
        next_date = last_donation.donation_date + timedelta(days=90)

        from datetime import date

        if date.today() < next_date:
            eligible = False

    current_request = DonationRequest.objects.filter(
        donor=donor
    ).order_by("-id").first()

    if request.method == "POST":

        if not eligible:

            messages.error(
                request,
                "You are not eligible to donate yet."
            )

            return redirect("donate_blood")

        DonationRequest.objects.create(

            donor=donor,

            blood_group=donor.blood_group,

            units=request.POST.get("units"),

            remarks=request.POST.get("remarks"),

        )

        messages.success(
            request,
            "Donation Request Submitted Successfully."
        )

        return redirect("donate_blood")

    context = {

        "donor": donor,

        "last_donation": last_donation,

        "next_date": next_date,

        "eligible": eligible,

        "current_request": current_request,

    }

    return render(
        request,
        "donor/donate_blood.html",
        context
    )

@login_required
def donation_history(request):

    donor = Donor.objects.get(user=request.user)

    donations = DonationRequest.objects.filter(
        donor=donor
    ).order_by("-donation_date")

    status = request.GET.get("status")

    if status:
        donations = donations.filter(status=status)

    approved = donations.filter(status="Approved").count()
    pending = donations.filter(status="Pending").count()
    rejected = donations.filter(status="Rejected").count()

    total = donations.count()

    # Next Badge
    if approved < 3:
        next_badge = 3
    elif approved < 10:
        next_badge = 10
    elif approved < 25:
        next_badge = 25
    elif approved < 50:
        next_badge = 50
    else:
        next_badge = approved

    context = {
        "donor": donor,
        "donations": donations,
        "total": total,
        "approved": approved,
        "pending": pending,
        "rejected": rejected,
        "next_badge": next_badge,
    }

    return render(
        request,
        "donor/donation_history.html",
        context
    )
@login_required
def donation_certificate(request, id):

    donor = Donor.objects.get(user=request.user)

    donation = DonationRequest.objects.get(
        id=id,
        donor=donor,
        status="Approved"
    )

    response = HttpResponse(content_type="application/pdf")

    response["Content-Disposition"] = (
        f'attachment; filename=Donation_Certificate_{donation.id}.pdf'
    )

    pdf = canvas.Canvas(response, pagesize=A4)

    width, height = A4


    # GOLD BORDER


    pdf.setStrokeColor(gold)
    pdf.setLineWidth(5)

    pdf.rect(
        25,
        25,
        width-50,
        height-50
    )

    
    # LOGO
    
    logo = os.path.join(
        settings.BASE_DIR,
        "static",
        "images",
        "blood logo.jpg"
    )

    if os.path.exists(logo):

        pdf.drawImage(
            logo,
            240,
            735,
            width=100,
            height=100,
            preserveAspectRatio=True
        )

    # ===========================
    # HEADER
    # ===========================

    pdf.setFillColor(red)

    pdf.setFont("Helvetica-Bold",26)

    pdf.drawCentredString(
        width/2,
        710,
        "LifeServe Blood Bank"
    )

    pdf.setFont("Helvetica-Bold",20)

    pdf.drawCentredString(
        width/2,
        680,
        "DONATION CERTIFICATE"
    )

    pdf.setStrokeColor(red)

    pdf.line(
        80,
        665,
        width-80,
        665
    )

    # ===========================
    # BODY
    # ===========================

    pdf.setFillColor(black)

    pdf.setFont("Helvetica",15)

    pdf.drawCentredString(
        width/2,
        620,
        "This Certificate is proudly presented to"
    )

    pdf.setFont("Helvetica-Bold",22)

    pdf.drawCentredString(
        width/2,
        585,
        donor.user.get_full_name()
    )

    pdf.setFont("Helvetica",15)

    pdf.drawCentredString(
        width/2,
        550,
        "For selflessly donating blood and helping save lives."
    )

    pdf.setFont("Helvetica-Bold",14)

    pdf.drawString(
        100,
        490,
        f"Blood Group : {donation.blood_group}"
    )

    pdf.drawString(
        100,
        460,
        f"Units : {donation.units}"
    )

    pdf.drawString(
        100,
        430,
        f"Donation Date : {donation.donation_date}"
    )

    pdf.drawString(
        100,
        400,
        f"Certificate ID : LS-{donation.id:05d}"
    )

    # ===========================
    # QR CODE
    # ===========================

    qr = qrcode.make(
        f"""
Certificate ID : LS-{donation.id:05d}

Donor :
{donor.user.get_full_name()}

Blood Group :
{donation.blood_group}

Donation Date :
{donation.donation_date}
"""
    )

    buffer = BytesIO()

    qr.save(buffer)

    buffer.seek(0)

    pdf.drawImage(
        ImageReader(buffer),
        410,
        340,
        width=120,
        height=120
    )

    # ===========================
    # THANK YOU
    # ===========================

    pdf.setFont("Helvetica-Bold",18)

    pdf.setFillColor(red)

    pdf.drawCentredString(
        width/2,
        300,
        "Thank You For Saving Lives ❤️"
    )

    # ===========================
    # GENERATED DATE
    # ===========================

    from datetime import datetime

    pdf.setFillColor(black)

    pdf.setFont("Helvetica",11)

    pdf.drawString(
        90,
        180,
        "Generated : " +
        datetime.now().strftime("%d %B %Y")
    )

    # ===========================
    # SIGNATURE
    # ===========================

    pdf.line(
        360,
        150,
        520,
        150
    )

    pdf.setFont("Helvetica",12)

    pdf.drawString(
        390,
        130,
        "Administrator"
    )

    pdf.save()

    return response

def notifications(request):
    notifications=Notification.objects.filter(user=request.user).order_by('-created_at')
    notifications.update(is_read=True)
    return render(request,'donor/notifications.html',{'notifications':notifications})