from django.urls import path
from . import views

urlpatterns = [
    path('', views.roadmap_list, name='roadmap_list'),
    path('new/', views.roadmap_create, name='roadmap_create'),
    path('<uuid:pk>/', views.roadmap_detail, name='roadmap_detail'),
]