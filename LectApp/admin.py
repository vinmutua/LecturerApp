# LectApp/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser, Lecture, Timetable, Lecturer

class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email',)
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Lecture)
admin.site.register(Timetable)
admin.site.register(Lecturer)

# LectAppProject/urls.py
from django.contrib import admin
from django.urls import path
from LectApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('', views.home_view, name='home'),
    path('add-lecturer/', views.add_lecturer_view, name='add_lecturer'),
    path('admin-page/', views.admin_page_view, name='admin_page'),
    path('delete-lecture/<int:pk>/', views.delete_lecture_view, name='delete_lecture'),
    path('update-lecture/<int:pk>/', views.update_lecture_view, name='update_lecture'),
    path('admin-timetables/', views.admin_timetables_view, name='admin_timetables'),
    path('add-timetable/<int:pk>/', views.add_timetable_view, name='add_timetable'),
    path('view-timetable/<int:pk>/', views.view_timetable_view, name='view_timetable'),
    # path('update-timetable/<int:pk>/', views.update_timetable_view, name='update_timetable'),  # Commented out
    # path('delete-timetable/<int:pk>/', views.delete_timetable_view, name='delete_timetable'),  # If needed
]
