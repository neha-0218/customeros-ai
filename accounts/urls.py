from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    CustomLoginView, SignupView, dashboard_redirect,
    pm_dashboard, analyst_dashboard, cs_dashboard
)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('dashboard/', dashboard_redirect, name='dashboard_redirect'),
    path('dashboard/pm/', pm_dashboard, name='pm_dashboard'),
    path('dashboard/analyst/', analyst_dashboard, name='analyst_dashboard'),
    path('dashboard/cs/', cs_dashboard, name='cs_dashboard'),
    path('', lambda request: redirect('login'), name='home'),
]
