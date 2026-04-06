from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('api/targets/', views.TargetStatusView.as_view(), name='target_status'),
]
