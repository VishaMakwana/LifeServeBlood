from django.urls import path
from . import views

urlpatterns = [

    path('dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('profile/', views.donor_profile, name='donor_profile'),
    path("donate-blood/",views.donate_blood,name="donate_blood"),
    path("donation-history/",views.donation_history,name="donation_history"),
    path("certificate/<int:id>/",views.donation_certificate,name="donation_certificate",),
    path("notifications/",views.notifications,name="notifications"),

]