from django.urls import path
from . import views

urlpatterns = [

    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('profile/', views.patient_profile, name='patient_profile'),
    path('sidebar/', views.patient_sidebar, name='patient_sidebar'),
    path('blood_availability/',views.blood_availability,name='blood_availability'),
    path('blood_request/',views.patient_blood_request,name='blood_request'),
    path('blood_request_history/',views.patient_request_history,name='blood_request_history'),
    path("notifications/",views.patient_notifications,name="patient_notifications",),

]