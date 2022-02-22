from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_bikes, name='bikes'),
    path('<int:bike_id>/', views.bike_detail, name='bike_detail'),
    path('add/', views.add_bike, name='add_bike'),
    path('edit/<int:bike_id>/', views.edit_bike, name='edit_bike'),
    path('delete/<int:bike_id>/', views.delete_bike, name='delete_bike'),
]
