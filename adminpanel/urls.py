from django.urls import path
from . import views

urlpatterns = [

    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

     # Donors
    path("donors/", views.manage_donors, name="manage_donors"),
    path("donors/view/<int:id>/", views.view_donor, name="view_donor"),
    path("donors/edit/<int:id>/", views.edit_donor, name="edit_donor"),
    path("donors/delete/<int:id>/", views.delete_donor, name="delete_donor"),

     #patients
    path("patients/", views.manage_patients, name="manage_patients"),
    path("patients/view/<int:id>/", views.view_patient, name="view_patient"),
    path("patients/edit/<int:id>/", views.edit_patient, name="edit_patient"),
    path("patients/delete/<int:id>/", views.delete_patient, name="delete_patient"),

     # Blood Stock 
    path("blood-stock/", views.blood_stock, name="blood_stock"),
    path("blood-stock/add/", views.add_blood_stock, name="add_blood_stock"),
    path("blood-stock/edit/<int:id>/", views.edit_blood_stock, name="edit_blood_stock"),
    path("blood-stock/delete/<int:id>/", views.delete_blood_stock, name="delete_blood_stock"),

    path("donation-requests/", views.donation_requests, name="donation_requests"),
    path("donation-request/<int:id>/approve/",views.approve_donation_request,name="approve_donation_request"),
    path("donation-request/<int:id>/reject/",views.reject_donation_request,name="reject_donation_request"),
    
    # Blood Requests
    path("blood-requests/", views.blood_requests, name="blood_requests"),
    path("blood-request/<int:id>/approve/",views.approve_blood_request,name="approve_blood_request"),
    path("blood-request/<int:id>/reject/",views.reject_blood_request,name="reject_blood_request"),


    #contact Messages
    path("contact-messages/",views.contact_messages,name="contact_messages"),
    path("contact-message/<int:id>/",views.contact_message_detail,name="contact_message_detail"),
    path("contact-message/<int:id>/reply/",views.reply_contact_message,name="reply_contact_message"),
    path("delete-contact-message/<int:id>/",views.delete_contact_message,name="delete_contact_message"),

    #reports
    path("reports/", views.reports, name="reports"),
    path("reports/pdf/",views.export_report_pdf,name="export_report_pdf"),
    path("reports/excel/",views.export_report_excel,name="export_report_excel"),
    path("reports/print/",views.print_report,name="print_report"),
    path("notifications/", views.admin_notifications, name="admin_notifications"),
        



]