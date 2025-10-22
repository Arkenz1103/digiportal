from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from inertia import render as inertia_render
from .middleware import teacher_required, student_required
from .models import User, PortfolioFolder, PortfolioActivity, StudentSubmission, Notification, Remark, RemarkReadStatus, PortfolioCompilationRequest
from .serializer import PortfolioFolderSerializer, PortfolioActivitySerializer, StudentSubmissionSerializer, NotificationSerializer, RemarkSerializer
import json


# Helper function to create notifications
def create_notification(recipient, notification_type, title, message, portfolio=None, activity=None, submission=None, remark=None):
    """Helper function to create a notification"""
    try:
        notification = Notification.objects.create(
            recipient=recipient,
            notification_type=notification_type,
            title=title,
            message=message,
            portfolio=portfolio,
            activity=activity,
            submission=submission,
            remark=remark
        )
        print(f"Created notification: {title} for {recipient.username}")
        return notification
    except Exception as e:
        print(f"Error creating notification: {str(e)}")
        return None


# Authentication Views
@require_http_methods(["GET"])
def landing(request):
    """Landing page"""
    return inertia_render(request, 'Landing')


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Login view"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Try to find user by email
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                auth_login(request, user)
                
                # Redirect based on role
                if user.role == 'teacher':
                    return redirect('teacher_home')
                elif user.role == 'student':
                    return redirect('student_newsfeed')
                else:
                    return redirect('landing')
            else:
                return inertia_render(request, 'Auth/Login', {
                    'errors': {'email': 'Invalid credentials.'}
                })
        except User.DoesNotExist:
            return inertia_render(request, 'Auth/Login', {
                'errors': {'email': 'Invalid credentials.'}
            })
    
    return inertia_render(request, 'Auth/Login')


@require_http_methods(["POST"])
def logout_view(request):
    """Logout view"""
    auth_logout(request)
    return redirect('login')


# Teacher Views
@login_required
@teacher_required
def teacher_home(request):
    """Teacher home page"""
    return inertia_render(request, 'Teacher/Home')


@login_required
@teacher_required
def teacher_outputs(request, id):
    """Teacher outputs page"""
    activity = request.GET.dict()
    
    # Ensure grade_section is available
    if 'grade_section' not in activity and 'room_id' in activity:
        activity['grade_section'] = activity['room_id']
    
    return inertia_render(request, 'Teacher/Outputs', {
        'activity': activity
    })


@login_required
@teacher_required
def teacher_class(request, grade_section):
    """Teacher class room page"""
    # Convert 'grade1-a' to 'Grade 1 - A'
    parts = grade_section.split('-')
    
    if len(parts) < 2:
        return redirect('teacher_home')
    
    grade = parts[0].replace('grade', 'Grade ')
    section = parts[1].upper()
    display_name = f"{grade} - {section}"
    
    # Default theme mapping
    classes = {
        'Grade 1 - A': 'purple',
        'Grade 2 - A': 'purple',
        'Grade 3 - A': 'purple',
    }
    
    return inertia_render(request, 'Teacher/Room', {
        'className': display_name,
        'theme': classes.get(display_name, 'emerald')
    })


@login_required
@teacher_required
def teacher_notify(request):
    """Teacher notify page"""
    return inertia_render(request, 'Teacher/Notify', {
        'user': {
            'id': request.user.id,
            'name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
            'role': request.user.role,
        }
    })


@login_required
@teacher_required
def teacher_progress(request):
    """Teacher progress page"""
    selected_student = request.GET.get('student', None)
    return inertia_render(request, 'Teacher/Progress', {
        'selectedStudent': selected_student
    })


@login_required
@teacher_required
def teacher_sprogress(request):
    """Teacher student progress page"""
    from django.db.models import Count, Q
    
    # Get class name from query parameter (from Sroom)
    class_name = request.GET.get('class', None)
    
    # Get all students (optionally filtered by class), exclude admin users
    students = User.objects.filter(role='student').exclude(username='admin').order_by('username')
    
    # Get teacher's portfolio folders
    teacher_folders = PortfolioFolder.objects.filter(teacher=request.user)
    
    # If class is specified, filter students by submissions in that class's portfolios
    if class_name:
        # Get folders for this class
        class_folders = teacher_folders.filter(class_name=class_name)
        # Get students who have submissions in these folders
        student_ids = StudentSubmission.objects.filter(
            activity__folder__in=class_folders
        ).values_list('student_id', flat=True).distinct()
        students = students.filter(id__in=student_ids)
    
    student_data = []
    for student in students:
        # Count total outputs (submissions) for this student
        total_outputs = StudentSubmission.objects.filter(student=student).count()
        
        # Get student's submissions with portfolio and activity info
        submissions = StudentSubmission.objects.filter(
            student=student,
            activity__isnull=False
        ).select_related('activity__folder').order_by('-submitted_at')
        
        student_data.append({
            'id': student.id,
            'student_id': f'STD{str(student.id).zfill(3)}',
            'name': student.get_full_name() or student.username,
            'username': student.username,
            'email': student.email,
            'total_outputs': total_outputs,
            'submissions': [
                {
                    'id': sub.id,
                    'activity_title': sub.activity.title if sub.activity else 'Sketch Pad',
                    'portfolio_name': sub.activity.folder.name if sub.activity and sub.activity.folder else 'N/A',
                    'score': sub.score,
                    'status': sub.status,
                    'submitted_at': sub.submitted_at.isoformat() if sub.submitted_at else None,
                }
                for sub in submissions[:10]  # Limit to 10 recent submissions
            ]
        })
    
    return inertia_render(request, 'Teacher/Sprogress', {
        'students': student_data,
        'class_name': class_name,
        'portfolio_folders': [
            {
                'id': folder.id,
                'name': folder.name,
                'class_name': folder.class_name,
            }
            for folder in teacher_folders
        ]
    })


@login_required
@teacher_required
def teacher_remarks(request):
    """Teacher remarks page"""
    return inertia_render(request, 'Teacher/Remarks', {
        'user': {
            'id': request.user.id,
            'name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
            'role': request.user.role,
        }
    })


@login_required
@teacher_required
def teacher_notice(request):
    """Teacher notice page"""
    return inertia_render(request, 'Teacher/Notice')


@login_required
@teacher_required
def teacher_archived(request):
    """Teacher archived page"""
    return inertia_render(request, 'Teacher/Archived')


# Student Views
@login_required
@student_required
def student_dashboard(request):
    """Student dashboard - redirects to newsfeed"""
    return redirect('student_newsfeed')


@login_required
@student_required
def student_newsfeed(request):
    """Student newsfeed page"""
    return inertia_render(request, 'Student/Newsfeed')


@login_required
@student_required
def student_sketch(request):
    """Student sketch page"""
    return inertia_render(request, 'Student/Sketch')


@login_required
@student_required
def student_archived(request):
    """Student archived page"""
    return inertia_render(request, 'Student/Sarchived')


@login_required
@student_required
def student_class(request, grade_section):
    """Student class room page"""
    parts = grade_section.split('-')
    
    if len(parts) < 2:
        return redirect('student_newsfeed')
    
    grade = parts[0].replace('grade', 'Grade ')
    section = parts[1].upper()
    display_name = f"{grade} - {section}"
    
    classes = {
        'Grade 1 - A': 'purple',
        'Grade 2 - A': 'purple',
        'Grade 3 - A': 'purple',
    }
    
    return inertia_render(request, 'Student/Sroom', {
        'className': display_name,
        'theme': classes.get(display_name, 'emerald')
    })


@login_required
@student_required
def student_notifications(request):
    """Student notifications page"""
    return inertia_render(request, 'Student/Snotify', {
        'user': {
            'id': request.user.id,
            'name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
            'role': request.user.role,
        }
    })


