from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('',views.dashboard,name='dashboard'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotpassword/',views.forgotpassword,name='forgotpassword'),
    path('forgotpassword_email/<uidb64>/<token>/', views.forgotpassword_email, name='forgotpassword_email'),
    path('resetpassword/',views.resetpassword,name='resetpassword'),



]