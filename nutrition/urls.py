from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Measurements
    path('measurements/', views.MeasurementListView.as_view(), name='measurement_list'),
    path('measurements/add/', views.MeasurementCreateView.as_view(), name='measurement_create'),
    path('measurements/<int:pk>/edit/', views.MeasurementUpdateView.as_view(), name='measurement_update'),
    path('measurements/<int:pk>/delete/', views.MeasurementDeleteView.as_view(), name='measurement_delete'),

    # Programs and enrolments
    path('programs/', views.ProgramListView.as_view(), name='program_list'),
    path('programs/add/', views.ProgramCreateView.as_view(), name='program_create'),
    path('programs/<int:pk>/', views.ProgramDetailView.as_view(), name='program_detail'),
    path('programs/<int:pk>/edit/', views.ProgramUpdateView.as_view(), name='program_update'),
    path('programs/<int:pk>/delete/', views.ProgramDeleteView.as_view(), name='program_delete'),
    path('programs/<int:pk>/enroll/', views.EnrollmentCreateView.as_view(), name='enrollment_create'),
    path('enrollments/<int:pk>/delete/', views.EnrollmentDeleteView.as_view(), name='enrollment_delete'),

    # Referrals
    path('referrals/', views.ReferralListView.as_view(), name='referral_list'),
    path('referrals/add/', views.ReferralCreateView.as_view(), name='referral_create'),
    path('referrals/<int:pk>/edit/', views.ReferralUpdateView.as_view(), name='referral_update'),
    path('referrals/<int:pk>/delete/', views.ReferralDeleteView.as_view(), name='referral_delete'),
    path('referrals/<int:pk>/status/<slug:status>/', views.referral_set_status, name='referral_status'),
]