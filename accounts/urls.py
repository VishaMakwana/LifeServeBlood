from django.urls import path
from . import views

urlpatterns = [

    # path('', views.base, name="home"),
    path('', views.home, name="home"),

    path('about/', views.about, name="about"),

    path('contact/', views.contact, name="contact"),

    path('login/', views.login_view, name="login"),

    path('register/', views.register, name="register"),

    path('logout/', views.logout_view, name="logout"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),

    path("test-email/", views.test_email, name="test_email"),
    path("verify-register-otp/",views.verify_register_otp,name="verify_register_otp"),
    path("verify-login-otp/",views.verify_login_otp,name="verify_login_otp"),

]