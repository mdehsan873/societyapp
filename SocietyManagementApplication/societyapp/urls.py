from django.urls import path
from . import views

app_name = 'societyapp'
urlpatterns = [
    path('signup', views.index, name='signup'),
    path('login', views.login_view, name='login'),
    path('otp', views.reg_otp_view, name='otp'),
    path('reset', views.resetpassword, name='reset'),
    path('', views.dashboard, name='dashboard'),
    path('setpassword', views.setpassword, name='setpassword'),
    path('logout', views.logout, name='logout'),
    path('userprofile', views.profile, name='userprofile'),
    path('addnews', views.add_news, name='addnews'),
    path('addvisitor', views.add_visitor, name='addvisitor'),
    path('reslist', views.reslist, name='reslist'),
    path('rent',views.buy_rent,name='rent'),
    path('rent_board',views.rent_buy_board,name='br_board'),
    path('maintance',views.under_main,name='maint'),
    path('complain', views.under_main, name='complain')
]