# API Views
@csrf_exempt
@api_view(['GET', 'POST'])
def validate_session(request, id=None):
    """Validate user session and create mock session for development"""
    # Ignore the ID parameter if provided (for backwards compatibility)
    if id is not None:
        print(f"Warning: validate_session called with ID={id}, ignoring it")
    
    if request.method == 'GET':
        if request.user.is_authenticated:
            print(f"User authenticated: {request.user.username} (role: {request.user.role})")
            return JsonResponse({
                'authenticated': True,
                'user': {
                    'id': request.user.id,
                    'name': request.user.get_full_name() or request.user.username,
                    'email': request.user.email,
                    'role': request.user.role,
                }
            })
        print("User not authenticated")
        return JsonResponse({'authenticated': False}, status=401)
    
    elif request.method == 'POST':
        # For development: create a mock session
        try:
            data = json.loads(request.body)
            role = data.get('role', 'teacher')
            
            print(f"Creating/authenticating test user with role: {role}")
            
            # Try to get or create a test user
            user, created = User.objects.get_or_create(
                username=f'test_{role}',
                defaults={
                    'email': f'test_{role}@example.com',
                    'role': role,
                    'first_name': 'Test',
                    'last_name': role.capitalize()
                }
            )
            
            if created:
                user.set_password('password123')
                user.save()
                print(f"Created new test user: {user.username}")
            else:
                print(f"Using existing test user: {user.username}")
            
            # Log the user in
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            print(f"User logged in successfully: {user.username} (role: {user.role})")
            
            return JsonResponse({
                'authenticated': True,
                'user': {
                    'id': user.id,
                    'name': user.get_full_name() or user.username,
                    'email': user.email,
                    'role': user.role,
                }
            })
        except Exception as e:
            import traceback
            print(f"Error in validate_session POST: {str(e)}")
            print(traceback.format_exc())
            return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@api_view(['GET', 'POST'])
