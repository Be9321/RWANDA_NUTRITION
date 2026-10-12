from django.urls import path
from . import views

app_name = 'households'

urlpatterns = [
    path('', views.HouseholdListView.as_view(), name='household_list'),
    path('add/', views.HouseholdCreateView.as_view(), name='household_create'),
    path('<int:pk>/', views.HouseholdDetailView.as_view(), name='household_detail'),
    path('<int:pk>/edit/', views.HouseholdUpdateView.as_view(), name='household_update'),
    path('<int:pk>/delete/', views.HouseholdDeleteView.as_view(), name='household_delete'),

    path('children/', views.ChildListView.as_view(), name='child_list'),
    path('children/add/', views.ChildCreateView.as_view(), name='child_create'),
    path('children/<int:pk>/', views.ChildDetailView.as_view(), name='child_detail'),
    path('children/<int:pk>/edit/', views.ChildUpdateView.as_view(), name='child_update'),
    path('children/<int:pk>/delete/', views.ChildDeleteView.as_view(), name='child_delete'),
]