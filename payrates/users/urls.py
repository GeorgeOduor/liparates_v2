from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    # path("reset-password/", views.ResetPasswordView.as_view(), name="reset-password"),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
