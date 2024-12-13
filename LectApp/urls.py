# LectApp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    # ... other URL patterns ...
    path('lecturer-page/', views.lecturer_page_view, name='lecturer_page'),
    path('delete-lecturer/<int:pk>/', views.delete_lecturer_view, name='delete_lecturer'),
]
