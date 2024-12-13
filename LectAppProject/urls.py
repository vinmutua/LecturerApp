from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from LectApp import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', include('LectApp.urls')),  # Include app URLs last
    path('login/', views.login_view, name='login'),
    path('admin-page/', views.admin_page_view, name='admin_page'),
    path('admin-timetables/', views.admin_timetables_view, name='admin_timetables'),
    path('add-lecturer/', views.add_lecturer_view, name='add_lecturer'),
    path('add-timetable/<int:pk>/', views.add_timetable_view, name='add_timetable'),
    path('view-timetable/<int:pk>/', views.view_timetable_view, name='view_timetable'),
    path('lecturer-page/', views.lecturer_page_view, name='lecturer_page'),
    path('edit-lecturer/<int:pk>/', views.edit_lecturer_view, name='edit_lecturer'),
    path('delete-lecturer/<int:pk>/', views.delete_lecturer_view, name='delete_lecturer'),
]