from django.urls import path
from . import views

urlpatterns = [
    path('', views.feature_list, name='feature_list'),
    path('new/', views.feature_create, name='feature_create'),
    path('<uuid:pk>/', views.feature_detail, name='feature_detail'),
    path('<uuid:pk>/vote/', views.feature_vote, name='feature_vote'),
]