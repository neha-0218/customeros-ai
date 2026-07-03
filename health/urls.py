from django.urls import path
from . import views

urlpatterns = [
    path('', views.account_health_list, name='account_health_list'),
    path('risks/', views.risk_flag_list, name='risk_flag_list'),
    path('<uuid:pk>/', views.account_health_detail, name='account_health_detail'),
]