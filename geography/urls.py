from django.urls import path
from . import views

app_name = 'geography'

urlpatterns = [
    path('districts/', views.district_list, name='district_list'),
    path('districts/<int:pk>/', views.district_detail, name='district_detail'),
    path('map/', views.district_map, name='map'),
]