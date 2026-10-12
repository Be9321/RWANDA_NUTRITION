from django.urls import path
from . import views

app_name = 'nutrition'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('measurements/', views.GrowthMeasurementListView.as_view(), name='measurement_list'),
    path('measurements/add/', views.GrowthMeasurementCreateView.as_view(), name='measurement_create'),
    path('measurements/<int:pk>/', views.GrowthMeasurementDetailView.as_view(), name='measurement_detail'),
    path('measurements/<int:pk>/edit/', views.GrowthMeasurementUpdateView.as_view(), name='measurement_update'),
    path('measurements/<int:pk>/delete/', views.GrowthMeasurementDeleteView.as_view(), name='measurement_delete'),

    path('programs/', views.ProgramListView.as_view(), name='program_list'),
    path('programs/add/', views.ProgramCreateView.as_view(), name='program_create'),
    path('programs/<int:pk>/', views.ProgramDetailView.as_view(), name='program_detail'),
    path('programs/<int:pk>/edit/', views.ProgramUpdateView.as_view(), name='program_update'),
    path('programs/<int:pk>/delete/', views.ProgramDeleteView.as_view(), name='program_delete'),

    path('referrals/', views.ReferralListView.as_view(), name='referral_list'),
    path('referrals/add/', views.ReferralCreateView.as_view(), name='referral_create'),
    path('referrals/<int:pk>/', views.ReferralDetailView.as_view(), name='referral_detail'),
    path('referrals/<int:pk>/edit/', views.ReferralUpdateView.as_view(), name='referral_update'),
    path('referrals/<int:pk>/delete/', views.ReferralDeleteView.as_view(), name='referral_delete'),
]