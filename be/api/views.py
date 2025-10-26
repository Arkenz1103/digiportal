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
from .models import User, PortfolioFolder, PortfolioActivity, StudentSubmission, Notification, Remark, RemarkReadStatus, PortfolioCompilationRequest, NewsfeedPost, PostLike, PostComment
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
            
            # Check for duplicate folder name for this teacher and class (case-sensitive)
            existing_folder = PortfolioFolder.objects.filter(
                teacher=request.user,
                name=name,  # Case-sensitive comparison (exact match)
                class_name=class_name
            ).first()
            
            if existing_folder:
                return Response({
                    'error': 'Duplicate folder name',
                    'detail': f'A folder with the exact name "{name}" already exists in {class_name}. Please choose a different name.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
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
            new_name = data.get('name', folder.name)
            
            # Check for duplicate folder name (excluding the current folder, case-sensitive)
            if new_name != folder.name:  # Only check if name is being changed
                existing_folder = PortfolioFolder.objects.filter(
                    teacher=request.user,
                    name=new_name,  # Case-sensitive comparison (exact match)
                    class_name=folder.class_name
                ).exclude(id=folder.id).first()
                
                if existing_folder:
                    return Response({
                        'error': 'Duplicate folder name',
                        'detail': f'A folder with the exact name "{new_name}" already exists in {folder.class_name}. Please choose a different name.'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            folder.name = new_name
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
        
        # Check if folder has any activities
        activity_count = folder.activities.count()
        if activity_count > 0:
            return Response({
                'error': 'Cannot delete folder with activities',
                'detail': f'This folder contains {activity_count} activity/activities. Please delete all activities first before deleting the folder.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
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
        # Teachers see all activities, students only see published ones
        if request.user.is_authenticated and request.user.role == 'teacher':
            activities = folder.activities.all().order_by('-created_at')
        else:
            # Students only see published activities
            activities = folder.activities.filter(is_published=True).order_by('-created_at')
        
        serializer = PortfolioActivitySerializer(activities, many=True)
        activities_data = serializer.data
        
        # For students, add submission status and is_late flag
        if request.user.is_authenticated and request.user.role == 'student':
            from django.utils import timezone
            from datetime import datetime, time as dt_time
            
            for activity_data in activities_data:
                activity_id = activity_data['id']
                
                # Check if student has submitted
                submission = StudentSubmission.objects.filter(
                    activity_id=activity_id,
                    student=request.user
                ).exclude(status='draft').first()
                
                if submission:
                    activity_data['hasSubmitted'] = True
                    activity_data['isLate'] = submission.is_late
                    activity_data['submittedAt'] = submission.submitted_at
                else:
                    activity_data['hasSubmitted'] = False
                    activity_data['isLate'] = False
        
        return Response(activities_data)
    
    elif request.method == 'POST':
        if not request.user.is_authenticated or request.user.role != 'teacher':
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            data = request.data  # Use request.data instead of json.loads(request.body)
            print(f"Received data: {data}")  # Debug log
            print(f"Request user: {request.user}")
            print(f"Folder: {folder}")
            
            # Validate required fields
            if not data.get('title') or not data.get('title').strip():
                return Response(
                    {'error': 'Activity Title is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not data.get('due_date'):
                return Response(
                    {'error': 'Due Date is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not data.get('due_time'):
                return Response(
                    {'error': 'Due Time is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate due date is not in the past
            from datetime import date, datetime, time as time_type
            if data.get('due_date'):
                try:
                    # Parse the due date
                    if isinstance(data.get('due_date'), str):
                        due_date_obj = datetime.strptime(data.get('due_date'), '%Y-%m-%d').date()
                    else:
                        due_date_obj = data.get('due_date')
                    
                    # Check if date is in the past
                    today = date.today()
                    if due_date_obj < today:
                        return Response(
                            {'error': 'Due date cannot be in the past. Please select today or a future date.'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    # If date is today, validate time is not in the past (time is now required)
                    if due_date_obj == today:
                        try:
                            # Parse the due time
                            if isinstance(data.get('due_time'), str):
                                time_parts = data.get('due_time').split(':')
                                due_time_obj = time_type(int(time_parts[0]), int(time_parts[1]))
                            else:
                                due_time_obj = data.get('due_time')
                            
                            # Check if time is in the past
                            current_time = datetime.now().time()
                            if due_time_obj < current_time:
                                return Response(
                                    {'error': 'Due time cannot be in the past. Please select a future time.'},
                                    status=status.HTTP_400_BAD_REQUEST
                                )
                        except (ValueError, IndexError) as e:
                            print(f"Error parsing time: {e}")
                            return Response(
                                {'error': 'Invalid time format. Please use HH:MM format.'},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                except (ValueError, TypeError) as e:
                    print(f"Error parsing date: {e}")
                    return Response(
                        {'error': 'Invalid date format. Please use YYYY-MM-DD format.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Validate scoring criteria
            import json
            scoring_criteria_str = data.get('scoring_criteria', '[]')
            try:
                scoring_criteria = json.loads(scoring_criteria_str) if isinstance(scoring_criteria_str, str) else scoring_criteria_str
                
                # Check if at least one criterion exists
                if not scoring_criteria or len(scoring_criteria) == 0:
                    return Response(
                        {'error': 'At least one scoring criterion is required'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Validate each criterion
                for criterion in scoring_criteria:
                    if not criterion.get('name') or not criterion.get('name').strip():
                        return Response(
                            {'error': 'Criterion name is required'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    max_score = criterion.get('maxScore')
                    if max_score is None or max_score == '':
                        return Response(
                            {'error': 'Criterion score is required'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    try:
                        max_score_int = int(max_score)
                        if max_score_int <= 0:
                            return Response(
                                {'error': 'Criterion score must be greater than 0'},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                    except (ValueError, TypeError):
                        return Response(
                            {'error': 'Criterion score must be a valid number'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
            except json.JSONDecodeError:
                return Response(
                    {'error': 'Invalid scoring criteria format'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
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
                
                # Activity is created as draft (is_published=False by default)
                # No notifications sent until teacher publishes it
                
                print(f"Activity created successfully as draft: {serializer.data}")
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
            
            # Check if activity due date has passed or is too close to deadline
            from datetime import date, datetime, time as time_type, timedelta
            
            # Configuration: Minimum hours before due date/time to allow editing
            EDIT_CUTOFF_HOURS = 3  # Teachers must edit at least 3 hours before deadline
            
            if activity.due_date:
                # Combine due date and time into a single datetime
                activity_due_date = activity.due_date if isinstance(activity.due_date, date) else datetime.strptime(str(activity.due_date), '%Y-%m-%d').date()
                
                if activity.due_time:
                    activity_time = activity.due_time if isinstance(activity.due_time, time_type) else datetime.strptime(str(activity.due_time), '%H:%M:%S').time()
                    due_datetime = datetime.combine(activity_due_date, activity_time)
                else:
                    # If no time specified, use end of day (23:59:59)
                    due_datetime = datetime.combine(activity_due_date, time_type(23, 59, 59))
                
                # Get current datetime
                now = datetime.now()
                
                # Calculate time remaining until deadline
                time_remaining = due_datetime - now
                
                # If deadline has passed
                if time_remaining.total_seconds() <= 0:
                    return Response(
                        {'error': 'Cannot edit activity after the due date/time has passed.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # If less than EDIT_CUTOFF_HOURS remaining
                cutoff_timedelta = timedelta(hours=EDIT_CUTOFF_HOURS)
                if time_remaining < cutoff_timedelta:
                    hours_remaining = time_remaining.total_seconds() / 3600
                    return Response(
                        {'error': f'Cannot edit activity within {EDIT_CUTOFF_HOURS} hours of the deadline. Only {hours_remaining:.1f} hours remaining.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Validate required fields if provided
            if 'title' in data and (not data.get('title') or not data.get('title').strip()):
                return Response(
                    {'error': 'Activity Title cannot be empty'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if 'due_date' in data and not data.get('due_date'):
                return Response(
                    {'error': 'Due Date cannot be empty'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if 'due_time' in data and not data.get('due_time'):
                return Response(
                    {'error': 'Due Time cannot be empty'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate due date is not in the past
            from datetime import date, datetime, time as time_type
            if data.get('due_date'):
                try:
                    # Parse the due date
                    if isinstance(data.get('due_date'), str):
                        due_date_obj = datetime.strptime(data.get('due_date'), '%Y-%m-%d').date()
                    else:
                        due_date_obj = data.get('due_date')
                    
                    # Check if date is in the past
                    today = date.today()
                    if due_date_obj < today:
                        return Response(
                            {'error': 'Due date cannot be in the past. Please select today or a future date.'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    # If date is today, validate time is not in the past
                    if due_date_obj == today and data.get('due_time'):
                        try:
                            # Parse the due time
                            if isinstance(data.get('due_time'), str):
                                time_parts = data.get('due_time').split(':')
                                due_time_obj = time_type(int(time_parts[0]), int(time_parts[1]))
                            else:
                                due_time_obj = data.get('due_time')
                            
                            # Check if time is in the past
                            current_time = datetime.now().time()
                            if due_time_obj < current_time:
                                return Response(
                                    {'error': 'Due time cannot be in the past. Please select a future time.'},
                                    status=status.HTTP_400_BAD_REQUEST
                                )
                        except (ValueError, IndexError) as e:
                            print(f"Error parsing time: {e}")
                            return Response(
                                {'error': 'Invalid time format. Please use HH:MM format.'},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                except (ValueError, TypeError) as e:
                    print(f"Error parsing date: {e}")
                    return Response(
                        {'error': 'Invalid date format. Please use YYYY-MM-DD format.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
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
            
            # Validate scoring criteria if provided
            if data.get('scoring_criteria'):
                import json
                scoring_criteria_str = data.get('scoring_criteria')
                try:
                    scoring_criteria = json.loads(scoring_criteria_str) if isinstance(scoring_criteria_str, str) else scoring_criteria_str
                    
                    # Check if at least one criterion exists
                    if not scoring_criteria or len(scoring_criteria) == 0:
                        return Response(
                            {'error': 'At least one scoring criterion is required'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    # Validate each criterion
                    for criterion in scoring_criteria:
                        if not criterion.get('name') or not criterion.get('name').strip():
                            return Response(
                                {'error': 'Criterion name is required'},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                        
                        max_score = criterion.get('maxScore')
                        if max_score is None or max_score == '':
                            return Response(
                                {'error': 'Criterion score is required'},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                        
                        try:
                            max_score_int = int(max_score)
                            if max_score_int <= 0:
                                return Response(
                                    {'error': 'Criterion score must be greater than 0'},
                                    status=status.HTTP_400_BAD_REQUEST
                                )
                        except (ValueError, TypeError):
                            return Response(
                                {'error': 'Criterion score must be a valid number'},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                except json.JSONDecodeError:
                    return Response(
                        {'error': 'Invalid scoring criteria format'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                if data.get('scoring_criteria') != activity.scoring_criteria:
                    changes.append('scoring criteria')
                activity.scoring_criteria = data.get('scoring_criteria')
            
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
@api_view(['POST'])
def publish_activity_api(request, activity_id):
    """
    POST: Publish an activity to make it visible to students (teacher only)
    """
    try:
        activity = PortfolioActivity.objects.get(id=activity_id)
    except PortfolioActivity.DoesNotExist:
        return Response({'error': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Only teachers can publish
    if not request.user.is_authenticated or request.user.role != 'teacher':
        return Response({'error': 'Only teachers can publish activities'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Check if already published (but allow re-publishing if it was retracted)
        if activity.is_published:
            return Response({'error': 'Activity is already published'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Publish or re-publish the activity
        from django.utils import timezone
        was_retracted = activity.published_at is None  # Check if this is a first-time publish or re-publish
        
        activity.is_published = True
        activity.published_at = timezone.now()
        activity.save()
        
        action = "re-published" if not was_retracted else "published"
        print(f"✅ Activity {activity_id} {action} successfully")
        
        # Notify all students about the new activity
        students = User.objects.filter(role='student').exclude(username='admin')
        
        # Build detailed message with due date/time info
        due_info = ""
        if activity.due_date:
            from datetime import datetime, time as time_type
            try:
                # Handle both date objects and strings
                if isinstance(activity.due_date, str):
                    due_date_obj = datetime.strptime(activity.due_date, '%Y-%m-%d').date()
                    due_date_str = due_date_obj.strftime('%B %d, %Y')
                else:
                    due_date_str = activity.due_date.strftime('%B %d, %Y')
                
                if activity.due_time:
                    # Convert time object to datetime for formatting
                    if isinstance(activity.due_time, str):
                        time_parts = activity.due_time.split(':')
                        time_obj = time_type(int(time_parts[0]), int(time_parts[1]))
                    else:
                        time_obj = activity.due_time
                    
                    # Format time in 12-hour format
                    time_str = datetime.combine(datetime.today(), time_obj).strftime('%I:%M %p')
                    due_info = f" Due: {due_date_str} at {time_str}"
                else:
                    due_info = f" Due: {due_date_str}"
            except Exception as e:
                print(f"Error formatting due date/time: {e}")
                due_info = f" Due: {activity.due_date}"
        
        for student in students:
            create_notification(
                recipient=student,
                notification_type='activity_created',
                title='New Activity Published',
                message=f'New activity "{activity.title}" has been published in portfolio "{activity.folder.name}".{due_info}',
                activity=activity,
                portfolio=activity.folder
            )
        
        serializer = PortfolioActivitySerializer(activity)
        return Response({
            'message': 'Activity published successfully',
            'activity': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error publishing activity: {str(e)}")
        print(error_trace)
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def retract_activity_api(request, activity_id):
    """
    POST: Retract (unpublish) an activity to make it hidden from students (teacher only)
    """
    try:
        activity = PortfolioActivity.objects.get(id=activity_id)
    except PortfolioActivity.DoesNotExist:
        return Response({'error': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Only teachers can retract
    if not request.user.is_authenticated or request.user.role != 'teacher':
        return Response({'error': 'Only teachers can retract activities'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Check if activity is published
        if not activity.is_published:
            return Response({'error': 'Activity is not published'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Retract the activity (set back to draft)
        activity.is_published = False
        activity.published_at = None
        activity.save()
        
        print(f"✅ Activity {activity_id} retracted successfully")
        
        # Notify all students that the activity has been retracted
        students = User.objects.filter(role='student').exclude(username='admin')
        
        for student in students:
            create_notification(
                recipient=student,
                notification_type='activity_updated',
                title='Activity Retracted',
                message=f'Activity "{activity.title}" has been retracted and is no longer available.',
                activity=activity,
                portfolio=activity.folder
            )
        
        serializer = PortfolioActivitySerializer(activity)
        return Response({
            'message': 'Activity retracted successfully',
            'activity': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error retracting activity: {str(e)}")
        print(error_trace)
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
        # Check if requesting drafts only
        include_drafts = request.GET.get('include_drafts', 'false').lower() == 'true'
        
        # Teachers see all submissions, students see only their own
        if request.user.role == 'teacher':
            # Teachers see only final submissions (not drafts) unless specifically requested
            if include_drafts:
                submissions = StudentSubmission.objects.filter(activity=activity).order_by('-submitted_at')
            else:
                submissions = StudentSubmission.objects.filter(
                    activity=activity
                ).exclude(status='draft').order_by('-submitted_at')
            # Use lightweight serializer for teachers (excludes large file_path)
            from .serializer import StudentSubmissionListSerializer
            serializer = StudentSubmissionListSerializer(submissions, many=True)
        else:
            # Students can request all submissions including drafts
            if include_drafts:
                submissions = StudentSubmission.objects.filter(
                    activity=activity, 
                    student=request.user
                ).order_by('-submitted_at')
            else:
                # By default, exclude drafts
                submissions = StudentSubmission.objects.filter(
                    activity=activity, 
                    student=request.user
                ).exclude(status='draft').order_by('-submitted_at')
            # Use full serializer for students (includes file_path for their own submissions)
            serializer = StudentSubmissionSerializer(submissions, many=True, context={'request': request})
        
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
                
                # Check if this update is late (if not already marked as late)
                if not existing_submission.is_late and activity.due_date:
                    from django.utils import timezone
                    from datetime import datetime, time as dt_time
                    
                    now = timezone.now()
                    if activity.due_time:
                        due_datetime = timezone.make_aware(
                            datetime.combine(activity.due_date, activity.due_time)
                        )
                    else:
                        due_datetime = timezone.make_aware(
                            datetime.combine(activity.due_date, dt_time(23, 59, 59))
                        )
                    
                    if now > due_datetime:
                        existing_submission.is_late = True
                
                existing_submission.save()
                serializer = StudentSubmissionSerializer(existing_submission)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # Create new submission
                # Handle post_to_feed - convert string to boolean
                post_to_feed_raw = data.get('post_to_feed', False)
                if isinstance(post_to_feed_raw, str):
                    post_to_feed = post_to_feed_raw.lower() in ('true', '1', 'yes')
                else:
                    post_to_feed = bool(post_to_feed_raw)
                
                # Check if this is a draft or final submission
                is_draft = data.get('is_draft', True)  # Default to draft
                if isinstance(is_draft, str):
                    is_draft = is_draft.lower() in ('true', '1', 'yes')
                else:
                    is_draft = bool(is_draft)
                
                # Automatically detect if submission is late (only for final submissions)
                is_late = False
                if not is_draft and activity.due_date:
                    from django.utils import timezone
                    from datetime import datetime, time as dt_time
                    
                    # Get current time
                    now = timezone.now()
                    
                    # Create due datetime
                    if activity.due_time:
                        # Combine date and time
                        due_datetime = timezone.make_aware(
                            datetime.combine(activity.due_date, activity.due_time)
                        )
                    else:
                        # If no time specified, use end of day (23:59:59)
                        due_datetime = timezone.make_aware(
                            datetime.combine(activity.due_date, dt_time(23, 59, 59))
                        )
                    
                    # Check if current time is after due datetime
                    is_late = now > due_datetime
                    print(f"📅 Due date check: now={now}, due={due_datetime}, is_late={is_late}")
                
                # Handle file upload - support both base64 and actual file
                file_path = data.get('file_path', '')
                file_obj = request.FILES.get('file')  # Check if actual file was uploaded
                
                # Determine file type
                file_type = data.get('file_type', '')
                if file_obj and not file_type:
                    # Auto-detect file type from uploaded file
                    content_type = file_obj.content_type
                    if content_type.startswith('image/'):
                        file_type = 'image'
                    elif content_type == 'application/pdf':
                        file_type = 'pdf'
                    elif content_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                        file_type = 'document'
                    else:
                        file_type = 'file'
                    print(f"📎 Auto-detected file type: {file_type} from {content_type}")
                
                # Set status based on draft flag
                submission_status = 'draft' if is_draft else 'unscored'
                
                submission = StudentSubmission.objects.create(
                    activity=activity,
                    student=request.user,
                    caption=data.get('caption', ''),
                    file=file_obj if file_obj else None,  # Store actual file if provided
                    file_path=file_path,  # Store base64 as fallback
                    file_type=file_type,
                    status=submission_status,
                    post_to_feed=post_to_feed,
                    approval_status='pending' if post_to_feed else 'approved',
                    is_late=is_late
                )
                
                print(f"✅ Submission created: ID={submission.id}, status={submission_status}, file_type={file_type}, is_late={is_late}, is_draft={is_draft}")
                
                # Only notify teacher if this is a final submission (not draft)
                if not is_draft:
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
        # Get all unscored submissions - explicitly filter by status='unscored' 
        # AND exclude any that have scores (double safety check)
        # AND exclude drafts
        submissions = StudentSubmission.objects.filter(
            status='unscored'
        ).exclude(
            status='scored'
        ).exclude(
            status='draft'
        ).exclude(
            score__isnull=False  # Exclude any submission that has a score, regardless of status
        ).distinct().order_by('-submitted_at')
        
        print(f"📊 Unscored submissions query: Found {submissions.count()} submissions")
        
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
        # Get all scored submissions - filter by status='scored' OR has a score
        # This ensures we catch all scored submissions even if status wasn't updated properly
        submissions = StudentSubmission.objects.filter(
            Q(status='scored') | Q(score__isnull=False)
        ).exclude(
            status='draft'
        ).distinct().order_by('-scored_at', '-submitted_at')
        
        print(f"📊 Scored submissions query: Found {submissions.count()} submissions")
        
        # Use lightweight serializer for list (excludes large file_path)
        from .serializer import StudentSubmissionListSerializer
        serializer = StudentSubmissionListSerializer(submissions, many=True, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        print(f"Error fetching scored submissions: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
def student_submitted_collection_api(request):
    """
    GET: Get all submissions by the current student (student only)
    Returns all submitted works across all activities for the student's submitted collection
    """
    if not request.user.is_authenticated or request.user.role != 'student':
        return Response({'error': 'Only students can view their submitted collection'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Get all submitted works by this student (exclude drafts and hidden items), ordered by most recent first
        submissions = StudentSubmission.objects.filter(
            student=request.user,
            submitted_at__isnull=False,  # Only include submissions that have been submitted (not drafts)
            is_active=True  # Only show active submissions (not hidden from collection)
        ).select_related('activity', 'activity__folder').order_by('-submitted_at')
        
        print(f"📦 Processing {submissions.count()} submissions for student {request.user.username}")
        
        # Format response with activity details
        collection_data = []
        for submission in submissions:
            try:
                activity = submission.activity
                if not activity:
                    print(f"⚠️ Submission {submission.id} has no activity, skipping")
                    continue
                
                # Get folder name safely
                folder_name = 'Unknown'
                if hasattr(activity, 'folder') and activity.folder:
                    folder_name = activity.folder.name
                
                collection_data.append({
                    'id': submission.id,
                    'activity_id': activity.id,
                    'activity_title': activity.title,
                    'activity_type': activity.activity_type,
                    'folder_name': folder_name,
                    'caption': submission.caption or '',
                    'file_path': submission.file_path or '',
                    'file_type': submission.file_type or 'unknown',
                    'submitted_at': submission.submitted_at.isoformat() if submission.submitted_at else None,
                    'is_late': submission.is_late,
                    'status': submission.status,
                    'score': submission.score if submission.status == 'scored' else None,
                    'feedback': submission.feedback if submission.status == 'scored' else '',
                    'scored_at': submission.scored_at.isoformat() if submission.scored_at else None,
                })
            except Exception as item_error:
                print(f"⚠️ Error processing submission {submission.id}: {str(item_error)}")
                continue
        
        print(f"✅ Successfully formatted {len(collection_data)} submissions for student {request.user.username}")
        return Response(collection_data)
    except Exception as e:
        import traceback
        print(f"❌ Error fetching submitted collection: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
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
        # Get all submissions with pending approval for this teacher's classes
        # Filter by teacher's folders
        submissions = StudentSubmission.objects.filter(
            approval_status='pending',
            activity__folder__teacher=request.user
        ).select_related('student', 'activity', 'activity__folder').order_by('-submitted_at')
        
        print(f"📝 Found {submissions.count()} pending approvals for teacher {request.user.username}")
        
        # Debug: Print each submission
        for sub in submissions:
            print(f"   - ID: {sub.id}, Student: {sub.student.username}, Activity: {sub.activity.title if sub.activity else 'N/A'}, Status: {sub.approval_status}")
        
        serializer = StudentSubmissionSerializer(submissions, many=True, context={'request': request})
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
            submission.post_to_feed = True  # Mark as posted to feed
            submission.save()
            
            print(f"✅ Approved submission {submission_id} for posting to feed")
            
            # Notify student about approval
            create_notification(
                recipient=submission.student,
                notification_type='submission_approved',
                title='Post Approved',
                message=f'Your post request for "{submission.activity.title}" has been approved and is now visible in the newsfeed',
                submission=submission,
                activity=submission.activity
            )
            
            # Create a newsfeed post (now that it's approved)
            if True:  # Always create post when approved
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
        elif action == 'cancel':
            # Cancel/remove the post request - reset to approved without posting
            submission.approval_status = 'approved'
            submission.post_to_feed = False  # Don't post to feed
            submission.save()
            
            print(f"🚫 Cancelled post request for submission {submission_id}")
            
            # Notify student that request was cancelled
            create_notification(
                recipient=submission.student,
                notification_type='submission_rejected',
                title='Post Request Cancelled',
                message=f'Your post request for "{submission.activity.title}" has been cancelled by your teacher',
                submission=submission,
                activity=submission.activity
            )
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
    GET: Get all newsfeed posts with likes and comments
    """
    try:
        # Get all newsfeed posts
        posts = NewsfeedPost.objects.all().order_by('-posted_at')
        
        # Serialize posts with additional data
        posts_data = []
        for post in posts:
            # Try to get likes count, fallback to 0 if table doesn't exist
            try:
                likes_count = post.likes.count()
                is_liked = PostLike.objects.filter(post=post, user=request.user).exists() if request.user.is_authenticated else False
            except Exception:
                likes_count = 0
                is_liked = False
            
            post_dict = {
                'id': post.id,
                'student_name': post.student_name,
                'caption': post.caption,
                'file_path': post.file_path,
                'file_type': post.file_type,
                'activity_title': post.activity_title,
                'activity_type': post.activity_type,
                'posted_at': post.posted_at.isoformat(),
                'likes': likes_count,
                'is_liked': is_liked,
            }
            posts_data.append(post_dict)
        
        return Response(posts_data)
    except Exception as e:
        print(f"Error fetching newsfeed: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def post_like_api(request, post_id):
    """
    POST: Toggle like on a post
    Body: { "liked": true/false }
    """
    if not request.user.is_authenticated:
        print(f"❌ Like API - User not authenticated")
        return Response({
            'error': 'Authentication required',
            'message': 'Please log in to like posts'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        from .models import NewsfeedPost, PostLike
        
        post = NewsfeedPost.objects.get(id=post_id)
        liked = request.data.get('liked', True)
        
        if liked:
            # Add like (use get_or_create to avoid duplicates)
            like, created = PostLike.objects.get_or_create(
                post=post,
                user=request.user
            )
            message = 'Post liked' if created else 'Already liked'
        else:
            # Remove like
            deleted_count = PostLike.objects.filter(post=post, user=request.user).delete()[0]
            message = 'Like removed' if deleted_count > 0 else 'Like not found'
        
        # Return updated like count
        return Response({
            'success': True,
            'message': message,
            'likes_count': post.likes_count,
            'is_liked': liked
        })
        
    except NewsfeedPost.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error toggling like: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET', 'POST'])
def post_comments_api(request, post_id):
    """
    GET: Get all comments for a post
    POST: Add a comment to a post
    Body: { "text": "comment text" }
    """
    # Allow GET for everyone, but require auth for POST
    if request.method == 'POST' and not request.user.is_authenticated:
        print(f"❌ Comment API - User not authenticated")
        return Response({
            'error': 'Authentication required',
            'message': 'Please log in to comment on posts'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        from .models import NewsfeedPost, PostComment
        
        post = NewsfeedPost.objects.get(id=post_id)
        
        if request.method == 'GET':
            # Get all comments for this post
            comments = PostComment.objects.filter(post=post).order_by('created_at')
            comments_data = [{
                'id': comment.id,
                'user': comment.user.username,
                'text': comment.text,
                'created_at': comment.created_at.isoformat(),
                'timestamp': get_time_ago(comment.created_at)
            } for comment in comments]
            
            return Response(comments_data)
        
        elif request.method == 'POST':
            # Add new comment
            text = request.data.get('text', '').strip()
            
            if not text:
                return Response({'error': 'Comment text is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            comment = PostComment.objects.create(
                post=post,
                user=request.user,
                text=text
            )
            
            return Response({
                'success': True,
                'message': 'Comment added',
                'comment': {
                    'id': comment.id,
                    'user': comment.user.username,
                    'text': comment.text,
                    'created_at': comment.created_at.isoformat(),
                    'timestamp': 'Just now'
                }
            }, status=status.HTTP_201_CREATED)
            
    except NewsfeedPost.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error with comments: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_time_ago(datetime_obj):
    """Helper function to get relative time"""
    from django.utils import timezone
    now = timezone.now()
    diff = now - datetime_obj
    
    seconds = diff.total_seconds()
    if seconds < 60:
        return 'Just now'
    minutes = int(seconds / 60)
    if minutes < 60:
        return f'{minutes} minute{"s" if minutes > 1 else ""} ago'
    hours = int(minutes / 60)
    if hours < 24:
        return f'{hours} hour{"s" if hours > 1 else ""} ago'
    days = int(hours / 24)
    if days < 7:
        return f'{days} day{"s" if days > 1 else ""} ago'
    return datetime_obj.strftime('%b %d, %Y')


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def submission_detail_api(request, submission_id):
    """
    GET: Get full submission details including file_path (for viewing individual submission)
    PUT: Update submission (for turning in drafts or updating caption)
    DELETE: Delete submission (for removing drafts)
    """
    try:
        submission = StudentSubmission.objects.get(id=submission_id)
        
        # Check permissions - only the student who created it or teacher can modify
        if request.user.role == 'student' and submission.student != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        if request.method == 'GET':
            serializer = StudentSubmissionSerializer(submission, context={'request': request})
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            # Update submission
            data = request.data
            
            if 'caption' in data:
                submission.caption = data['caption']
            if 'post_to_feed' in data:
                post_to_feed_raw = data['post_to_feed']
                if isinstance(post_to_feed_raw, str):
                    submission.post_to_feed = post_to_feed_raw.lower() in ('true', '1', 'yes')
                else:
                    submission.post_to_feed = bool(post_to_feed_raw)
            
            # Check if status is being changed (turning in work)
            if 'status' in data:
                old_status = submission.status
                new_status = data['status']
                
                # Handle resubmit logic - converting back to draft
                if old_status in ['unscored', 'scored'] and new_status == 'draft':
                    from django.utils import timezone
                    
                    # Check if already scored - cannot resubmit if scored
                    if submission.score is not None:
                        return Response({
                            'error': 'Cannot resubmit work that has already been scored',
                            'can_resubmit': False,
                            'reason': 'already_scored'
                        }, status=status.HTTP_400_BAD_REQUEST)
                    
                    # Check resubmit count limit (max 3 resubmissions)
                    MAX_RESUBMITS = 3
                    if submission.resubmit_count >= MAX_RESUBMITS:
                        return Response({
                            'error': f'Maximum resubmit limit ({MAX_RESUBMITS}) reached',
                            'can_resubmit': False,
                            'reason': 'max_limit_reached',
                            'resubmit_count': submission.resubmit_count,
                            'max_resubmits': MAX_RESUBMITS
                        }, status=status.HTTP_400_BAD_REQUEST)
                    
                    # Increment resubmit count and track time
                    submission.resubmit_count += 1
                    submission.last_resubmit_at = timezone.now()
                    print(f"🔄 Resubmit #{submission.resubmit_count} for submission {submission.id}")
                
                submission.status = new_status
                
                # If changing from draft to final submission, ALWAYS update submitted_at to current time
                if old_status == 'draft' and new_status in ['unscored', 'scored']:
                    from django.utils import timezone
                    from datetime import datetime, time as dt_time
                    
                    # ALWAYS update submitted_at to current time (when student turned in)
                    now = timezone.now()
                    submission.submitted_at = now
                    
                    activity = submission.activity
                    if activity and activity.due_date:
                        if activity.due_time:
                            due_datetime = timezone.make_aware(
                                datetime.combine(activity.due_date, activity.due_time)
                            )
                        else:
                            due_datetime = timezone.make_aware(
                                datetime.combine(activity.due_date, dt_time(23, 59, 59))
                            )
                        
                        # Check if late based on CURRENT submission time
                        submission.is_late = now > due_datetime
                        print(f"📅 Turning in work: submitted_at={now}, due={due_datetime}, is_late={submission.is_late}")
                    else:
                        print(f"📅 Turning in work: submitted_at={now}")
                    
                    # Notify teacher when work is turned in
                    if activity:
                        teacher = activity.folder.teacher
                        create_notification(
                            recipient=teacher,
                            notification_type='submission_received',
                            title='New Submission Received',
                            message=f'{request.user.username} submitted work for "{activity.title}"',
                            submission=submission,
                            activity=activity
                        )
            
            # Legacy support: Check if turning in a draft using is_draft parameter
            is_draft = data.get('is_draft', None)
            if is_draft is not None:
                if isinstance(is_draft, str):
                    is_draft = is_draft.lower() in ('true', '1', 'yes')
                else:
                    is_draft = bool(is_draft)
                
                # If turning in (is_draft=False), check for late submission and update submitted_at
                if not is_draft and submission.status == 'draft':
                    from django.utils import timezone
                    from datetime import datetime, time as dt_time
                    
                    # Update submitted_at to current time
                    now = timezone.now()
                    submission.submitted_at = now
                    
                    activity = submission.activity
                    if activity and activity.due_date:
                        if activity.due_time:
                            due_datetime = timezone.make_aware(
                                datetime.combine(activity.due_date, activity.due_time)
                            )
                        else:
                            due_datetime = timezone.make_aware(
                                datetime.combine(activity.due_date, dt_time(23, 59, 59))
                            )
                        
                        submission.is_late = now > due_datetime
                        print(f"📅 Legacy is_draft: submitted_at={now}, is_late={submission.is_late}")
            
            submission.save()
            serializer = StudentSubmissionSerializer(submission, context={'request': request})
            return Response(serializer.data)
        
        elif request.method == 'DELETE':
            # Students can hide their own submissions from collection (not permanent delete)
            # Teachers can permanently delete any submission
            if request.user.role == 'student' and submission.student != request.user:
                return Response({'error': 'You can only manage your own submissions'}, status=status.HTTP_403_FORBIDDEN)
            
            if request.user.role == 'student':
                # Students: Hide from collection (set is_active=False)
                submission.is_active = False
                submission.save()
                print(f"👁️ Hiding submission {submission.id} from collection by {request.user.username}")
                return Response({'message': 'Submission hidden from collection'}, status=status.HTTP_200_OK)
            else:
                # Teachers: Permanent delete
                print(f"🗑️ Permanently deleting submission {submission.id} by teacher {request.user.username}")
                submission.delete()
                return Response({'message': 'Submission deleted permanently'}, status=status.HTTP_200_OK)
        
    except StudentSubmission.DoesNotExist:
        return Response({'error': 'Submission not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error in submission_detail_api: {str(e)}")
        print(error_trace)
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def request_post_approval_api(request, submission_id):
    """
    POST: Student requests approval to post their output to feed
    Creates a notification for the teacher to approve/reject
    """
    if not request.user.is_authenticated or request.user.role != 'student':
        return Response({'error': 'Only students can request post approval'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        submission = StudentSubmission.objects.get(id=submission_id, student=request.user)
        
        # Check if already posted
        if submission.post_to_feed:
            return Response({'error': 'This submission is already posted to feed'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if there's already a pending approval request
        if submission.approval_status == 'pending':
            return Response({'error': 'You already have a pending approval request for this submission'}, status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data
        caption = data.get('caption', '').strip()
        include_score = data.get('include_score', False)
        
        # Validate caption
        if not caption:
            return Response({'error': 'Caption is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update submission with new caption and set approval status to pending
        submission.caption = caption
        submission.approval_status = 'pending'
        submission.save()
        
        print(f"📝 Updated submission {submission_id}:")
        print(f"   Caption: {caption}")
        print(f"   Approval status: {submission.approval_status}")
        
        # Create notification for teacher
        activity = submission.activity
        teacher = activity.folder.teacher if activity and activity.folder else None
        
        if teacher:
            # Create notification
            notification_message = f'{request.user.username} requests approval to post their work for "{activity.title}"'
            if include_score:
                notification_message += f' (with score: {submission.score} points)'
            
            create_notification(
                recipient=teacher,
                notification_type='approval_requested',
                title='Post Approval Request',
                message=notification_message,
                submission=submission,
                activity=activity
            )
            
            print(f"📤 Post approval request created for submission {submission_id}")
            print(f"   Student: {request.user.username}")
            print(f"   Include score: {include_score}")
            print(f"   Caption: {caption[:50]}...")
            
            return Response({
                'message': 'Post approval request sent successfully',
                'submission_id': submission.id,
                'approval_status': submission.approval_status
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Teacher not found for this activity'}, status=status.HTTP_404_NOT_FOUND)
            
    except StudentSubmission.DoesNotExist:
        return Response({'error': 'Submission not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        import traceback
        print(f"❌ Error in request_post_approval_api: {str(e)}")
        print(traceback.format_exc())
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
        print(f"📝 Before update - Status: {submission.status}, Score: {submission.score}")
        
        submission.score = score
        submission.feedback = feedback
        submission.criteria_scores = criteria_scores  # Save the criteria scores JSON
        submission.status = 'scored'
        submission.scored_at = timezone.now()
        submission.save(update_fields=['score', 'feedback', 'criteria_scores', 'status', 'scored_at'])
        
        # Refresh from database to confirm the save
        submission.refresh_from_db()
        print(f"✅ Submission {submission_id} marked as scored")
        print(f"📝 After update - Status: {submission.status}, Score: {submission.score}, Scored at: {submission.scored_at}")
        
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
            
            # Convert submission time to local timezone if submitted
            submitted_at_local = None
            if envelope.is_submitted and envelope.submitted_at:
                submitted_at_local = timezone.localtime(envelope.submitted_at).isoformat()
            
            return Response({
                'envelope': {
                    'id': envelope.id,
                    'title': envelope.title,
                    'student_name': envelope.student_name,
                    'class_name': envelope.class_name,
                    'color': envelope.color,
                    'pattern': envelope.pattern,
                    'is_submitted': envelope.is_submitted,
                    'submitted_at': submitted_at_local,
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
            # Get only published activities in this folder (students should not see drafts)
            activities = PortfolioActivity.objects.filter(folder=folder, is_published=True).order_by('created_at')
            
            for activity in activities:
                # Check if student has submitted this activity
                submission = StudentSubmission.objects.filter(
                    activity=activity,
                    student=request.user
                ).first()
                
                # Get submission file path with better error handling
                submission_file = None
                if submission:
                    try:
                        if submission.file:
                            # Use the FileField URL
                            submission_file = submission.file.url if submission.file else None
                        elif submission.file_path:
                            # Fallback to file_path for base64 or legacy data
                            submission_file = submission.file_path
                    except Exception as file_error:
                        print(f"⚠️ Error getting submission file for activity {activity.id}: {file_error}")
                        submission_file = None
                
                # Convert submission time to local timezone if exists
                local_submitted_time = None
                submitted_date_str = None
                submitted_time_str = None
                
                if submission and submission.submitted_at:
                    try:
                        local_submitted_time = timezone.localtime(submission.submitted_at)
                        submitted_date_str = local_submitted_time.strftime('%b %d, %Y')
                        submitted_time_str = local_submitted_time.strftime('%I:%M %p')
                    except Exception as date_error:
                        print(f"⚠️ Error formatting submission date: {date_error}")
                
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
                    'submission_date': local_submitted_time.isoformat() if local_submitted_time else None,
                    'submitted_date': submitted_date_str,
                    'submitted_time': submitted_time_str,
                    'submission_file': submission_file,
                    'submission_caption': submission.caption if submission else None,
                    'submission_score': submission.score if submission else None,
                    'submission_feedback': submission.feedback if submission else None,
                    'submission_status': 'submitted' if submission else 'missing',
                    'folder_name': folder.name
                }
                
                print(f"📝 Activity {activity.id} ({activity.title}): status={activity_data['submission_status']}, has_file={submission_file is not None}")
                
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
@api_view(['POST'])
def submit_missing_activity_api(request, activity_id):
    """Submit a missing activity from portfolio compilation"""
    try:
        from .models import PortfolioActivity, StudentSubmission
        import base64
        from django.core.files.base import ContentFile
        
        print(f"📝 Submitting missing activity {activity_id} for student: {request.user.username}")
        
        # Get the activity
        activity = PortfolioActivity.objects.get(id=activity_id)
        
        # Get submission data
        file_data = request.data.get('file')
        caption = request.data.get('caption', '')
        
        if not file_data:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if submission already exists
        existing_submission = StudentSubmission.objects.filter(
            activity=activity,
            student=request.user
        ).first()
        
        if existing_submission:
            return Response({
                'error': 'Activity already submitted',
                'submission_id': existing_submission.id
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Handle file upload
        if file_data.startswith('data:'):
            # Base64 encoded file
            format, filestr = file_data.split(';base64,')
            ext = format.split('/')[-1]
            file_name = f"submission_{request.user.id}_{activity_id}.{ext}"
            
            # Create submission with file
            submission = StudentSubmission.objects.create(
                activity=activity,
                student=request.user,
                caption=caption,
                file=ContentFile(base64.b64decode(filestr), name=file_name),
                file_path=file_data,  # Keep base64 for compatibility
                file_type=ext,
                status='unscored',
                approval_status='pending',
                post_to_feed=False
            )
        else:
            # Regular file path
            submission = StudentSubmission.objects.create(
                activity=activity,
                student=request.user,
                caption=caption,
                file_path=file_data,
                status='unscored',
                approval_status='pending',
                post_to_feed=False
            )
        
        print(f"✅ Missing activity submitted successfully: {submission.id}")
        
        # Notify teacher
        try:
            teacher = activity.folder.teacher
            notification_title = f'Missing Activity Submitted - {activity.title}'
            notification_message = f'{request.user.username} has submitted the missing activity "{activity.title}" for {activity.folder.class_name}.'
            
            notification = create_notification(
                recipient=teacher,
                notification_type='submission_created',
                title=notification_title,
                message=notification_message
            )
            
            if notification:
                print(f"✅ Notified teacher {teacher.username}")
        except Exception as notify_error:
            print(f"⚠️ Error notifying teacher: {str(notify_error)}")
        
        return Response({
            'message': 'Activity submitted successfully',
            'submission': {
                'id': submission.id,
                'activity_id': activity.id,
                'activity_title': activity.title,
                'caption': submission.caption,
                'submitted_at': submission.submitted_at.isoformat(),
                'status': submission.status
            }
        }, status=status.HTTP_201_CREATED)
        
    except PortfolioActivity.DoesNotExist:
        return Response({'error': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        import traceback
        print(f"❌ Error submitting missing activity: {str(e)}")
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
        
        # Get all submitted envelopes for this class (only show submitted portfolios to teachers)
        envelopes = PortfolioEnvelope.objects.filter(
            class_name=class_name,
            is_submitted=True
        ).select_related('student')
        
        envelope_list = []
        for envelope in envelopes:
            # Convert UTC time to local timezone (Asia/Manila)
            local_time = timezone.localtime(envelope.created_at)
            
            envelope_list.append({
                'id': envelope.id,
                'student_id': envelope.student.id,
                'student_name': envelope.student_name,
                'student_username': envelope.student.username,
                'id_number': envelope.student.id,  # Use database primary key as ID number
                'title': envelope.title,
                'color': envelope.color,
                'pattern': envelope.pattern,
                'created_at': local_time.isoformat(),
                'date_created': local_time.strftime('%b %d, %Y'),
                'time_created': local_time.strftime('%I:%M %p')
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


@csrf_exempt
@api_view(['GET'])
def get_teacher_student_activities_api(request, class_name, student_id):
    """Get all activities (submitted and missing) for a specific student (teacher view)"""
    try:
        from .models import PortfolioActivity, StudentSubmission, PortfolioFolder
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        
        print(f"📚 Teacher fetching activities for student ID: {student_id} in class: {class_name}")
        
        # Check if user is a teacher
        if request.user.role != 'teacher':
            return Response({
                'error': 'Only teachers can view student activities'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Get the student
        try:
            student = User.objects.get(id=student_id)
        except User.DoesNotExist:
            return Response({
                'error': 'Student not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
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
                    student=student
                ).first()
                
                # Get submission file path
                submission_file = None
                if submission:
                    try:
                        if submission.file:
                            # Use the FileField URL
                            submission_file = submission.file.url if submission.file else None
                        elif submission.file_path:
                            # Fallback to file_path for base64 or legacy data
                            submission_file = submission.file_path
                    except Exception as file_error:
                        print(f"⚠️ Error getting submission file: {file_error}")
                        submission_file = None
                
                # Convert submission time to local timezone if exists
                local_submitted_time = None
                submitted_date_str = None
                submitted_time_str = None
                submission_date_iso = None
                
                if submission and submission.submitted_at:
                    try:
                        local_submitted_time = timezone.localtime(submission.submitted_at)
                        submission_date_iso = local_submitted_time.isoformat()
                        submitted_date_str = local_submitted_time.strftime('%b %d, %Y')
                        submitted_time_str = local_submitted_time.strftime('%I:%M %p')
                    except Exception as date_error:
                        print(f"⚠️ Error formatting submission date: {date_error}")
                
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
                    'submission_date': submission_date_iso,
                    'submitted_date': submitted_date_str,
                    'submitted_time': submitted_time_str,
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
        
        print(f"✅ Found {len(submitted_activities)} submitted and {len(missing_activities)} missing activities for student")
        
        return Response({
            'all_activities': activity_list,
            'submitted_activities': submitted_activities,
            'missing_activities': missing_activities,
            'total_count': len(activity_list),
            'submitted_count': len(submitted_activities),
            'missing_count': len(missing_activities),
            'student_name': student.username
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        import traceback
        print(f"❌ Error fetching student activities: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def submit_portfolio_api(request, class_name):
    """Submit a portfolio envelope (student only)"""
    try:
        from .models import PortfolioEnvelope
        
        print(f"📤 Student {request.user.username} submitting portfolio for class: {class_name}")
        
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return Response({
                'error': 'Authentication required'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Check if user is a student
        if request.user.role != 'student':
            return Response({
                'error': 'Only students can submit portfolios'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Get the student's envelope for this class
        try:
            envelope = PortfolioEnvelope.objects.get(
                student=request.user,
                class_name=class_name
            )
        except PortfolioEnvelope.DoesNotExist:
            return Response({
                'error': 'Portfolio envelope not found. Please create your envelope first.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if already submitted
        if envelope.is_submitted:
            return Response({
                'error': 'Portfolio has already been submitted',
                'submitted_at': envelope.submitted_at.isoformat() if envelope.submitted_at else None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Mark as submitted
        envelope.is_submitted = True
        envelope.submitted_at = timezone.now()
        envelope.save()
        
        print(f"✅ Portfolio submitted successfully by {request.user.username} for {class_name}")
        
        # Notify teacher about the submission
        try:
            from .models import PortfolioCompilationRequest
            compilation_request = PortfolioCompilationRequest.objects.filter(
                class_name=class_name,
                is_active=True
            ).first()
            
            if compilation_request and compilation_request.requested_by:
                teacher = compilation_request.requested_by
                create_notification(
                    recipient=teacher,
                    notification_type='portfolio_submitted',
                    title='Portfolio Submitted',
                    message=f'{request.user.username} has submitted their portfolio for {class_name}'
                )
                print(f"📧 Notification sent to teacher: {teacher.username}")
        except Exception as e:
            print(f"⚠️ Could not send notification to teacher: {str(e)}")
        
        # Convert to local timezone for response
        local_submitted_time = timezone.localtime(envelope.submitted_at)
        
        return Response({
            'success': True,
            'message': 'Portfolio submitted successfully',
            'submitted_at': local_submitted_time.isoformat(),
            'submitted_date': local_submitted_time.strftime('%b %d, %Y'),
            'submitted_time': local_submitted_time.strftime('%I:%M %p')
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        import traceback
        print(f"❌ Error submitting portfolio: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
def check_activity_edit_deadlines_api(request):
    """
    Check for activities approaching their edit deadline and notify teachers
    Should be called periodically (e.g., every hour) or when teacher logs in
    """
    if not request.user.is_authenticated or request.user.role != 'teacher':
        return Response({'error': 'Only teachers can check edit deadlines'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        from datetime import datetime, timedelta, time as time_type
        
        # Configuration
        EDIT_CUTOFF_HOURS = 3  # Activities can't be edited within 3 hours of deadline
        WARNING_HOUR = 4  # Warn when 4 hours remain (1 hour before edit cutoff)
        
        # Get all published activities for this teacher
        teacher_folders = PortfolioFolder.objects.filter(teacher=request.user)
        activities = PortfolioActivity.objects.filter(
            folder__in=teacher_folders,
            is_published=True
        )
        
        now = datetime.now()
        warnings = []
        
        print(f"🔍 Checking {activities.count()} activities for edit deadline warnings...")
        print(f"⏰ Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        
        for activity in activities:
            if not activity.due_date:
                continue
            
            # Combine due date and time
            activity_due_date = activity.due_date
            if activity.due_time:
                activity_time = activity.due_time
                due_datetime = datetime.combine(activity_due_date, activity_time)
            else:
                due_datetime = datetime.combine(activity_due_date, time_type(23, 59, 59))
            
            # Calculate time remaining
            time_remaining = due_datetime - now
            hours_remaining = time_remaining.total_seconds() / 3600
            
            print(f"📊 Activity '{activity.title}': Due {due_datetime.strftime('%Y-%m-%d %H:%M')}, {hours_remaining:.1f} hours remaining")
            
            # Skip if deadline has passed
            if hours_remaining <= 0:
                print(f"  ⏭️ Skipped: Deadline passed")
                continue
            
            # Skip if already past edit cutoff
            if hours_remaining <= EDIT_CUTOFF_HOURS:
                print(f"  ⏭️ Skipped: Already in edit cutoff window ({hours_remaining:.1f} ≤ {EDIT_CUTOFF_HOURS})")
                continue
            
            # Check if we're at the 1-hour warning mark (4 hours before deadline = 1 hour before edit cutoff)
            if WARNING_HOUR - 0.5 <= hours_remaining <= WARNING_HOUR + 0.5:
                print(f"  ⚠️ AT WARNING MARK: {hours_remaining:.1f} hours (1 hour before edit cutoff)")
                
                # Check if notification already sent
                existing_notification = Notification.objects.filter(
                    recipient=request.user,
                    notification_type='edit_deadline_warning',
                    activity=activity,
                    created_at__gte=now - timedelta(hours=2)  # Don't send duplicate within 2 hours
                ).exists()
                
                if not existing_notification:
                    print(f"  📨 Creating 1-hour warning notification...")
                    
                    # Calculate when editing will be locked
                    edit_deadline = due_datetime - timedelta(hours=EDIT_CUTOFF_HOURS)
                    edit_deadline_str = edit_deadline.strftime('%b %d, %Y at %I:%M %p')
                    
                    # Create notification
                    create_notification(
                        recipient=request.user,
                        notification_type='edit_deadline_warning',
                        title='⚠️ You Have 1 Hour Remaining to Make Changes',
                        message=f'Activity "{activity.title}" in "{activity.folder.name}" can only be edited for 1 more hour. Edit deadline: {edit_deadline_str}.',
                        activity=activity,
                        portfolio=activity.folder
                    )
                    
                    print(f"  ✅ 1-hour warning notification created successfully")
                    
                    warnings.append({
                        'activity_id': activity.id,
                        'activity_title': activity.title,
                        'folder_name': activity.folder.name,
                        'hours_remaining': round(hours_remaining, 1),
                        'edit_deadline': edit_deadline_str
                    })
                else:
                    print(f"  ⏭️ Skipped: 1-hour warning already sent")
            
            elif hours_remaining <= EDIT_CUTOFF_HOURS:
                print(f"  ⏭️ Skipped: Already in edit cutoff window ({hours_remaining:.1f} ≤ {EDIT_CUTOFF_HOURS})")
            else:
                print(f"  ⏭️ Skipped: Not at 1-hour warning mark yet ({hours_remaining:.1f} hours)")
        
        return Response({
            'success': True,
            'warnings_sent': len(warnings),
            'activities_warned': warnings
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error checking edit deadlines: {str(e)}")
        print(error_trace)
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================
# PROFILE AND SETTINGS APIs
# ============================================

@csrf_exempt
@api_view(['GET', 'PUT'])
def user_profile_api(request):
    """
    GET: Get user profile
    PUT: Update user profile
    """
    print(f"🔍 Profile API - User: {request.user}, Authenticated: {request.user.is_authenticated}")
    if not request.user.is_authenticated:
        print(f"❌ Profile API - User not authenticated")
        return Response({'error': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        try:
            from .serializer import UserProfileSerializer
            serializer = UserProfileSerializer(request.user, context={'request': request})
            profile_data = serializer.data
            
            print(f"✅ Profile loaded for {request.user.username} (Role: {request.user.role})")
            print(f"   Fields returned: {list(profile_data.keys())}")
            
            return Response(profile_data)
        except Exception as e:
            print(f"❌ Error fetching profile: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'PUT':
        try:
            from .serializer import UserProfileSerializer
            
            # Handle profile picture upload
            profile_picture = request.FILES.get('profile_picture')
            if profile_picture:
                # Validate file size (5MB limit)
                if profile_picture.size > 5 * 1024 * 1024:
                    return Response({'error': 'File size must be less than 5MB'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Validate file type
                allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
                if profile_picture.content_type not in allowed_types:
                    return Response({'error': 'Invalid file type. Only images are allowed.'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = UserProfileSerializer(
                request.user, 
                data=request.data, 
                partial=True,
                context={'request': request}
            )
            
            if serializer.is_valid():
                serializer.save()
                print(f"✅ Profile updated for user: {request.user.username}")
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            print(f"❌ Error updating profile: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET', 'PUT'])
def user_settings_api(request):
    """
    GET: Get user settings
    PUT: Update user settings
    """
    print(f"🔍 Settings API - User: {request.user}, Authenticated: {request.user.is_authenticated}")
    if not request.user.is_authenticated:
        print(f"❌ Settings API - User not authenticated")
        return Response({'error': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        try:
            from .models import UserSettings
            from .serializer import UserSettingsSerializer
            
            # Get or create settings for the user
            settings, created = UserSettings.objects.get_or_create(user=request.user)
            
            if created:
                print(f"📝 Created new settings for user: {request.user.username}")
            
            serializer = UserSettingsSerializer(settings)
            return Response(serializer.data)
            
        except Exception as e:
            print(f"❌ Error fetching settings: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'PUT':
        try:
            from .models import UserSettings
            from .serializer import UserSettingsSerializer
            
            # Get or create settings for the user
            settings, created = UserSettings.objects.get_or_create(user=request.user)
            
            serializer = UserSettingsSerializer(settings, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                print(f"✅ Settings updated for user: {request.user.username}")
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            print(f"❌ Error updating settings: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def change_password_api(request):
    """Change user password"""
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        from django.contrib.auth import authenticate
        
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        
        if not current_password or not new_password:
            return Response({'error': 'Both current and new passwords are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify current password
        user = authenticate(username=request.user.username, password=current_password)
        if not user:
            return Response({'error': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate new password length
        if len(new_password) < 8:
            return Response({'error': 'Password must be at least 8 characters long'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Set new password
        request.user.set_password(new_password)
        request.user.save()
        
        print(f"✅ Password changed for user: {request.user.username}")
        
        # Update session to prevent logout
        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(request, request.user)
        
        return Response({'success': True, 'message': 'Password changed successfully'})
        
    except Exception as e:
        print(f"❌ Error changing password: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
def export_user_data_api(request):
    """Export user data"""
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        import json
        from django.core import serializers
        from django.http import HttpResponse
        
        # Collect user data
        user_data = {
            'profile': {
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'role': request.user.role,
                'phone_number': request.user.phone_number,
                'bio': request.user.bio,
                'date_joined': request.user.date_joined.isoformat() if request.user.date_joined else None
            }
        }
        
        # Add role-specific data
        if request.user.role == 'teacher':
            user_data['profile']['department'] = request.user.department
            user_data['profile']['years_of_experience'] = request.user.years_of_experience
            
            # Get teacher's activities
            from .models import PortfolioActivity
            activities = PortfolioActivity.objects.filter(folder__teacher=request.user)
            user_data['activities'] = [{
                'title': a.title,
                'description': a.description,
                'activity_type': a.activity_type,
                'max_score': a.max_score,
                'created_at': a.created_at.isoformat() if a.created_at else None
            } for a in activities]
            
        elif request.user.role == 'student':
            user_data['profile']['grade_level'] = request.user.grade_level
            user_data['profile']['section'] = request.user.section
            user_data['profile']['id_number'] = request.user.id_number
            
            # Get student's submissions
            from .models import StudentSubmission
            submissions = StudentSubmission.objects.filter(student=request.user)
            user_data['submissions'] = [{
                'activity': s.activity.title if s.activity else 'Sketch',
                'status': s.status,
                'score': s.score,
                'submitted_at': s.submitted_at.isoformat() if s.submitted_at else None
            } for s in submissions]
        
        # Get user settings
        from .models import UserSettings
        settings = UserSettings.objects.filter(user=request.user).first()
        if settings:
            from .serializer import UserSettingsSerializer
            user_data['settings'] = UserSettingsSerializer(settings).data
        
        # Create JSON response
        response = HttpResponse(
            json.dumps(user_data, indent=2),
            content_type='application/json'
        )
        response['Content-Disposition'] = f'attachment; filename="user_data_{request.user.username}.json"'
        
        print(f"✅ Data exported for user: {request.user.username}")
        return response
        
    except Exception as e:
        print(f"❌ Error exporting data: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
