from django.urls import path
from . import views

app_name = 'households'

urlpatterns = [
    path('children/', views.ChildListView.as_view(), name='child_list'),
    path('children/add/', views.ChildCreateView.as_view(), name='child_create'),
    path('children/<int:pk>/', views.ChildDetailView.as_view(), name='child_detail'),
    path('children/<int:pk>/edit/', views.ChildUpdateView.as_view(), name='child_update'),
    path('children/<int:pk>/delete/', views.ChildDeleteView.as_view(), name='child_delete'),
]