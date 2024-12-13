from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout, get_user_model
from functools import wraps
from .models import Lecture, Timetable, Lecturer, CustomUser  # Fix import
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.decorators.csrf import csrf_protect
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Admin access required')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper  # Fix indentation

def lecturer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'lecturer_id' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'You must be logged in as lecturer to view this page.')
            return redirect('login')
    return wrapper

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if role == 'admin' and user.is_staff:
                return redirect('admin_page')
            elif role == 'lecturer':
                return redirect('lecturer_page')
    return render(request, 'home.html')

def home_view(request):
    return render(request, 'home.html')

@csrf_protect
@admin_required
def add_lecturer_view(request):
    if request.method == 'POST':
        try:
            user = CustomUser.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password']
            )
            
            Lecturer.objects.create(
                user=user,
                names=request.POST['names'],
                faculty=request.POST['faculty']
            )
            messages.success(request, 'Lecturer added successfully!')
            return redirect('admin_page')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return render(request, 'addlecturer.html', {
                'form_data': request.POST
            })
    return render(request, 'addlecturer.html')

@csrf_protect
@admin_required 
def admin_page_view(request):
    if request.method == 'POST':
        try:
            # Get form data
            names = request.POST.get('names')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            faculty = request.POST.get('faculty')
            
            try:
                # Create CustomUser
                user = CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                
                # Create Lecturer
                Lecturer.objects.create(
                    user=user,
                    names=names,
                    faculty=faculty
                )
                messages.success(request, 'Lecturer added successfully!')
                return redirect('admin_page')
            except Exception as e:
                messages.error(request, f'Error adding lecturer: {str(e)}')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    # Get all lecturers for display
    lecturers = Lecturer.objects.select_related('user').all()
    return render(request, 'adminpage.html', {'lecturers': lecturers})

@admin_required
def delete_lecture_view(request, pk):
    lecture = get_object_or_404(Lecture, pk=pk)
    lecture.delete()
    messages.success(request, 'Lecture deleted successfully!')
    return redirect('admin_page')

@admin_required
def update_lecture_view(request, pk):
    lecture = get_object_or_404(Lecture, pk=pk)
    if request.method == 'POST':
        lecture.names = request.POST.get('names')
        lecture.username = request.POST.get('username')
        lecture.email = request.POST.get('email')
        lecture.faculty = request.POST.get('faculty')
        password = request.POST.get('password')

        if password:
            # Update the password if it's provided
            lecture.password = make_password(password)
        lecture.save()
        messages.success(request, 'Lecturer updated successfully!')
        return redirect('admin_page')
    else:
        return render(request, 'addlecturer.html', {'lecture': lecture})

@admin_required
def admin_timetables_view(request):
    timetables = Timetable.objects.select_related('lecturer').all()
    lecturers = Lecturer.objects.all()
    return render(request, 'admintimetables.html', {'timetables': timetables, 'lecturers': lecturers})

@admin_required 
def add_timetable_view(request, pk):
    lecturer = get_object_or_404(Lecturer, pk=pk)
    
    if request.method == 'POST':
        try:
            # Create and save timetable
            timetable = Timetable.objects.create(
                lecturer=lecturer,
                unit_code=request.POST['unitcode'],
                unit_name=request.POST['unitname'],
                venue=request.POST['venue'],
                time=request.POST['time']
            )
            # Verify save
            if timetable.id:
                logger.info(f'Timetable created with ID: {timetable.id}')
                messages.success(request, 'Timetable added successfully!')
                return redirect('admin_timetables')
            else:
                messages.error(request, 'Failed to save timetable')
        except Exception as e:
            logger.error(f'Error creating timetable: {str(e)}')
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'addtimetable.html', {'lecturer': lecturer})

@admin_required
def view_timetable_view(request, pk):
    lecturer = get_object_or_404(Lecturer, pk=pk)
    timetables = Timetable.objects.filter(lecturer=lecturer)
    return render(request, 'view_timetable.html', {
        'lecturer': lecturer,
        'timetables': timetables
    })

@login_required
def lecturer_page_view(request):
    try:
        lecturer = request.user.lecturer
        timetables = Timetable.objects.filter(lecturer=lecturer)
        context = {
            'lecturer': lecturer,
            'timetables': timetables
        }
        return render(request, 'lecturerpage.html', context)
    except Lecturer.DoesNotExist:
        messages.error(request, 'Lecturer profile not found')
        return redirect('login')

@admin_required
def edit_lecturer_view(request, pk):
    lecturer = get_object_or_404(Lecturer, pk=pk)
    
    if request.method == 'POST':
        try:
            # Update user data
            lecturer.user.username = request.POST['username']
            lecturer.user.email = request.POST['email']
            if request.POST['password']:
                lecturer.user.set_password(request.POST['password'])
            lecturer.user.save()
            
            # Update lecturer data
            lecturer.names = request.POST['names']
            lecturer.faculty = request.POST['faculty']
            lecturer.save()
            
            messages.success(request, 'Lecturer updated successfully!')
            return redirect('admin_page')
        except Exception as e:
            messages.error(request, f'Error updating lecturer: {str(e)}')
    
    # Pre-populate form
    context = {
        'lecturer': lecturer,
        'edit_mode': True
    }
    return render(request, 'addlecturer.html', context)

@admin_required
def delete_lecturer_view(request, pk):
    if request.method == 'POST':
        lecturer = get_object_or_404(Lecturer, pk=pk)
        try:
            # Delete user (will cascade delete lecturer due to OneToOne relationship)
            lecturer.user.delete()
            messages.success(request, 'Lecturer deleted successfully')
        except Exception as e:
            messages.error(request, f'Error deleting lecturer: {str(e)}')
        
    return redirect('admin_page')