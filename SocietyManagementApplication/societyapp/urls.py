from django.urls import path
from . import views
app_name = 'societyapp'
urlpatterns = [
path('',views.index,name='signup'),
path('login',views.login,name='login'),
path('otp', views.reg_otp_view, name='otp'),
]