def portfolio_folders_api(request):
    """
    GET: List all portfolio folders
    POST: Create a new portfolio folder (teacher only)
    """
    if request.method == 'GET':
        try:
            folders = PortfolioFolder.objects.all().order_by('-created_at')
            serializer = PortfolioFolderSerializer(folders, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(f"Error fetching folders: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'POST':
        # Check authentication
        if not hasattr(request, 'user') or not request.user or not request.user.is_authenticated:
            print(f"Authentication failed - User: {getattr(request, 'user', None)}")
            return Response({
                'error': 'Authentication required',
                'detail': 'Please authenticate with the backend first'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check role
        if not hasattr(request.user, 'role') or request.user.role != 'teacher':
            print(f"Authorization failed - User role: {getattr(request.user, 'role', 'unknown')}")
            return Response({
                'error': 'Only teachers can create folders',
                'detail': f'Your role is: {getattr(request.user, "role", "unknown")}'
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            # Use request.data (DRF automatically parses JSON)
            # DO NOT access request.body after this!
            data = request.data
            print(f"Received data: {data}")
            print(f"Content-Type: {request.content_type}")
            
            name = data.get('name')
            description = data.get('description', '')
            class_name = data.get('class_name', 'Grade 1 - A')  # Default class name
            
            if not name:
                return Response({'error': 'Folder name is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            print(f"Creating folder - Name: {name}, User: {request.user.username}, Class: {class_name}")
            
            folder = PortfolioFolder.objects.create(
                teacher=request.user,
                name=name,
                class_name=class_name,
                description=description
            )
            
            # Notify all students about new portfolio (exclude admin)
            students = User.objects.filter(role='student').exclude(username='admin')
            print(f"📢 Notifying {students.count()} students about new portfolio")
            
            for student in students:
                notification = create_notification(
                    recipient=student,
                    notification_type='portfolio_created',
                    title='New Portfolio Created',
                    message=f'Teacher {request.user.username} created a new portfolio: {name}',
                    portfolio=folder
                )
                if notification:
                    print(f"✅ Notification created for student: {student.username}")
                else:
                    print(f"❌ Failed to create notification for student: {student.username}")
            
            serializer = PortfolioFolderSerializer(folder)
            print(f"Folder created successfully - ID: {folder.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except KeyError as e:
            print(f"Missing required field: {str(e)}")
            return Response({'error': f'Missing required field: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            import traceback
            print(f"Error creating folder: {str(e)}")
            print(traceback.format_exc())
            return Response({'error': str(e), 'detail': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def portfolio_folder_detail_api(request, folder_id):
    """
    GET: Get folder details
    PUT: Update folder (teacher only)
    DELETE: Delete folder (teacher only)
    """
    try:
        folder = PortfolioFolder.objects.get(id=folder_id)
    except PortfolioFolder.DoesNotExist:
        return Response({'error': 'Folder not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PortfolioFolderSerializer(folder)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        if not request.user.is_authenticated or request.user.role != 'teacher':
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            data = json.loads(request.body)
            folder.name = data.get('name', folder.name)
            folder.description = data.get('description', folder.description)
            folder.save()
            
            # Notify all students about portfolio update (exclude admin)
            students = User.objects.filter(role='student').exclude(username='admin')
            for student in students:
                create_notification(
                    recipient=student,
                    notification_type='portfolio_updated',
                    title='Portfolio Updated',
                    message=f'Portfolio "{folder.name}" has been updated',
                    portfolio=folder
                )
            
            serializer = PortfolioFolderSerializer(folder)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if not request.user.is_authenticated or request.user.role != 'teacher':
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        folder_name = folder.name
        
        # Notify all students about portfolio deletion (exclude admin)
        students = User.objects.filter(role='student').exclude(username='admin')
        for student in students:
            create_notification(
                recipient=student,
                notification_type='portfolio_deleted',
                title='Portfolio Deleted',
                message=f'Portfolio "{folder_name}" has been deleted'
            )
        
        folder.delete()
        return Response({'message': 'Folder deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET', 'POST'])
def portfolio_activities_api(request, folder_id):
    """
    GET: List activities in a folder
    POST: Add activity to folder (teacher only)
    """
    try:
        folder = PortfolioFolder.objects.get(id=folder_id)
    except PortfolioFolder.DoesNotExist:
        return Response({'error': 'Folder not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        activities = folder.activities.all().order_by('-created_at')
        serializer = PortfolioActivitySerializer(activities, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if not request.user.is_authenticated or request.user.role != 'teacher':
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            data = request.data  # Use request.data instead of json.loads(request.body)
            print(f"Received data: {data}")  # Debug log
            print(f"Request user: {request.user}")
            print(f"Folder: {folder}")
            
            # Prepare data for serializer
            activity_data = {
                'folder': folder.id,
                'activity_type': data.get('activity_type', 'Quiz'),
                'title': data.get('title'),
                'description': data.get('description', ''),
                'due_date': data.get('due_date') if data.get('due_date') else None,
                'due_time': data.get('due_time') if data.get('due_time') else None,
                'file_path': data.get('file_path', ''),
                'scoring_criteria': data.get('scoring_criteria', '[]')  # Add scoring criteria
            }
            
            print(f"Activity data: {activity_data}")
            print(f"Scoring criteria received: {data.get('scoring_criteria')}")
            
            serializer = PortfolioActivitySerializer(data=activity_data)
            if serializer.is_valid():
                activity = serializer.save()
                
                # Notify all students about new activity (exclude admin)
                students = User.objects.filter(role='student').exclude(username='admin')
                
                # Build detailed message with due date/time info
                due_info = ""
                if activity.due_date:
                    from datetime import datetime, time as time_type
                    try:
                        # Handle both date objects and strings
                        if isinstance(activity.due_date, str):
                            # Parse string date
                            due_date_obj = datetime.strptime(activity.due_date, '%Y-%m-%d').date()
                            due_date_str = due_date_obj.strftime('%B %d, %Y')
                        else:
                            due_date_str = activity.due_date.strftime('%B %d, %Y')
                        
                        if activity.due_time:
                            # Convert time object to datetime for formatting
                            if isinstance(activity.due_time, time_type):
                                temp_datetime = datetime.combine(datetime.today(), activity.due_time)
                                due_time_str = temp_datetime.strftime('%I:%M %p')
                            else:
                                # If it's a string, try to parse it
                                due_time_str = str(activity.due_time)
                                if ':' in due_time_str and len(due_time_str) <= 8:
                                    parts = due_time_str.split(':')
                                    hour = int(parts[0])
                                    minute = int(parts[1])
                                    ampm = 'AM' if hour < 12 else 'PM'
                                    display_hour = hour if hour <= 12 else hour - 12
                                    if display_hour == 0:
                                        display_hour = 12
                                    due_time_str = f'{display_hour:02d}:{minute:02d} {ampm}'
                            due_info = f" Due: {due_date_str} at {due_time_str}"
                        else:
                            due_info = f" Due: {due_date_str}"
                    except Exception as e:
                        print(f"Error formatting due date/time: {e}")
                        due_info = f" Due: {activity.due_date}"
                
                for student in students:
                    create_notification(
                        recipient=student,
                        notification_type='activity_created',
                        title='New Activity Created',
                        message=f'New activity "{activity.title}" added to portfolio "{folder.name}".{due_info}',
                        activity=activity,
                        portfolio=folder
                    )
                
                print(f"Activity created successfully: {serializer.data}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(f"Serializer errors: {serializer.errors}")
                return Response({'error': 'Validation failed', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"Error creating activity: {str(e)}")
            print(error_trace)
            return Response({'error': str(e), 'details': error_trace}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def activity_detail_api(request, activity_id):
    """
    GET: Get activity details
    PUT: Update activity (teacher only)
    DELETE: Delete activity (teacher only)
    """
    try:
        activity = PortfolioActivity.objects.get(id=activity_id)
    except PortfolioActivity.DoesNotExist:
        return Response({'error': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PortfolioActivitySerializer(activity)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # Only teachers can update
        if not request.user.is_authenticated or request.user.role != 'teacher':
            return Response({'error': 'Only teachers can update activities'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            data = request.data
            print(f"Updating activity {activity_id} with data: {data}")
            
            # Track what changed
            changes = []
            old_due_date = activity.due_date
            old_due_time = activity.due_time
            
            # Update activity fields
            if data.get('title') and data.get('title') != activity.title:
                changes.append('title')
            activity.title = data.get('title', activity.title)
            
            if data.get('activity_type') and data.get('activity_type') != activity.activity_type:
                changes.append('type')
            activity.activity_type = data.get('activity_type', activity.activity_type)
            
            if data.get('description') and data.get('description') != activity.description:
                changes.append('description')
            activity.description = data.get('description', activity.description)
            
            # Check due date changes
            new_due_date = data.get('due_date')
            if new_due_date and str(new_due_date) != str(old_due_date):
                changes.append('due date')
            activity.due_date = new_due_date if new_due_date else activity.due_date
            
            # Check due time changes
            new_due_time = data.get('due_time')
            # Convert string time to proper format if needed
            if new_due_time and isinstance(new_due_time, str) and new_due_time.lower() != 'none':
                # Keep as string, Django will handle conversion
                pass
            elif new_due_time and new_due_time.lower() == 'none':
                new_due_time = None
            
            if str(new_due_time) != str(old_due_time):
                if new_due_time and not old_due_time:
                    changes.append('due time added')
                elif not new_due_time and old_due_time:
                    changes.append('due time removed')
                elif new_due_time and old_due_time:
                    changes.append('due time')
            activity.due_time = new_due_time if new_due_time else None
            
            if data.get('scoring_criteria') and data.get('scoring_criteria') != activity.scoring_criteria:
                changes.append('scoring criteria')
            activity.scoring_criteria = data.get('scoring_criteria', activity.scoring_criteria)
            
            activity.save()
            
            # Build notification message based on changes
            if changes:
                changes_text = ', '.join(changes)
                update_message = f'Activity "{activity.title}" has been updated. Changes: {changes_text}.'
            else:
                update_message = f'Activity "{activity.title}" has been updated.'
            
            # Add current due date/time info
            if activity.due_date:
                from datetime import datetime, time as time_type
                try:
                    # Handle both date objects and strings
                    if isinstance(activity.due_date, str):
                        # Parse string date
                        due_date_obj = datetime.strptime(activity.due_date, '%Y-%m-%d').date()
                        due_date_str = due_date_obj.strftime('%B %d, %Y')
                    else:
                        due_date_str = activity.due_date.strftime('%B %d, %Y')
                    
                    if activity.due_time:
                        # Convert time object to datetime for formatting
                        if isinstance(activity.due_time, time_type):
                            temp_datetime = datetime.combine(datetime.today(), activity.due_time)
                            due_time_str = temp_datetime.strftime('%I:%M %p')
                        else:
                            # If it's a string, try to parse it
                            due_time_str = str(activity.due_time)
                            if ':' in due_time_str and len(due_time_str) <= 8:
                                # Format like "18:28:00" or "18:28"
                                parts = due_time_str.split(':')
                                hour = int(parts[0])
                                minute = int(parts[1])
                                ampm = 'AM' if hour < 12 else 'PM'
                                display_hour = hour if hour <= 12 else hour - 12
                                if display_hour == 0:
                                    display_hour = 12
                                due_time_str = f'{display_hour:02d}:{minute:02d} {ampm}'
                        update_message += f' Due: {due_date_str} at {due_time_str}'
                    else:
                        update_message += f' Due: {due_date_str}'
                except Exception as e:
                    print(f"Error formatting due date/time: {e}")
                    update_message += f' Due: {activity.due_date}'
            
            # Notify all students about activity update (exclude admin)
            students = User.objects.filter(role='student').exclude(username='admin')
            for student in students:
                create_notification(
                    recipient=student,
                    notification_type='activity_updated',
                    title='Activity Updated',
                    message=update_message,
                    activity=activity
                )
            
            print(f"✅ Activity {activity_id} updated successfully")
            serializer = PortfolioActivitySerializer(activity)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"❌ Error updating activity: {str(e)}")
            print(error_trace)
            return Response({'error': str(e), 'details': error_trace}, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # Only teachers can delete
        if not request.user.is_authenticated or request.user.role != 'teacher':
            return Response({'error': 'Only teachers can delete activities'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            print(f"Deleting activity {activity_id}")
            activity_title = activity.title
            activity_type = activity.activity_type
            
            # Build detailed deletion message
            delete_message = f'Activity "{activity_title}" ({activity_type}) has been deleted'
            
            if activity.due_date:
                from datetime import datetime, time as time_type
                try:
                    # Handle both date objects and strings
                    if isinstance(activity.due_date, str):
                        # Parse string date
                        due_date_obj = datetime.strptime(activity.due_date, '%Y-%m-%d').date()
                        due_date_str = due_date_obj.strftime('%B %d, %Y')
                    else:
                        due_date_str = activity.due_date.strftime('%B %d, %Y')
                    
                    if activity.due_time:
                        # Convert time object to datetime for formatting
                        if isinstance(activity.due_time, time_type):
                            temp_datetime = datetime.combine(datetime.today(), activity.due_time)
                            due_time_str = temp_datetime.strftime('%I:%M %p')
                        else:
                            # If it's a string, try to parse it
                            due_time_str = str(activity.due_time)
                            if ':' in due_time_str and len(due_time_str) <= 8:
                                parts = due_time_str.split(':')
                                hour = int(parts[0])
                                minute = int(parts[1])
                                ampm = 'AM' if hour < 12 else 'PM'
                                display_hour = hour if hour <= 12 else hour - 12
                                if display_hour == 0:
                                    display_hour = 12
                                due_time_str = f'{display_hour:02d}:{minute:02d} {ampm}'
                        delete_message += f'. It was due on {due_date_str} at {due_time_str}.'
                    else:
                        delete_message += f'. It was due on {due_date_str}.'
                except Exception as e:
                    print(f"Error formatting due date/time: {e}")
                    delete_message += f'. It was due on {activity.due_date}.'
            else:
                delete_message += '.'
            
            # Notify all students about activity deletion (exclude admin)
            students = User.objects.filter(role='student').exclude(username='admin')
            for student in students:
                create_notification(
                    recipient=student,
                    notification_type='activity_deleted',
                    title='Activity Deleted',
                    message=delete_message
                )
            
            activity.delete()
            print(f"✅ Activity {activity_id} deleted successfully")
            return Response({'message': 'Activity deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"❌ Error deleting activity: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'POST'])
def activity_submissions_api(request, activity_id):
    """
    GET: List all submissions for an activity (teacher) or student's own submission
    POST: Submit work for an activity (student only)
    """
    try:
        activity = PortfolioActivity.objects.get(id=activity_id)
    except PortfolioActivity.DoesNotExist:
        return Response({'error': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        # Teachers see all submissions, students see only their own
        if request.user.role == 'teacher':
            submissions = StudentSubmission.objects.filter(activity=activity).order_by('-submitted_at')
            # Use lightweight serializer for teachers (excludes large file_path)
            from .serializer import StudentSubmissionListSerializer
            serializer = StudentSubmissionListSerializer(submissions, many=True)
        else:
            submissions = StudentSubmission.objects.filter(activity=activity, student=request.user)
            # Use full serializer for students (includes file_path for their own submissions)
            serializer = StudentSubmissionSerializer(submissions, many=True)
        
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Only students can submit
        if not request.user.is_authenticated or request.user.role != 'student':
            return Response({'error': 'Only students can submit work'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            data = request.data
            print(f"Received submission data: {data}")
            
            # Check if student already submitted
            existing_submission = StudentSubmission.objects.filter(
                activity=activity,
                student=request.user
            ).first()
            
            if existing_submission:
                # Update existing submission
                existing_submission.caption = data.get('caption', '')
                existing_submission.file_path = data.get('file_path', '')
                existing_submission.file_type = data.get('file_type', '')
                existing_submission.save()
                serializer = StudentSubmissionSerializer(existing_submission)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # Create new submission directly
                post_to_feed = data.get('post_to_feed', False)
                
                # Handle file upload - support both base64 and actual file
                file_path = data.get('file_path', '')
                file_obj = request.FILES.get('file')  # Check if actual file was uploaded
                
                submission = StudentSubmission.objects.create(
                    activity=activity,
                    student=request.user,
                    caption=data.get('caption', ''),
                    file=file_obj if file_obj else None,  # Store actual file if provided
                    file_path=file_path,  # Store base64 as fallback
                    file_type=data.get('file_type', ''),
                    status='unscored',
                    post_to_feed=post_to_feed,
                    approval_status='pending' if post_to_feed else 'approved'
                )
                
                # Notify teacher about new submission
                teacher = activity.folder.teacher
                create_notification(
                    recipient=teacher,
                    notification_type='submission_received',
                    title='New Submission Received',
                    message=f'{request.user.username} submitted work for "{activity.title}"',
                    submission=submission,
                    activity=activity
                )
                
                # If requesting approval, send additional notification
                if post_to_feed:
                    create_notification(
                        recipient=teacher,
                        notification_type='approval_requested',
                        title='Approval Requested',
                        message=f'{request.user.username} requested approval to post "{activity.title}" to newsfeed',
                        submission=submission,
                        activity=activity
                    )
                
                serializer = StudentSubmissionSerializer(submission)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"Error creating submission: {str(e)}")
            print(error_trace)
            return Response({'error': str(e), 'details': error_trace}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
def unscored_submissions_api(request):
    """
    GET: List all unscored submissions (teacher only)
    """
    if not request.user.is_authenticated or request.user.role != 'teacher':
        return Response({'error': 'Only teachers can view unscored submissions'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Get all unscored submissions (distinct to avoid duplicates)
        submissions = StudentSubmission.objects.filter(status='unscored').distinct().order_by('-submitted_at')
        
        # Use lightweight serializer for list (excludes large file_path)
        from .serializer import StudentSubmissionListSerializer
        serializer = StudentSubmissionListSerializer(submissions, many=True, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        print(f"Error fetching unscored submissions: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
def scored_submissions_api(request):
    """
    GET: List all scored submissions (teacher only)
    """
    if not request.user.is_authenticated or request.user.role != 'teacher':
        return Response({'error': 'Only teachers can view scored submissions'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Get all scored submissions (distinct to avoid duplicates)
        submissions = StudentSubmission.objects.filter(status='scored').distinct().order_by('-scored_at')
        
        # Use lightweight serializer for list (excludes large file_path)
        from .serializer import StudentSubmissionListSerializer
        serializer = StudentSubmissionListSerializer(submissions, many=True, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        print(f"Error fetching scored submissions: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['PUT'])
def score_submission_api(request, submission_id):
    """
    PUT: Score a submission (teacher only)
    """
    if not request.user.is_authenticated or request.user.role != 'teacher':
        return Response({'error': 'Only teachers can score submissions'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        submission = StudentSubmission.objects.get(id=submission_id)
    except StudentSubmission.DoesNotExist:
        return Response({'error': 'Submission not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        data = request.data
        submission.score = data.get('score')
        submission.feedback = data.get('feedback', '')
        submission.status = 'scored'
        submission.scored_at = timezone.now()
        submission.save()
        
        # Notify student about score
        create_notification(
            recipient=submission.student,
            notification_type='score_added',
            title='Your Work Has Been Scored',
            message=f'Your submission for "{submission.activity.title}" received a score of {submission.score}',
            submission=submission,
            activity=submission.activity
        )
        
        serializer = StudentSubmissionSerializer(submission)
        return Response(serializer.data)
    except Exception as e:
        print(f"Error scoring submission: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
def pending_approvals_api(request):
    """
    GET: List all pending feed approvals (teacher only)
    """
    if not request.user.is_authenticated or request.user.role != 'teacher':
        return Response({'error': 'Only teachers can view pending approvals'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Get all submissions that are marked for posting to feed and pending approval
        submissions = StudentSubmission.objects.filter(
            post_to_feed=True,
            approval_status='pending'
        ).order_by('-submitted_at')
        
        serializer = StudentSubmissionSerializer(submissions, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(f"Error fetching pending approvals: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['PUT'])
def approve_submission_api(request, submission_id):
    """
    PUT: Approve or reject a submission for feed posting (teacher only)
    """
    if not request.user.is_authenticated or request.user.role != 'teacher':
        return Response({'error': 'Only teachers can approve submissions'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        submission = StudentSubmission.objects.get(id=submission_id)
    except StudentSubmission.DoesNotExist:
        return Response({'error': 'Submission not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        from .models import NewsfeedPost
        
        data = request.data
        action = data.get('action')  # 'approve' or 'reject'
        
        if action == 'approve':
            submission.approval_status = 'approved'
            submission.save()
            
            # Notify student about approval
            create_notification(
                recipient=submission.student,
                notification_type='submission_approved',
                title='Submission Approved',
                message=f'Your submission for "{submission.activity.title}" has been approved and posted to the newsfeed',
                submission=submission,
                activity=submission.activity
            )
            
            # Create a newsfeed post if this submission was marked to post to feed
            if submission.post_to_feed:
                # Check if newsfeed post already exists for this submission
                existing_post = NewsfeedPost.objects.filter(original_submission=submission).first()
                
                if not existing_post:
                    # Create new newsfeed post
                    NewsfeedPost.objects.create(
                        student=submission.student,
                        student_name=submission.student.username,
                        caption=submission.caption or '',
                        file_path=submission.file_path,
                        file_type=submission.file_type,
                        activity_title=submission.activity.title if submission.activity else 'Sketch Pad',
                        activity_type=submission.activity.activity_type if submission.activity else 'Sketch',
                        original_submission=submission
                    )
                    print(f"Created newsfeed post for submission {submission_id}")
        elif action == 'reject':
            submission.approval_status = 'rejected'
            submission.save()
            
            # Get rejection reason and details from request
            rejection_reason = data.get('rejectionReason', '')
            rejection_details = data.get('rejectionDetails', '')
            
            # Create detailed rejection message
            activity_title = submission.activity.title if submission.activity else 'your submission'
            
            # Map rejection reason IDs to readable text
            reason_map = {
                'invalid': 'Invalid submission',
                'unrelated': 'Unrelated content',
                'disturbing': 'Inappropriate content',
                'lack_of_content': 'Insufficient content',
                'others': 'Other reasons'
            }
            
            reason_text = reason_map.get(rejection_reason, 'Not specified')
            
            # Build notification message
            if rejection_details:
                notification_message = f'Your submission for "{activity_title}" was not approved for the newsfeed. Reason: {reason_text}. Details: {rejection_details}'
            else:
                notification_message = f'Your submission for "{activity_title}" was not approved for the newsfeed. Reason: {reason_text}'
            
            # Notify student about rejection
            create_notification(
                recipient=submission.student,
                notification_type='submission_rejected',
                title='Submission Not Approved',
                message=notification_message,
                submission=submission,
                activity=submission.activity
            )
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = StudentSubmissionSerializer(submission)
        return Response(serializer.data)
    except Exception as e:
        print(f"Error approving submission: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
def newsfeed_api(request):
    """
    GET: Get all newsfeed posts
    """
    try:
        from .models import NewsfeedPost
        from .serializer import NewsfeedPostSerializer
        
        # Get all newsfeed posts
        posts = NewsfeedPost.objects.all().order_by('-posted_at')
        serializer = NewsfeedPostSerializer(posts, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(f"Error fetching newsfeed: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
def submission_detail_api(request, submission_id):
    """
    GET: Get full submission details including file_path (for viewing individual submission)
    """
    try:
        submission = StudentSubmission.objects.get(id=submission_id)
        serializer = StudentSubmissionSerializer(submission)
        return Response(serializer.data)
    except StudentSubmission.DoesNotExist:
        return Response({'error': 'Submission not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error fetching submission: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def notifications_api(request):
    """
    GET: Get all notifications for current user
    PUT: Mark notification(s) as read
    DELETE: Delete notification(s)
    """
    if not request.user.is_authenticated:
        print(f"❌ Notifications API - User not authenticated")
        return Response({'error': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        try:
            print(f"📬 Fetching notifications for user: {request.user.username} (role: {request.user.role})")
            notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
            print(f"📊 Found {notifications.count()} notifications")
            
            # Debug: Print first few notifications
            for notif in notifications[:3]:
                print(f"  - {notif.notification_type}: {notif.title}")
            
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(f"❌ Error fetching notifications: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'PUT':
        try:
            data = request.data
            notification_id = data.get('notification_id')
            mark_all = data.get('mark_all', False)
            
            if mark_all:
                # Mark all notifications as read
                Notification.objects.filter(recipient=request.user, is_read=False).update(
                    is_read=True,
                    read_at=timezone.now()
                )
                return Response({'message': 'All notifications marked as read'})
            elif notification_id:
                # Mark specific notification as read
                try:
                    notification = Notification.objects.get(id=notification_id, recipient=request.user)
                    notification.is_read = True
                    notification.read_at = timezone.now()
                    notification.save()
                    serializer = NotificationSerializer(notification)
                    return Response(serializer.data)
                except Notification.DoesNotExist:
                    return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'notification_id or mark_all required'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error updating notification: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        try:
            data = request.data
            notification_id = data.get('notification_id')
            delete_all = data.get('delete_all', False)
            
            if delete_all:
                # Delete all notifications for current user
                count = Notification.objects.filter(recipient=request.user).count()
                Notification.objects.filter(recipient=request.user).delete()
                print(f"🗑️ Deleted {count} notifications for user: {request.user.username}")
                return Response({'message': f'Deleted {count} notifications', 'count': count})
            elif notification_id:
                # Delete specific notification
                try:
                    notification = Notification.objects.get(id=notification_id, recipient=request.user)
                    notification.delete()
                    print(f"🗑️ Deleted notification {notification_id} for user: {request.user.username}")
                    return Response({'message': 'Notification deleted'})
                except Notification.DoesNotExist:
                    return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'notification_id or delete_all required'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"❌ Error deleting notification: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
def unread_notifications_count_api(request):
    """
    GET: Get count of unread notifications for current user
    """
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return Response({'count': count})
    except Exception as e:
        print(f"Error counting notifications: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def score_submission_api(request, submission_id):
    """
    POST: Score a student submission with multiple criteria
    Expected data:
    {
        "scores": {
            "creativity": 8,
            "creativity_max": 10,
            "technical_skill": 9,
            "technical_skill_max": 10,
            "requirements": 10,
            "requirements_max": 10
        },
        "feedback": "Great work!",
        "total_score": 27,
        "max_score": 30
    }
    """
    try:
        from .models import SubmissionScore
        
        submission = StudentSubmission.objects.get(id=submission_id)
        
        # Get scoring data from request
        score = request.data.get('score', 0)
        feedback = request.data.get('feedback', '')
        criteria_scores = request.data.get('criteria_scores', '[]')
        
        print(f"Scoring submission {submission_id}:")
        print(f"  Score: {score}")
        print(f"  Feedback: {feedback}")
        print(f"  Criteria scores: {criteria_scores}")
        
        # Update submission with score, feedback, and criteria scores
        submission.score = score
        submission.feedback = feedback
        submission.criteria_scores = criteria_scores  # Save the criteria scores JSON
        submission.status = 'scored'
        submission.scored_at = timezone.now()
        submission.save()
        
        print(f"✅ Submission {submission_id} marked as scored")
        
        # Check if there are any remarks and feedback for this submission
        has_remarks = Remark.objects.filter(submission=submission).exists()
        has_feedback = feedback and feedback.strip()
        
        # Send notification to student
        activity_title = submission.activity.title if submission.activity else 'your submission'
        
        # Create specific notification message based on what was added
        notification_parts = []
        
        if has_feedback and has_remarks:
            notification_message = f'Your submission for "{activity_title}" has been scored and includes feedback and output remarks. Check your outputs to view your score and feedback.'
        elif has_feedback:
            notification_message = f'Your submission for "{activity_title}" has been scored and includes feedback. Check your outputs to view your score and feedback.'
        elif has_remarks:
            notification_message = f'Your submission for "{activity_title}" has been scored and includes output remarks. Check your outputs to view your score and remarks.'
        else:
            notification_message = f'Your submission for "{activity_title}" has been scored. Check your outputs to view your score.'
        
        create_notification(
            recipient=submission.student,
            notification_type='score_added',
            title='Submission Scored',
            message=notification_message,
            submission=submission,
            activity=submission.activity
        )
        
        serializer = StudentSubmissionSerializer(submission)
        return Response({
            'message': 'Submission scored successfully',
            'submission': serializer.data
        }, status=status.HTTP_200_OK)
    except StudentSubmission.DoesNotExist:
        return Response({'error': 'Submission not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error scoring submission: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def sketch_submission_api(request):
    """
    POST: Submit a sketch to newsfeed (creates a submission without activity)
    """
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        data = request.data
        
        # Create a sketch submission (activity_id can be null or use a special "Sketch" activity)
        # For now, we'll create it without an activity or you can create a default "Sketch Pad" activity
        submission = StudentSubmission.objects.create(
            activity_id=None,  # No specific activity for sketches
            student=request.user,
            caption=data.get('caption', ''),
            file_path=data.get('file_path', ''),
            file_type='image',
            status='unscored',
            post_to_feed=True,
            approval_status='pending'
        )
        
        serializer = StudentSubmissionSerializer(submission)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(f"Error creating sketch submission: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'POST'])
def sketches_api(request):
    """
    GET: List all sketches for the authenticated student
    POST: Save a new sketch
    """
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        try:
            from .models import Sketch
            from .serializer import SketchSerializer
            
            # Get all sketches for the current student
            sketches = Sketch.objects.filter(student=request.user).order_by('-created_at')
            serializer = SketchSerializer(sketches, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(f"Error fetching sketches: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'POST':
        try:
            from .models import Sketch
            from .serializer import SketchSerializer
            
            data = request.data
            
            # Create new sketch
            sketch = Sketch.objects.create(
                student=request.user,
                title=data.get('title', 'Untitled Sketch'),
                image_data=data.get('image_data', '')
            )
            
            serializer = SketchSerializer(sketch)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Error saving sketch: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['DELETE'])
def sketch_delete_api(request, sketch_id):
    """
    DELETE: Delete a sketch
    """
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        from .models import Sketch
        
        sketch = Sketch.objects.get(id=sketch_id, student=request.user)
        sketch.delete()
        return Response({'message': 'Sketch deleted successfully'}, status=status.HTTP_200_OK)
    except Sketch.DoesNotExist:
        return Response({'error': 'Sketch not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error deleting sketch: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
def student_progress_list_api(request):
    """Get list of all students with their progress summary"""
    if not request.user.is_authenticated or request.user.role != 'teacher':
        return Response({'error': 'Teacher authentication required'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        from django.db.models import Count, Avg, Q
        
        # Get class name from query parameter
        class_name = request.GET.get('class', None)
        
        # Get all students, exclude admin users
        students = User.objects.filter(role='student').exclude(username='admin').order_by('username')
        
        # Filter by class if specified
        if class_name:
            # Get teacher's folders for this class
            teacher_folders = PortfolioFolder.objects.filter(teacher=request.user)
            class_folders = teacher_folders.filter(class_name=class_name)
            # Get students who have submissions in these folders
            student_ids = StudentSubmission.objects.filter(
                activity__folder__in=class_folders
            ).values_list('student_id', flat=True).distinct()
            students = students.filter(id__in=student_ids)
        
        student_list = []
        for student in students:
            # Get submissions count
            total_submissions = StudentSubmission.objects.filter(student=student).count()
            scored_submissions = StudentSubmission.objects.filter(student=student, status='scored').count()
            
            # Get average score
            avg_score = StudentSubmission.objects.filter(
                student=student, 
                status='scored',
                score__isnull=False
            ).aggregate(Avg('score'))['score__avg'] or 0
            
            student_list.append({
                'id': student.id,
                'student_id': str(student.id),  # Display database ID as student_id (e.g., "28")
                'name': student.get_full_name() or student.username,
                'username': student.username,
                'email': student.email,
                'total_outputs': total_submissions,
                'scored_outputs': scored_submissions,
                'average_score': round(avg_score, 2) if avg_score else 0,
            })
        
        return Response(student_list, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error fetching student progress list: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
def student_progress_detail_api(request, student_id):
    """Get detailed progress for a specific student"""
    if not request.user.is_authenticated or request.user.role != 'teacher':
        return Response({'error': 'Teacher authentication required'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Get student
        student = User.objects.get(id=student_id, role='student')
        
        # Get all submissions for this student
        submissions = StudentSubmission.objects.filter(
            student=student
        ).select_related('activity__folder').order_by('-submitted_at')
        
        # Group submissions by portfolio
        portfolio_data = {}
        for sub in submissions:
            if sub.activity and sub.activity.folder:
                folder_id = sub.activity.folder.id
                folder_name = sub.activity.folder.name
                
                if folder_id not in portfolio_data:
                    portfolio_data[folder_id] = {
                        'portfolio_id': folder_id,
                        'portfolio_name': folder_name,
                        'class_name': sub.activity.folder.class_name,
                        'activities': []
                    }
                
                portfolio_data[folder_id]['activities'].append({
                    'id': sub.id,
                    'activity_id': sub.activity.id,
                    'activity_title': sub.activity.title,
                    'activity_type': sub.activity.activity_type,
                    'score': sub.score,
                    'status': sub.status,
                    'feedback': sub.feedback,
                    'submitted_at': sub.submitted_at.isoformat() if sub.submitted_at else None,
                    'scored_at': sub.scored_at.isoformat() if sub.scored_at else None,
                })
        
        # Get sketch submissions (no activity)
        sketch_submissions = StudentSubmission.objects.filter(
            student=student,
            activity__isnull=True
        ).order_by('-submitted_at')
        
        response_data = {
            'student': {
                'id': student.id,
                'student_id': f'STD{str(student.id).zfill(3)}',
                'name': student.get_full_name() or student.username,
                'username': student.username,
                'email': student.email,
            },
            'portfolios': list(portfolio_data.values()),
            'sketches': [
                {
                    'id': sub.id,
                    'caption': sub.caption,
                    'score': sub.score,
                    'status': sub.status,
                    'feedback': sub.feedback,
                    'submitted_at': sub.submitted_at.isoformat() if sub.submitted_at else None,
                }
                for sub in sketch_submissions
            ],
            'summary': {
                'total_outputs': submissions.count(),
                'scored_outputs': submissions.filter(status='scored').count(),
                'unscored_outputs': submissions.filter(status='unscored').count(),
                'average_score': round(
                    submissions.filter(status='scored', score__isnull=False).aggregate(Avg('score'))['score__avg'] or 0,
                    2
                ),
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error fetching student progress detail: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Remark API Endpoints
@api_view(['GET', 'POST'])
def remark_list(request):
    """
    GET: List all remarks (filtered by teacher or student)
    POST: Create a new remark (teacher only)
    """
    if request.method == 'GET':
        # Get query parameters
        student_id = request.query_params.get('student_id')
        teacher_id = request.query_params.get('teacher_id')
        
        # Filter remarks - exclude submission-linked remarks for both teachers and students
        remarks = Remark.objects.filter(submission__isnull=True)
        
        if student_id:
            remarks = remarks.filter(student_id=student_id)
        
        if teacher_id:
            remarks = remarks.filter(teacher_id=teacher_id)
        
        # For students, only show their own remarks
        if request.user.role == 'student':
            remarks = remarks.filter(student=request.user)
        
        # For teachers, show remarks they created or received
        elif request.user.role == 'teacher':
            remarks = remarks.filter(Q(teacher=request.user) | Q(student=request.user))
        
        serializer = RemarkSerializer(remarks, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # Only teachers can create remarks
        if request.user.role != 'teacher':
            return Response({'error': 'Only teachers can create remarks'}, status=status.HTTP_403_FORBIDDEN)
        
        # Add teacher to the data
        data = request.data.copy()
        data['teacher'] = request.user.id
        
        serializer = RemarkSerializer(data=data)
        if serializer.is_valid():
            remark = serializer.save()
            
            # Create notification for the student
            try:
                student = User.objects.get(id=data['student'])
                create_notification(
                    recipient=student,
                    notification_type='remark_added',
                    title='New Remark Added',
                    message=f'{request.user.get_full_name() or request.user.username} added a new remark for you.'
                )
                print(f"Notification sent to student {student.username} for new remark")
            except Exception as e:
                print(f"Error creating notification: {e}")
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def remark_detail(request, pk):
    """
    GET: Retrieve a specific remark
    PUT: Update a remark (teacher only)
    DELETE: Delete a remark (teacher only)
    """
    try:
        remark = Remark.objects.get(pk=pk)
    except Remark.DoesNotExist:
        return Response({'error': 'Remark not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check permissions
    if request.user.role == 'student' and remark.student != request.user:
        return Response({'error': 'You do not have permission to view this remark'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        serializer = RemarkSerializer(remark)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        # Only the teacher who created the remark can edit it
        if request.user.role != 'teacher' or remark.teacher != request.user:
            return Response({'error': 'You do not have permission to edit this remark'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = RemarkSerializer(remark, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            # Create notification for the student
            try:
                create_notification(
                    recipient=remark.student,
                    notification_type='remark_updated',
                    title='Remark Updated',
                    message=f'{request.user.get_full_name() or request.user.username} updated a remark for you.'
                )
                print(f"Notification sent to student {remark.student.username} for updated remark")
            except Exception as e:
                print(f"Error creating notification: {e}")
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # Only the teacher who created the remark can delete it
        if request.user.role != 'teacher' or remark.teacher != request.user:
            return Response({'error': 'You do not have permission to delete this remark'}, status=status.HTTP_403_FORBIDDEN)
        
        # Store student info before deleting
        student = remark.student
        teacher_name = request.user.get_full_name() or request.user.username
        
        remark.delete()
        
        # Create notification for the student
        try:
            create_notification(
                recipient=student,
                notification_type='remark_deleted',
                title='Remark Deleted',
                message=f'{teacher_name} deleted a remark.'
            )
            print(f"Notification sent to student {student.username} for deleted remark")
        except Exception as e:
            print(f"Error creating notification: {e}")
        
        return Response({'message': 'Remark deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def mark_remark_read(request, pk):
    """
    Mark a remark as read for the current user (both students and teachers can mark remarks as read for themselves)
    """
    try:
        remark = Remark.objects.get(pk=pk)
    except Remark.DoesNotExist:
        return Response({'error': 'Remark not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Create or get the read status for this user
    read_status, created = RemarkReadStatus.objects.get_or_create(
        remark=remark,
        user=request.user
    )
    
    if created:
        print(f"User {request.user.username} marked remark {pk} as read")
    else:
        print(f"User {request.user.username} already marked remark {pk} as read")
    
    serializer = RemarkSerializer(remark, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


# Submission Remark API Endpoints
@csrf_exempt
@api_view(['GET', 'POST'])
def submission_remarks_api(request, submission_id):
    """
    GET: Get remarks for a specific submission
    POST: Add a remark to a submission (teacher only)
    """
    try:
        submission = StudentSubmission.objects.get(pk=submission_id)
    except StudentSubmission.DoesNotExist:
        return Response({'error': 'Submission not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        # Get all remarks for this submission
        remarks = Remark.objects.filter(submission=submission).order_by('-created_at')
        serializer = RemarkSerializer(remarks, many=True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Only teachers can add remarks
        if request.user.role != 'teacher':
            return Response({'error': 'Only teachers can add remarks'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        text = data.get('text', '').strip()
        
        if not text:
            return Response({'error': 'Remark text is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the remark
        remark = Remark.objects.create(
            teacher=request.user,
            student=submission.student,
            submission=submission,
            text=text
        )
        
        # Send notification to student
        activity_title = submission.activity.title if submission.activity else 'your submission'
        create_notification(
            recipient=submission.student,
            notification_type='remark_added',
            title='New Output Remark',
            message=f'{request.user.username} added a remark on {activity_title}',
            remark=remark,
            submission=submission
        )
        
        serializer = RemarkSerializer(remark, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(['PUT', 'DELETE'])
def submission_remark_detail_api(request, submission_id, remark_id):
    """
    PUT: Update a remark (teacher only)
    DELETE: Delete a remark (teacher only)
    """
    try:
        submission = StudentSubmission.objects.get(pk=submission_id)
        remark = Remark.objects.get(pk=remark_id, submission=submission)
    except StudentSubmission.DoesNotExist:
        return Response({'error': 'Submission not found'}, status=status.HTTP_404_NOT_FOUND)
    except Remark.DoesNotExist:
        return Response({'error': 'Remark not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Only the teacher who created the remark can modify it
    if request.user != remark.teacher:
        return Response({'error': 'You can only modify your own remarks'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'PUT':
        data = request.data
        text = data.get('text', '').strip()
        
        if not text:
            return Response({'error': 'Remark text is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        remark.text = text
        remark.save()
        
        # Send notification to student about update
        activity_title = submission.activity.title if submission.activity else 'your submission'
        create_notification(
            recipient=submission.student,
            notification_type='remark_updated',
            title='Output Remark Updated',
            message=f'{request.user.username} updated a remark on {activity_title}',
            remark=remark,
            submission=submission
        )
        
        serializer = RemarkSerializer(remark, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        # Store info before deletion for notification
        student = submission.student
        activity_title = submission.activity.title if submission.activity else 'your submission'
        teacher_name = request.user.username
        
        remark.delete()
        
        # Send notification to student about deletion
        create_notification(
            recipient=student,
            notification_type='remark_deleted',
            title='Output Remark Deleted',
            message=f'{teacher_name} deleted a remark on {activity_title}',
            submission=submission
        )
        
        return Response({'message': 'Remark deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET'])
def student_submission_remarks_api(request):
    """
    GET: Get all remarks for the current student's submissions
    """
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        # Get all submissions for this student
        submissions = StudentSubmission.objects.filter(student=request.user)
        
        # Get all remarks for these submissions
        all_remarks = []
        for submission in submissions:
            remarks = Remark.objects.filter(submission=submission).order_by('-created_at')
            for remark in remarks:
                serializer = RemarkSerializer(remark, context={'request': request})
                remark_data = serializer.data
                # Add submission info
                remark_data['submission_id'] = submission.id
                remark_data['activity_title'] = submission.activity.title if submission.activity else 'Activity'
                remark_data['activity_type'] = submission.activity.activity_type if submission.activity else 'General'
                remark_data['submission_score'] = submission.score
                all_remarks.append(remark_data)
        
        return Response(all_remarks)
    except Exception as e:
        print(f"Error fetching student submission remarks: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def request_portfolio_compilation_api(request):
    """
    POST: Teacher requests portfolio compilation for a class
    Creates notifications for all students in the class
    """
    if not request.user.is_authenticated or request.user.role != 'teacher':
        return Response({'error': 'Teacher authentication required'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        data = request.data
        class_name = data.get('class_name')
        
        print(f"📋 Portfolio compilation request for class: {class_name}")
        
        if not class_name:
            return Response({'error': 'class_name is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create or update compilation request for this class
        print(f"Creating/updating compilation request...")
        compilation_request, created = PortfolioCompilationRequest.objects.get_or_create(
            class_name=class_name,
            requested_by=request.user,
            defaults={'is_active': True}
        )
        print(f"Compilation request {'created' if created else 'updated'}: {compilation_request.id}")
        
        if not created:
            # Update existing request
            compilation_request.is_active = True
            compilation_request.requested_at = timezone.now()
            compilation_request.save()
        
        # Get all students (not just those with submissions)
        # This ensures all students in the system get notified
        students = User.objects.filter(role='student').exclude(username='admin')
        
        print(f"📢 Found {students.count()} students to notify")
        
        # Create notifications for all students
        notifications_created = 0
        for student in students:
            # Check if notification already exists for this student
            existing_notification = Notification.objects.filter(
                recipient=student,
                notification_type='portfolio_compilation',
                title__contains=class_name
            ).first()
            
            if not existing_notification:
                notification = create_notification(
                    recipient=student,
                    notification_type='portfolio_compilation',
                    title=f'Portfolio Compilation - {class_name}',
                    message=f'Your teacher has asked you to start compiling your portfolio for {class_name}.'
                )
                if notification:
                    notifications_created += 1
                    print(f"✅ Notified student: {student.username}")
                else:
                    print(f"❌ Failed to notify student: {student.username}")
            else:
                print(f"⏭️ Skipped {student.username} - already has notification")
        
        return Response({
            'message': 'Portfolio compilation request sent successfully',
            'class_name': class_name,
            'students_notified': notifications_created,
            'request_id': compilation_request.id
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        import traceback
        print(f"❌ Error requesting portfolio compilation: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET', 'DELETE'])
def check_portfolio_compilation_status_api(request, class_name):
    """
    GET: Check if portfolio compilation has been requested for a class
    DELETE: Drop/cancel portfolio compilation request for a class (teacher only)
    """
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'GET':
        try:
            # Check if there's an active compilation request for this class
            compilation_request = PortfolioCompilationRequest.objects.filter(
                class_name=class_name,
                is_active=True
            ).first()
            
            if compilation_request:
                # Also check if the student has a notification for this
                has_notification = Notification.objects.filter(
                    recipient=request.user,
                    notification_type='portfolio_compilation',
                    title__contains=class_name
                ).exists()
                
                return Response({
                    'compilation_requested': True,
                    'requested_at': compilation_request.requested_at,
                    'has_notification': has_notification
                })
            else:
                return Response({
                    'compilation_requested': False,
                    'has_notification': False
                })
                
        except Exception as e:
            print(f"Error checking portfolio compilation status: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'DELETE':
        # Only teachers can delete compilation requests
        if request.user.role != 'teacher':
            return Response({'error': 'Teacher authentication required'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            print(f"🗑️ Dropping portfolio compilation for class: {class_name}")
            
            # Find and deactivate the compilation request
            compilation_request = PortfolioCompilationRequest.objects.filter(
                class_name=class_name,
                requested_by=request.user,
                is_active=True
            ).first()
            
            if not compilation_request:
                return Response({'error': 'No active compilation request found'}, status=status.HTTP_404_NOT_FOUND)
            
            # Deactivate the request
            compilation_request.is_active = False
            compilation_request.save()
            
            # Delete all portfolio envelopes for this class
            from .models import PortfolioEnvelope
            envelopes_deleted = PortfolioEnvelope.objects.filter(class_name=class_name).delete()[0]
            print(f"🗑️ Deleted {envelopes_deleted} portfolio envelopes")
            
            # Delete old compilation notifications
            deleted_count = Notification.objects.filter(
                notification_type='portfolio_compilation',
                title__contains=class_name
            ).delete()[0]
            
            print(f"🗑️ Deleted {deleted_count} old notifications")
            
            # Get all students to notify about cancellation
            students = User.objects.filter(role='student').exclude(username='admin')
            
            print(f"📢 Notifying {students.count()} students about cancellation")
            
            # Notify students about cancellation
            students_notified = 0
            for student in students:
                notification = create_notification(
                    recipient=student,
                    notification_type='portfolio_compilation',
                    title=f'Portfolio Compilation Cancelled - {class_name}',
                    message=f'The portfolio compilation for {class_name} has been cancelled by your teacher.'
                )
                if notification:
                    students_notified += 1
                    print(f"✅ Notified {student.username} about cancellation")
                else:
                    print(f"❌ Failed to notify {student.username}")
            
            print(f"✅ Compilation request deactivated, {envelopes_deleted} envelopes deleted, {deleted_count} notifications deleted, {students_notified} students notified")
            
            return Response({
                'message': 'Portfolio compilation request dropped successfully',
                'class_name': class_name,
                'envelopes_deleted': envelopes_deleted,
                'notifications_deleted': deleted_count,
                'students_notified': students_notified
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            import traceback
            print(f"❌ Error dropping portfolio compilation: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def create_portfolio_envelope_api(request):
    """Create a portfolio envelope for a student"""
    try:
        from .models import PortfolioEnvelope
        
        print(f"📬 Creating portfolio envelope for user: {request.user.username}")
        
        # Get data from request
        title = request.data.get('title')
        student_name = request.data.get('student_name')
        class_name = request.data.get('class_name')
        color = request.data.get('color', '#4F46E5')
        pattern = request.data.get('pattern', 'solid')
        
        # Validate required fields
        if not all([title, student_name, class_name]):
            return Response({
                'error': 'Missing required fields: title, student_name, class_name'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create or update envelope
        envelope, created = PortfolioEnvelope.objects.update_or_create(
            student=request.user,
            class_name=class_name,
            defaults={
                'title': title,
                'student_name': student_name,
                'color': color,
                'pattern': pattern
            }
        )
        
        action = 'created' if created else 'updated'
        print(f"✅ Portfolio envelope {action} for {request.user.username} in {class_name}")
        
        # Notify teacher about the envelope creation/update
        try:
            # Find the teacher who requested the compilation for this class
            from .models import PortfolioCompilationRequest
            compilation_request = PortfolioCompilationRequest.objects.filter(
                class_name=class_name,
                is_active=True
            ).first()
            
            if compilation_request and compilation_request.requested_by:
                teacher = compilation_request.requested_by
                
                # Create notification for teacher
                notification_title = f'Portfolio Envelope {"Created" if created else "Updated"} - {class_name}'
                notification_message = f'{student_name} has {"created" if created else "updated"} their portfolio envelope for {class_name}.'
                
                notification = create_notification(
                    recipient=teacher,
                    notification_type='portfolio_envelope',
                    title=notification_title,
                    message=notification_message
                )
                
                if notification:
                    print(f"✅ Notified teacher {teacher.username} about envelope {action}")
                else:
                    print(f"❌ Failed to notify teacher {teacher.username}")
            else:
                print(f"⚠️ No active compilation request found for {class_name}")
                
        except Exception as notify_error:
            print(f"⚠️ Error notifying teacher: {str(notify_error)}")
            # Don't fail the envelope creation if notification fails
        
        return Response({
            'message': f'Portfolio envelope {action} successfully',
            'envelope': {
                'id': envelope.id,
                'title': envelope.title,
                'student_name': envelope.student_name,
                'class_name': envelope.class_name,
                'color': envelope.color,
                'pattern': envelope.pattern,
                'created_at': envelope.created_at.isoformat()
            }
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        
    except Exception as e:
        import traceback
        print(f"❌ Error creating portfolio envelope: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
def get_student_envelope_api(request, class_name):
    """Get the student's own portfolio envelope for a class"""
    try:
        from .models import PortfolioEnvelope
        
        print(f"📋 Fetching portfolio envelope for student: {request.user.username} in class: {class_name}")
        
        # Get the student's envelope for this class
        try:
            envelope = PortfolioEnvelope.objects.get(
                student=request.user,
                class_name=class_name
            )
            
            return Response({
                'envelope': {
                    'id': envelope.id,
                    'title': envelope.title,
                    'student_name': envelope.student_name,
                    'class_name': envelope.class_name,
                    'color': envelope.color,
                    'pattern': envelope.pattern,
                    'created_at': envelope.created_at.isoformat(),
                    'updated_at': envelope.updated_at.isoformat()
                }
            }, status=status.HTTP_200_OK)
            
        except PortfolioEnvelope.DoesNotExist:
            return Response({
                'error': 'No portfolio envelope found for this class'
            }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        import traceback
        print(f"❌ Error fetching student envelope: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
def get_student_portfolio_activities_api(request, class_name):
    """Get all activities (submitted and missing) for a student's portfolio"""
    try:
        from .models import PortfolioActivity, StudentSubmission, PortfolioFolder
        
        print(f"📚 Fetching portfolio activities for student: {request.user.username} in class: {class_name}")
        
        # Get all portfolio folders for this class
        folders = PortfolioFolder.objects.filter(class_name=class_name)
        
        activity_list = []
        for folder in folders:
            # Get all activities in this folder
            activities = PortfolioActivity.objects.filter(folder=folder).order_by('created_at')
            
            for activity in activities:
                # Check if student has submitted this activity
                submission = StudentSubmission.objects.filter(
                    activity=activity,
                    student=request.user
                ).first()
                
                # Get submission file path
                submission_file = None
                if submission:
                    if submission.file:
                        # Use the FileField URL
                        submission_file = submission.file.url if submission.file else None
                    elif submission.file_path:
                        # Fallback to file_path for base64 or legacy data
                        submission_file = submission.file_path
                
                activity_data = {
                    'id': activity.id,
                    'title': activity.title,
                    'description': activity.description,
                    'due_date': activity.due_date.isoformat() if activity.due_date else None,
                    'due_time': activity.due_time.strftime('%H:%M') if activity.due_time else None,
                    'created_at': activity.created_at.isoformat(),
                    'activity_type': activity.activity_type,
                    'has_submission': submission is not None,
                    'submission_id': submission.id if submission else None,
                    'submission_date': submission.submitted_at.isoformat() if submission else None,
                    'submission_file': submission_file,
                    'submission_caption': submission.caption if submission else None,
                    'submission_score': submission.score if submission else None,
                    'submission_feedback': submission.feedback if submission else None,
                    'submission_status': 'submitted' if submission else 'missing',
                    'folder_name': folder.name
                }
                
                activity_list.append(activity_data)
        
        # Separate submitted and missing activities
        submitted_activities = [a for a in activity_list if a['has_submission']]
        missing_activities = [a for a in activity_list if not a['has_submission']]
        
        print(f"✅ Found {len(submitted_activities)} submitted and {len(missing_activities)} missing activities")
        
        return Response({
            'all_activities': activity_list,
            'submitted_activities': submitted_activities,
            'missing_activities': missing_activities,
            'total_count': len(activity_list),
            'submitted_count': len(submitted_activities),
            'missing_count': len(missing_activities)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        import traceback
        print(f"❌ Error fetching portfolio activities: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
def get_portfolio_envelopes_api(request, class_name):
    """Get all portfolio envelopes for a class (teacher only)"""
    try:
        from .models import PortfolioEnvelope
        
        print(f"📋 Fetching portfolio envelopes for class: {class_name}")
        
        # Check if user is a teacher
        if request.user.role != 'teacher':
            return Response({
                'error': 'Only teachers can view portfolio envelopes'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Get all envelopes for this class
        envelopes = PortfolioEnvelope.objects.filter(class_name=class_name).select_related('student')
        
        envelope_list = []
        for envelope in envelopes:
            envelope_list.append({
                'id': envelope.id,
                'student_id': envelope.student.id,
                'student_name': envelope.student_name,
                'student_username': envelope.student.username,
                'id_number': envelope.student.id_number or envelope.student.username,  # Use actual ID number or fallback to username
                'title': envelope.title,
                'color': envelope.color,
                'pattern': envelope.pattern,
                'created_at': envelope.created_at.isoformat(),
                'date_created': envelope.created_at.strftime('%b %d, %Y'),
                'time_created': envelope.created_at.strftime('%I:%M %p')
            })
        
        print(f"✅ Found {len(envelope_list)} portfolio envelopes for {class_name}")
        
        return Response({
            'envelopes': envelope_list,
            'count': len(envelope_list)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        import traceback
        print(f"❌ Error fetching portfolio envelopes: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
