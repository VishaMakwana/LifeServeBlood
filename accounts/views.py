from urllib import request

from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import ContactMessage

from donor.models import Donor
from patient.models import Patient
from .models import UserProfile

#email
from django.core.mail import send_mail
from django.http import HttpResponse
import random
from django.conf import settings
from datetime import datetime, timedelta
from blood.models import BloodStock


# Create your views here.

def base(request):
    return render(request,"home/base.html")
def home(request):

    blood_stock = BloodStock.objects.all().order_by("blood_group")

    context = {
        "blood_stock": blood_stock,
    }

    return render(
        request,
        "home/home.html",
        context
    )

def about(request):
    return render(request,"home/about.html")



def contact(request):

    if request.method == "POST":

        ContactMessage.objects.create(

            name=request.POST.get("name"),
            email=request.POST.get("email"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message")

        )

        messages.success(
            request,
            "Your message has been sent successfully."
        )

        return redirect("contact")

    return render(request, "home/contact.html")

# def login_view(request):
#     return render(request,"accounts/login.html")

# def register(request):
#     return render(request,"accounts/register.html")


def register(request):

    if request.method == "POST":

        fullname = request.POST.get("fullname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        blood_group = request.POST.get("blood_group")
        city = request.POST.get("city")
        address = request.POST.get("address")
        state = request.POST.get("state")

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")

        # Password Check
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        # Username Check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            first_name=fullname,
            email=email,
            password=password
        )

        UserProfile.objects.create(
            user=user,
            phone=phone,
            role=role
        )

        if role == "Donor":
            Donor.objects.create(
                user=user,
                age=age,
                gender=gender,
                blood_group=blood_group,
                city=city,
                state=state,
                address=address
            )
        else:
            Patient.objects.create(
                user=user,
                age=age,
                gender=gender,
                blood_group=blood_group,
                city=city,
                state=state,
                address=address
            )

        messages.success(request, "Registration successful. Please login.")
        return redirect("login")

    return render(request, "accounts/register.html")

def verify_register_otp(request):

    if request.method == "POST":

        user_otp = request.POST.get("otp")

        expiry = datetime.strptime(
            request.session["register_otp_expiry"],
            "%Y-%m-%d %H:%M:%S"
        )

        if datetime.now() > expiry:

            messages.error(request, "OTP has expired.")

            request.session.pop("register_otp", None)
            request.session.pop("register_data", None)
            request.session.pop("register_otp_expiry", None)

            return redirect("register")

        saved_otp = request.session.get("register_otp")

        if user_otp == saved_otp:

            data = request.session.get("register_data")

            user = User.objects.create_user(
                username=data["username"],
                first_name=data["fullname"],
                email=data["email"],
                password=data["password"]
            )

            UserProfile.objects.create(
                user=user,
                phone=data["phone"],
                role=data["role"]
            )

            if data["role"] == "Donor":

                Donor.objects.create(
                    user=user,
                    age=data["age"],
                    gender=data["gender"],
                    blood_group=data["blood_group"],
                    city=data["city"],
                    state=data["state"],
                    address=data["address"]
                )

            else:

                Patient.objects.create(
                    user=user,
                    age=data["age"],
                    gender=data["gender"],
                    blood_group=data["blood_group"],
                    city=data["city"],
                    state=data["state"],
                    address=data["address"]
                )

            request.session.pop("register_otp", None)
            request.session.pop("register_data", None)
            request.session.pop("register_otp_expiry", None)

            messages.success(request, "Registration completed successfully.")

            return redirect("login")

        else:

            messages.error(request, "Invalid OTP.")

    return render(
        request,
        "accounts/verify_register_otp.html"
    )

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # ==========================================
            # ADMIN LOGIN
            # Admin ko OTP nahi chahiye
            # ==========================================

            if user.is_superuser:

                login(request, user)

                return redirect("admin_dashboard")


            # ==========================================
            # DONOR / PATIENT LOGIN
            # Inko OTP chahiye
            # ==========================================

            try:

                profile = UserProfile.objects.get(
                    user=user
                )

            except UserProfile.DoesNotExist:

                messages.error(
                    request,
                    "User profile not found."
                )

                return redirect("login")


            if profile.role in ["Donor", "Patient"]:

                # Generate OTP
                otp = generate_otp()

                # Save OTP & User ID in Session
                request.session["login_otp"] = otp

                request.session["login_otp_expiry"] = (
                    datetime.now() + timedelta(minutes=5)
                ).strftime("%Y-%m-%d %H:%M:%S")

                request.session["login_user_id"] = user.id

                # Reset attempts
                request.session["login_attempt"] = 0


                # Send OTP Email
                send_mail(

                    subject="LifeServe Login Verification",

                    message=f"""
Hello {user.first_name},

Your LifeServe Login OTP is:

{otp}

This OTP is valid for 5 minutes.

Do not share this OTP with anyone.

Thank you,
LifeServe Blood Bank
""",

                    from_email=settings.EMAIL_HOST_USER,

                    recipient_list=[user.email],

                    fail_silently=False,

                )


                messages.success(
                    request,
                    "OTP has been sent to your registered email."
                )

                return redirect("verify_login_otp")


            # Agar role Donor/Patient nahi hai
            messages.error(
                request,
                "Invalid user role."
            )

            return redirect("login")


        else:

            messages.error(
                request,
                "Invalid Username or Password"
            )


    return render(
        request,
        "accounts/login.html"
    )

def verify_login_otp(request):

    if request.method == "POST":

        entered_otp = request.POST.get("otp")

        expiry = datetime.strptime(
            request.session["login_otp_expiry"],
            "%Y-%m-%d %H:%M:%S"
        )

        if datetime.now() > expiry:

            messages.error(request, "OTP has expired.")

            request.session.pop("login_otp", None)
            request.session.pop("login_user_id", None)
            request.session.pop("login_otp_expiry", None)

            return redirect("login")

        saved_otp = request.session.get("login_otp")

        attempt = request.session.get("login_attempt", 0)

        if entered_otp != saved_otp:

            request.session["login_attempt"] = attempt + 1

            if request.session["login_attempt"] >= 3:

                messages.error(request, "Too many invalid attempts.")

                request.session.pop("login_otp", None)
                request.session.pop("login_user_id", None)
                request.session.pop("login_otp_expiry", None)
                request.session.pop("login_attempt", None)

                return redirect("login")

            messages.error(request, "Invalid OTP")

            return redirect("verify_login_otp")

        user_id = request.session.get("login_user_id")

        user = User.objects.get(id=user_id)

        login(request, user)

        request.session.pop("login_otp", None)
        request.session.pop("login_user_id", None)
        request.session.pop("login_otp_expiry", None)
        request.session.pop("login_attempt", None)

        if user.is_superuser:
            return redirect("admin_dashboard")

        profile = UserProfile.objects.get(user=user)

        if profile.role == "Donor":
            return redirect("donor_dashboard")

        return redirect("patient_dashboard")

    return render(request, "accounts/verify_login_otp.html")

def logout_view(request):

    logout(request)

    return redirect("home")

def forgot_password(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("forgot_password")

        try:
            user = User.objects.get(username=username)

            user.set_password(password)
            user.save()

            messages.success(request, "Password changed successfully. Please login.")
            return redirect("login")

        except User.DoesNotExist:
            messages.error(request, "Username not found.")

    return render(request, "accounts/forgot_password.html")



def test_email(request):

    send_mail(
        subject="LifeServe Test Email",
        message="Email is working successfully.",
        from_email=None,
        recipient_list=["makwanavishal1806@gmail.com"],
        fail_silently=False,
    )

    return HttpResponse("Email Sent Successfully")

def generate_otp():
    return str(random.randint(100000, 999999))