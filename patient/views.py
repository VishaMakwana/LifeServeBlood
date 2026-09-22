from urllib import request

from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

from patient.models import Patient
from blood.models import BloodRequest, BloodStock
from django.contrib import messages
from accounts.models import UserProfile
from accounts.models import Notification

from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.contrib.auth.models import User

# Create your views here.




@login_required
def patient_dashboard(request):

    patient = Patient.objects.get(user=request.user)

    requests = BloodRequest.objects.filter(patient=patient)

    total_requests = requests.count()

    last_request = requests.order_by("-request_date").first()

    recent_requests = requests.order_by("-request_date")[:5]

    # Monthly Blood Requests Chart
    monthly_requests = (
        requests
        .annotate(month=TruncMonth("request_date"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    months = [
        m["month"].strftime("%b")
        for m in monthly_requests
    ]

    request_counts = [
        m["total"]
        for m in monthly_requests
    ]

    # Status Chart
    approved = requests.filter(status="Approved").count()

    pending = requests.filter(status="Pending").count()

    rejected = requests.filter(status="Rejected").count()

    context = {

        "patient": patient,

        "total_requests": total_requests,

        "last_request": last_request,

        "recent_requests": recent_requests,

        # Chart Data
        "months": months,
        "request_counts": request_counts,

        "approved": approved,
        "pending": pending,
        "rejected": rejected,

    }

    return render(
        request,
        "patient/dashboard.html",
        context
    )





@login_required
def patient_profile(request):

    profile = Patient.objects.get(user=request.user)

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

        return redirect("patient_profile")

    context = {

        "profile": profile,

        "user_profile": user_profile,

    }

    return render(
        request,
        "patient/profile.html",
        context
    )

def patient_sidebar(request):
    return render(request,"patient/sidebar.html")

def blood_availability(request):
    blood_stock=BloodStock.objects.all().order_by("blood_group")
    context={"blood_stock":blood_stock}

    return render(request,"patient/blood_availability.html",context)


@login_required(login_url='login')
def patient_blood_request(request):

    patient = Patient.objects.get(user=request.user)

    if request.method == "POST":

        blood_group = request.POST.get("blood_group")
        units = request.POST.get("units")
        hospital = request.POST.get("hospital")
        reason = request.POST.get("reason")

        # Save Blood Request
        BloodRequest.objects.create(
            patient=patient,
            blood_group=blood_group,
            units=units,
            hospital=hospital,
            reason=reason,
            status="Pending"
        )
        

        # Create Notification for every Admin
        admins = User.objects.filter(is_superuser=True)

        for admin in admins:

            Notification.objects.create(
                user=admin,
                title="New Blood Request",
                message=f"{patient.user.get_full_name()} requested {units} unit(s) of {blood_group} blood.",
                notification_type="blood",
                is_read=False
            )
            print("Notification Created")

        messages.success(
            request,
            "Blood Request Sent Successfully."
        )

        return redirect("blood_request")

    return render(
        request,
        "patient/request_blood.html"
    )

@login_required
def patient_request_history(request):

    patient = Patient.objects.get(
        user=request.user
    )

    requests = BloodRequest.objects.filter(
        patient=patient
    ).order_by("-request_date")

    context = {

        "requests": requests,

    }

    return render(
        request,
        "patient/request_history.html",
        context
    )
@login_required
def patient_notifications(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    Notification.objects.filter(
        user=request.user,
        is_read=False
    ).update(is_read=True)

    return render(
        request,
        "patient/notifications.html",
        {
            "notifications": notifications
        }
    )