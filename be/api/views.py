from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from inertia import render as inertia_render
from .middleware import teacher_required, student_required
from .models import User, PortfolioFolder, PortfolioActivity, StudentSubmission, SubmissionFile, Notification, Remark, RemarkReadStatus, PortfolioCompilationRequest, NewsfeedPost, PostLike, PostComment, Student, Classroom
from .serializer import PortfolioFolderSerializer, PortfolioActivitySerializer, StudentSubmissionSerializer, SubmissionFileSerializer, NotificationSerializer, RemarkSerializer
import json
import os
import csv
from io import StringIO


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


@csrf_exempt
@csrf_exempt
@api_view(['POST'])
def logout_api(request):
    """
    API endpoint for user logout
    Clears the server-side session
    """
    try:
        # Logout the user (clears server-side session)
        auth_logout(request)

        return Response({
            'success': True,
            'message': 'Logged out successfully'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Logout API error: {str(e)}")
        return Response({
            'success': False,
            'error': 'An error occurred during logout'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([])  # Allow any user to access login endpoint
def login_api(request):
    """
    API endpoint for user login with email and password
    Returns user data and authentication status
    """
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role')  # Optional role verification

        if not email or not password:
            return Response({
                'success': False,
                'error': 'Email and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Try to find user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Invalid email or password'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Authenticate user
        authenticated_user = authenticate(request, username=user.username, password=password)

        if authenticated_user is not None:
            # Verify role if provided
            if role and authenticated_user.role != role:
                return Response({
                    'success': False,
                    'error': f'This account is not registered as a {role}'
                }, status=status.HTTP_403_FORBIDDEN)

            # Log the user in
            auth_login(request, authenticated_user)

            # IMPORTANT: Explicitly save the session to ensure it's persisted
            request.session.save()

            # Prepare user data
            user_data = {
                'id': authenticated_user.id,
                'username': authenticated_user.username,
                'email': authenticated_user.email,
                'role': authenticated_user.role,
                'name': f"{authenticated_user.first_name} {authenticated_user.last_name}".strip() or authenticated_user.username,
                'first_name': authenticated_user.first_name,
                'last_name': authenticated_user.last_name,
            }

            # Add role-specific data
            if authenticated_user.role == 'student':
                user_data['student_id'] = authenticated_user.id_number
                user_data['grade_level'] = authenticated_user.grade_level
                user_data['section'] = authenticated_user.section
                user_data['has_classroom'] = authenticated_user.classroom is not None
            elif authenticated_user.role == 'teacher':
                user_data['department'] = authenticated_user.department

            # Create response with explicit session cookie
            response = Response({
                'success': True,
                'user': user_data,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)

            # Ensure session cookie is set in response
            if request.session.session_key:
                response.set_cookie(
                    key='sessionid',
                    value=request.session.session_key,
                    httponly=True,
                    samesite='Lax',
                    secure=False  # Set to True in production with HTTPS
                )

            return response
        else:
            return Response({
                'success': False,
                'error': 'Invalid email or password'
            }, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        print(f"Login API error: {str(e)}")
        return Response({
            'success': False,
            'error': 'An error occurred during login'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
def student_school_year(request):
    """Student school year management page"""
    return inertia_render(request, 'Student/SchoolYear')


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

            # Serialize classroom if it exists
            classroom_data = None
            if request.user.classroom:
                classroom_data = {
                    'id': request.user.classroom.id,
                    'name': str(request.user.classroom)
                }

            return JsonResponse({
                'authenticated': True,
                'user': {
                    'id': request.user.id,
                    'name': request.user.get_full_name() or request.user.username,
                    'full_name': request.user.get_full_name() or request.user.username,
                    'username': request.user.username,
                    'email': request.user.email,
                    'role': request.user.role,
                    'classroom': classroom_data,
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

            # Serialize classroom if it exists
            classroom_data = None
            if user.classroom:
                classroom_data = {
                    'id': user.classroom.id,
                    'name': str(user.classroom)
                }

            return JsonResponse({
                'authenticated': True,
                'user': {
                    'id': user.id,
                    'name': user.get_full_name() or user.username,
                    'full_name': user.get_full_name() or user.username,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'classroom': classroom_data,
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
    Supports school_year query parameter for viewing archived school years
    """
    if request.method == 'GET':
        try:
            # Filter folders based on user role and classroom
            classroom_id = request.query_params.get('classroom_id')
            school_year_filter = request.query_params.get('school_year', None)

            if classroom_id:
                # If a classroom_id is provided, filter by it (for teacher's main view)
                try:
                    classroom = Classroom.objects.get(id=classroom_id)
                    # Teachers should only see their own folders in this classroom
                    if request.user.role == 'teacher':
                        folders = PortfolioFolder.objects.filter(
                            classroom=classroom,
                            teacher=request.user
                        ).order_by('-created_at')
                        print(f"📚 Teacher {request.user.username} viewing their own folders in classroom: {classroom.name}")
                    else:
                        # Students see ALL folders for their classroom (from any teacher)
                        # Check if student is currently in this classroom OR was previously in it
                        is_current_student = request.user.classroom == classroom
                        
                        # Check if student was previously in this classroom via teacher promotion
                        from .models import StudentPromotionHistory, StudentClassroomHistory
                        was_promoted_from = StudentPromotionHistory.objects.filter(
                            student=request.user,
                            previous_classroom=classroom
                        ).exists()
                        
                        # Check if student archived this classroom themselves
                        was_student_archived = StudentClassroomHistory.objects.filter(
                            student=request.user,
                            classroom=classroom
                        ).exists()
                        
                        if is_current_student or was_promoted_from or was_student_archived:
                            folders = PortfolioFolder.objects.filter(
                                classroom=classroom
                            ).order_by('-created_at')
                            print(f"📚 Student viewing all folders in classroom: {classroom.name}, found {folders.count()}")
                        else:
                            return Response({'error': 'You do not have permission to view this classroom'}, status=status.HTTP_403_FORBIDDEN)
                except Classroom.DoesNotExist:
                    return Response({'error': 'Classroom not found.'}, status=status.HTTP_404_NOT_FOUND)
            elif school_year_filter:
                # Filter by specific school year (for archived view mode)
                if request.user.role == 'teacher':
                    folders = PortfolioFolder.objects.filter(
                        teacher=request.user,
                        classroom__school_year=school_year_filter
                    ).order_by('-created_at')
                    print(f"📚 Teacher {request.user.username} viewing folders for school year: {school_year_filter}, found {folders.count()}")
                else:
                    folders = PortfolioFolder.objects.none()
            else:
                # If no classroom_id, use role-based logic (for sidebar and student view)
                if request.user.role == 'teacher':
                    # Check if we should filter by current school year only
                    current_sy_only = request.query_params.get('current_school_year', 'false').lower() == 'true'
                    
                    # Teacher sidebar gets all folders they own
                    folders = PortfolioFolder.objects.filter(teacher=request.user).order_by('-created_at')
                    
                    # If current_school_year=true, filter to only show folders from current school year
                    if current_sy_only:
                        from .models import SchoolYear
                        current_sy = SchoolYear.get_current_for_teacher(request.user)
                        if current_sy:
                            folders = folders.filter(
                                classroom__school_year=current_sy.name,
                                classroom__is_archived=False
                            )
                            print(f"📚 Teacher {request.user.username} viewing folders for current school year: {current_sy.name}, found {folders.count()}")
                        else:
                            # Fallback: show folders from non-archived classrooms
                            folders = folders.filter(classroom__is_archived=False)
                            print(f"📚 Teacher {request.user.username} viewing folders from non-archived classrooms")
                    else:
                        print(f"📚 Teacher {request.user.username} viewing all their folders for the sidebar.")
                elif request.user.role == 'student':
                    # Student gets ALL folders for their assigned classroom (from any teacher)
                    student_classroom = request.user.classroom
                    if student_classroom:
                        # Show all folders for the student's classroom regardless of which teacher created them
                        folders = PortfolioFolder.objects.filter(
                            classroom=student_classroom
                        ).order_by('-created_at')
                        print(f"📚 Student {request.user.username} viewing all folders in classroom: {student_classroom.name}, found {folders.count()} folders")
                    else:
                        folders = PortfolioFolder.objects.none()
                        print(f"⚠️ Student {request.user.username} has no classroom assigned.")
                else:
                    # Fallback for other roles
                    folders = PortfolioFolder.objects.none()

            serializer = PortfolioFolderSerializer(folders, many=True, context={'request': request})
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

            # Get classroom based on class_name - prioritize current school year
            classroom = None
            try:
                from .models import SchoolYear
                
                # Get the teacher's current school year
                current_sy = SchoolYear.get_current_for_teacher(request.user)
                
                # First try to find a non-archived classroom with this name assigned to the teacher for CURRENT school year
                if current_sy:
                    classroom = Classroom.objects.filter(
                        name=class_name,
                        is_archived=False,
                        teacher=request.user,
                        school_year=current_sy.name  # Match current school year
                    ).first()
                    if classroom:
                        print(f"✅ Found classroom for current school year: {classroom.name} (ID: {classroom.id}, School Year: {classroom.school_year})")
                
                # If not found for current school year, try any non-archived classroom assigned to teacher
                if not classroom:
                    classroom = Classroom.objects.filter(
                        name=class_name,
                        is_archived=False,
                        teacher=request.user
                    ).first()
                
                # If not found, try any non-archived classroom with this name
                if not classroom:
                    classroom = Classroom.objects.filter(
                        name=class_name,
                        is_archived=False
                    ).first()
                
                # Last resort: any classroom with this name
                if not classroom:
                    classroom = Classroom.objects.filter(
                        name=class_name
                    ).first()

                if classroom:
                    print(f"✅ Found classroom: {classroom.name} (ID: {classroom.id}, School Year: {classroom.school_year}, Archived: {classroom.is_archived})")
                else:
                    print(f"⚠️ No classroom found for class_name: {class_name}")
            except Exception as e:
                print(f"❌ Error finding classroom: {str(e)}")

            # Check for duplicate folder name - use classroom (which is unique per school year) instead of class_name
            if classroom:
                existing_folder = PortfolioFolder.objects.filter(
                    teacher=request.user,
                    name=name,
                    classroom=classroom  # Check against specific classroom (includes school year context)
                ).first()
            else:
                # Fallback to class_name check if no classroom found
                existing_folder = PortfolioFolder.objects.filter(
                    teacher=request.user,
                    name=name,
                    class_name=class_name,
                    classroom__isnull=True  # Only check folders without classroom link
                ).first()

            if existing_folder:
                return Response({
                    'error': 'Duplicate folder name',
                    'detail': f'A folder with the exact name "{name}" already exists in {class_name}. Please choose a different name.'
                }, status=status.HTTP_400_BAD_REQUEST)

            folder = PortfolioFolder.objects.create(
                teacher=request.user,
                name=name,
                class_name=class_name,
                classroom=classroom,  # Link to actual Classroom model
                description=description
            )

            # Notify ONLY students in this specific classroom
            if classroom:
                students = User.objects.filter(
                    role='student',
                    classroom=classroom
                ).exclude(username='admin')
                print(f"📢 Notifying {students.count()} students in {classroom.name} about new portfolio")
            else:
                # Fallback: notify all students (legacy behavior)
                students = User.objects.filter(role='student').exclude(username='admin')
                print(f"📢 Notifying {students.count()} students (no specific classroom) about new portfolio")

            for student in students:
                notification = create_notification(
                    recipient=student,
                    notification_type='portfolio_created',
                    title='New Portfolio Created',
                    message=f'Teacher {request.user.get_full_name() or request.user.username} created a new portfolio: {name}',
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
    GET: Retrieve details of a specific portfolio folder.
    PUT: Update a specific portfolio folder.
    DELETE: Delete a specific portfolio folder.
    """
    try:
        folder = PortfolioFolder.objects.get(id=folder_id)
    except PortfolioFolder.DoesNotExist:
        return Response({'error': 'Folder not found'}, status=status.HTTP_404_NOT_FOUND)

    # --- Centralized Permissions Check ---
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.user.role == 'student':
        # Students can only view folder details, not modify them.
        if request.method != 'GET':
            return Response({'error': 'Permission denied: Students cannot modify folders.'}, status=status.HTTP_403_FORBIDDEN)
        if folder.classroom != request.user.classroom:
            return Response({'error': 'You do not have permission to access this folder.'}, status=status.HTTP_403_FORBIDDEN)

    elif request.user.role == 'teacher':
        if folder.teacher != request.user:
            return Response({'error': 'You do not have permission to access this folder.'}, status=status.HTTP_403_FORBIDDEN)
    else:
        # Other roles have no access.
        return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    # --- Method-Specific Logic ---
    if request.method == 'GET':
        serializer = PortfolioFolderSerializer(folder)
        return Response(serializer.data)

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            new_name = data.get('name', folder.name).strip()
            new_class_name = data.get('class_name', folder.class_name)

            if not new_name:
                return Response({'error': 'Folder name cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if class is being changed
            if new_class_name and new_class_name != folder.class_name:
                # Find the new classroom - prioritize current school year
                from .models import SchoolYear
                current_sy = SchoolYear.get_current_for_teacher(request.user)
                
                new_classroom = None
                if current_sy:
                    new_classroom = Classroom.objects.filter(
                        name=new_class_name,
                        school_year=current_sy.name,
                        is_archived=False
                    ).first()
                
                # Fallback: try any non-archived classroom
                if not new_classroom:
                    new_classroom = Classroom.objects.filter(
                        name=new_class_name,
                        is_archived=False
                    ).first()
                
                # Last resort: any classroom with this name
                if not new_classroom:
                    new_classroom = Classroom.objects.filter(name=new_class_name).first()
                
                if new_classroom:
                    # Check if folder with same name exists in new class
                    if PortfolioFolder.objects.filter(classroom=new_classroom, name=new_name, teacher=request.user).exclude(id=folder.id).exists():
                        return Response({'error': f'A folder named "{new_name}" already exists in {new_class_name}.'}, status=status.HTTP_400_BAD_REQUEST)
                    folder.classroom = new_classroom
                    folder.class_name = new_class_name
                    print(f"📂 Moving folder to {new_class_name}")
                else:
                    return Response({'error': f'Classroom "{new_class_name}" not found.'}, status=status.HTTP_404_NOT_FOUND)
            elif new_name != folder.name:
                # Just renaming, check for duplicates in same class
                if PortfolioFolder.objects.filter(classroom=folder.classroom, name=new_name, teacher=request.user).exclude(id=folder.id).exists():
                    return Response({'error': f'A folder named "{new_name}" already exists in this class.'}, status=status.HTTP_400_BAD_REQUEST)

            folder.name = new_name
            folder.description = data.get('description', folder.description)
            folder.save()
            
            print(f"✅ Folder updated: {folder.name} in {folder.class_name}")
            serializer = PortfolioFolderSerializer(folder)
            return Response(serializer.data)

        except json.JSONDecodeError:
            return Response({'error': 'Invalid request format.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error during folder update: {e}")
            return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'DELETE':
        if folder.activities.count() > 0:
            return Response({'error': 'Cannot drop a folder with activities. Please remove all activities first.'}, status=status.HTTP_400_BAD_REQUEST)

        folder.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET', 'POST'])
def portfolio_activities_api(request, folder_id):
    """
    GET: List activities in a folder
    POST: Add activity to folder (teacher only)
    """
    try:
        folder = PortfolioFolder.objects.get(id=folder_id)

        # Authorization check: Ensure the user has permission to view this folder.
        if request.user.role == 'student':
            # Students can access folders in their current classroom OR archived classrooms they were in
            is_current_classroom = folder.classroom == request.user.classroom
            
            # Check if student was previously in this classroom (archived view mode)
            from .models import StudentPromotionHistory, StudentClassroomHistory
            was_promoted_from = StudentPromotionHistory.objects.filter(
                student=request.user,
                previous_classroom=folder.classroom
            ).exists()
            
            was_student_archived = StudentClassroomHistory.objects.filter(
                student=request.user,
                classroom=folder.classroom
            ).exists()
            
            if not is_current_classroom and not was_promoted_from and not was_student_archived:
                return Response({'error': 'Permission denied: You can only access folders in your classroom.'}, status=status.HTTP_403_FORBIDDEN)
        elif request.user.role == 'teacher':
            # Teachers can only access folders they own.
            if folder.teacher != request.user:
                return Response({'error': 'Permission denied: You can only access your own folders.'}, status=status.HTTP_403_FORBIDDEN)

    except PortfolioFolder.DoesNotExist:
        return Response({'error': 'Folder not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Teachers see all activities, students only see published ones
        if request.user.is_authenticated and request.user.role == 'teacher':
            activities = folder.activities.all().order_by('-created_at')
        else:
            # Students only see published activities, ordered by most recently published first
            activities = folder.activities.filter(is_published=True).order_by('-published_at', '-created_at')

        serializer = PortfolioActivitySerializer(activities, many=True, context={'request': request})
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

                # Handle instruction file uploads
                instruction_files = request.FILES.getlist('instruction_files')
                if instruction_files:
                    from .models import ActivityInstructionFile
                    for uploaded_file in instruction_files:
                        ActivityInstructionFile.objects.create(
                            activity=activity,
                            file=uploaded_file,
                            file_name=uploaded_file.name,
                            file_type=uploaded_file.content_type,
                            file_size=uploaded_file.size
                        )
                    print(f"Saved {len(instruction_files)} instruction files for activity {activity.id}")

                # Activity is created as draft (is_published=False by default)
                # No notifications sent until teacher publishes it

                # Re-serialize to include instruction files
                serializer = PortfolioActivitySerializer(activity, context={'request': request})
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
        serializer = PortfolioActivitySerializer(activity, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Only teachers can update
        if not request.user.is_authenticated or request.user.role != 'teacher':
            return Response({'error': 'Only teachers can update activities'}, status=status.HTTP_403_FORBIDDEN)

        try:
            data = request.data
            print(f"Updating activity {activity_id} with data: {data}")

            # Note: Teachers can edit activities even after the due date has passed
            # This allows them to fix mistakes like incorrect due dates/times

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

            # Handle instruction file uploads
            instruction_files = request.FILES.getlist('instruction_files')
            if instruction_files:
                from .models import ActivityInstructionFile
                for uploaded_file in instruction_files:
                    ActivityInstructionFile.objects.create(
                        activity=activity,
                        file=uploaded_file,
                        file_name=uploaded_file.name,
                        file_type=uploaded_file.content_type,
                        file_size=uploaded_file.size
                    )
                print(f"Saved {len(instruction_files)} new instruction files for activity {activity.id}")

            # Handle deletion of existing instruction files
            delete_file_ids = data.get('delete_instruction_file_ids', [])
            if delete_file_ids:
                from .models import ActivityInstructionFile
                if isinstance(delete_file_ids, str):
                    import json
                    delete_file_ids = json.loads(delete_file_ids)
                ActivityInstructionFile.objects.filter(id__in=delete_file_ids, activity=activity).delete()
                print(f"Deleted {len(delete_file_ids)} instruction files from activity {activity.id}")

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
            serializer = PortfolioActivitySerializer(activity, context={'request': request})
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

        # Notify ONLY students in the activity's classroom
        activity_classroom = activity.folder.classroom

        if activity_classroom:
            students = User.objects.filter(
                role='student',
                classroom=activity_classroom
            ).exclude(username='admin')
            print(f"📢 Notifying {students.count()} students in {activity_classroom.name} about published activity")
        else:
            # Fallback: notify all students if no classroom assigned (legacy behavior)
            students = User.objects.filter(role='student').exclude(username='admin')
            print(f"⚠️ No classroom assigned to folder, notifying all {students.count()} students")

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

        # Notify ONLY students in the activity's classroom that it has been retracted
        activity_classroom = activity.folder.classroom

        if activity_classroom:
            students = User.objects.filter(
                role='student',
                classroom=activity_classroom
            ).exclude(username='admin')
            print(f"📢 Notifying {students.count()} students in {activity_classroom.name} about retracted activity")
        else:
            # Fallback: notify all students if no classroom assigned
            students = User.objects.filter(role='student').exclude(username='admin')
            print(f"⚠️ No classroom assigned to folder, notifying all {students.count()} students")

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

        # Teachers see all submissions FROM THEIR CLASSROOM, students see only their own
        if request.user.role == 'teacher':
            # Check if we should show only scored submissions (for Special Progress view)
            show_scored_only = request.GET.get('scored_only', 'false').lower() == 'true'

            # Get teacher's classroom(s) for this activity
            activity_classroom = activity.folder.classroom

            print(f"🎓 Activity {activity_id} - Classroom: {activity_classroom.name if activity_classroom else 'None'}, Archived: {activity_classroom.is_archived if activity_classroom else 'N/A'}")

            # For archived classrooms, get students from promotion history
            if activity_classroom and activity_classroom.is_archived:
                from .models import StudentPromotionHistory
                
                # Get student IDs from promotion history (students who were in this classroom)
                promotion_student_ids = StudentPromotionHistory.objects.filter(
                    previous_classroom=activity_classroom
                ).values_list('student_id', flat=True).distinct()
                
                # Also include students still assigned (shouldn't happen but just in case)
                current_student_ids = User.objects.filter(
                    classroom=activity_classroom, role='student'
                ).values_list('id', flat=True)
                
                # Combine both sets
                all_student_ids = set(promotion_student_ids) | set(current_student_ids)
                
                print(f"📚 Archived classroom - Loading submissions from {len(all_student_ids)} historical students")
                
                # Get submissions from these students for this activity
                if include_drafts:
                    all_submissions = StudentSubmission.objects.filter(
                        activity=activity,
                        student_id__in=all_student_ids
                    ).order_by('-submitted_at')
                else:
                    all_submissions = StudentSubmission.objects.filter(
                        activity=activity,
                        student_id__in=all_student_ids
                    ).exclude(status='draft').order_by('-submitted_at')
            else:
                # Non-archived classroom - use current classroom assignment
                # Teachers see only final submissions (not drafts) unless specifically requested
                # AND only from students in their assigned classroom
                if include_drafts:
                    all_submissions = StudentSubmission.objects.filter(
                        activity=activity,
                        student__classroom=activity_classroom  # Filter by classroom
                    ).order_by('-submitted_at')
                else:
                    all_submissions = StudentSubmission.objects.filter(
                        activity=activity,
                        student__classroom=activity_classroom  # Filter by classroom
                    ).exclude(status='draft').order_by('-submitted_at')

            # If scored_only is requested, filter to only scored submissions
            if show_scored_only:
                all_submissions = all_submissions.filter(status='scored')
                print(f"📊 Activity {activity_id}: Filtering for SCORED submissions only")

            # Get LATEST submission per student (handling resubmissions)
            # Group by student and get the most recent submission for each
            from django.db.models import Max
            latest_submission_ids = []
            student_latest = {}

            for submission in all_submissions:
                student_id = submission.student.id
                if student_id not in student_latest:
                    student_latest[student_id] = submission.id
                    latest_submission_ids.append(submission.id)

            # Filter to only include latest submissions
            submissions = StudentSubmission.objects.filter(
                id__in=latest_submission_ids
            ).order_by('-submitted_at')

            print(f"📊 Activity {activity_id}: Total submissions={all_submissions.count()}, Latest per student={submissions.count()}, Scored only={show_scored_only}")

            # Use lightweight serializer for teachers (excludes large file_path)
            from .serializer import StudentSubmissionListSerializer
            serializer = StudentSubmissionListSerializer(submissions, many=True, context={'request': request})
        else:
            # Students can request all submissions including drafts
            if include_drafts:
                submissions = StudentSubmission.objects.filter(
                    activity=activity,
                    student=request.user,
                    is_active=True  # Only show active submissions
                ).order_by('-submitted_at')
            else:
                # By default, exclude drafts
                submissions = StudentSubmission.objects.filter(
                    activity=activity,
                    student=request.user,
                    is_active=True  # Only show active submissions
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
            existing_submissions = StudentSubmission.objects.filter(
                activity=activity,
                student=request.user,
                is_active=True  # Only check active submissions
            ).order_by('-submitted_at')

            # Clean up duplicate drafts - keep only the most recent one
            if existing_submissions.count() > 1:
                draft_submissions = existing_submissions.filter(status='draft')
                if draft_submissions.count() > 1:
                    # Keep the most recent draft, delete the rest
                    drafts_to_delete = draft_submissions[1:]
                    for draft in drafts_to_delete:
                        print(f"🗑️ Deleting duplicate draft submission {draft.id}")
                        draft.delete()
                    print(f"✅ Cleaned up {len(drafts_to_delete)} duplicate draft(s)")

            existing_submission = existing_submissions.first()

            if existing_submission:
                from django.utils import timezone

                # Check if this is a draft being updated
                is_draft = data.get('is_draft', True)
                if isinstance(is_draft, str):
                    is_draft = is_draft.lower() in ('true', '1', 'yes')
                else:
                    is_draft = bool(is_draft)

                # If existing submission is a draft and new one is also a draft,
                # just update it WITHOUT incrementing resubmit count
                if existing_submission.status == 'draft' and is_draft:
                    print(f"📝 Updating existing draft submission {existing_submission.id}")
                    print(f"📊 Current resubmit_count: {existing_submission.resubmit_count}, last_resubmit_at: {existing_submission.last_resubmit_at}")

                    # Update the draft with new file
                    file_obj = request.FILES.get('file')
                    if file_obj:
                        existing_submission.file = file_obj
                        # Auto-detect file type
                        content_type = file_obj.content_type
                        if content_type.startswith('image/'):
                            existing_submission.file_type = 'image'
                        elif content_type == 'application/pdf':
                            existing_submission.file_type = 'pdf'
                        elif content_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                            existing_submission.file_type = 'document'
                        else:
                            existing_submission.file_type = 'file'

                    if 'caption' in data:
                        existing_submission.caption = data.get('caption', '')
                    if 'file_path' in data:
                        existing_submission.file_path = data.get('file_path', '')

                    # IMPORTANT: Preserve resubmit_count and last_resubmit_at when updating draft
                    existing_submission.save()
                    print(f"✅ Draft updated - resubmit_count preserved: {existing_submission.resubmit_count}")
                    print(f"📎 File saved: {existing_submission.file.url if existing_submission.file else 'No file'}")

                    serializer = StudentSubmissionSerializer(existing_submission, context={'request': request})
                    print(f"📤 Returning file_url: {serializer.data.get('file_url')}")
                    return Response(serializer.data, status=status.HTTP_200_OK)

                # If existing submission is a draft and we're turning it in (is_draft=False),
                # this is the FIRST submission, NOT a resubmission - don't increment count
                if existing_submission.status == 'draft' and not is_draft:
                    print(f"📤 Turning in draft submission {existing_submission.id} for the FIRST time")
                    print(f"📊 Current resubmit_count: {existing_submission.resubmit_count} (should stay 0)")

                    # Update the submission with new data
                    file_obj = request.FILES.get('file')
                    if file_obj:
                        existing_submission.file = file_obj
                        content_type = file_obj.content_type
                        if content_type.startswith('image/'):
                            existing_submission.file_type = 'image'
                        elif content_type == 'application/pdf':
                            existing_submission.file_type = 'pdf'
                        elif content_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                            existing_submission.file_type = 'document'
                        else:
                            existing_submission.file_type = 'file'

                    if 'caption' in data:
                        existing_submission.caption = data.get('caption', '')
                    if 'file_path' in data:
                        existing_submission.file_path = data.get('file_path', '')

                    # Set status to unscored (first submission)
                    import pytz
                    manila_tz = pytz.timezone('Asia/Manila')
                    existing_submission.status = 'unscored'
                    existing_submission.submitted_at = timezone.now().astimezone(manila_tz)

                    # Check if late
                    if activity.due_date:
                        from datetime import datetime, time as dt_time
                        if activity.due_time:
                            due_datetime = timezone.make_aware(
                                datetime.combine(activity.due_date, activity.due_time)
                            )
                        else:
                            due_datetime = timezone.make_aware(
                                datetime.combine(activity.due_date, dt_time(23, 59, 59))
                            )
                        existing_submission.is_late = timezone.now() > due_datetime

                    # IMPORTANT: Do NOT increment resubmit_count - this is the first submission
                    # resubmit_count should remain 0
                    existing_submission.save()
                    print(f"✅ First submission turned in - resubmit_count: {existing_submission.resubmit_count}")

                    # Send notification to teacher about the first submission
                    teacher = activity.folder.teacher
                    print(f"📧 Sending 'submission_received' notification to {teacher.username} for first submission")
                    create_notification(
                        recipient=teacher,
                        notification_type='submission_received',
                        title='New Submission Received',
                        message=f'{request.user.username} submitted work for "{activity.title}"',
                        submission=existing_submission,
                        activity=activity
                    )

                    serializer = StudentSubmissionSerializer(existing_submission, context={'request': request})
                    return Response(serializer.data, status=status.HTTP_200_OK)

                # This is a TRUE resubmission - student is submitting new work after already submitting
                print(f"🔄 Resubmission detected for existing submission {existing_submission.id}")
                print(f"📊 Current resubmit_count: {existing_submission.resubmit_count}")

                # Check if this is a portfolio compilation submission (no resubmit limits)
                is_portfolio_compilation = data.get('is_portfolio_compilation', False)
                if isinstance(is_portfolio_compilation, str):
                    is_portfolio_compilation = is_portfolio_compilation.lower() in ('true', '1', 'yes')
                else:
                    is_portfolio_compilation = bool(is_portfolio_compilation)

                # Check resubmit limit (only for regular submissions, not portfolio compilation)
                if not is_portfolio_compilation:
                    MAX_RESUBMITS = 3
                    if existing_submission.resubmit_count >= MAX_RESUBMITS:
                        return Response({
                            'error': f'Maximum resubmit limit ({MAX_RESUBMITS}) reached',
                            'resubmit_count': existing_submission.resubmit_count,
                            'max_resubmits': MAX_RESUBMITS
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    print(f"📋 Portfolio compilation submission - skipping resubmit limit check")

                # Increment resubmit count
                existing_submission.resubmit_count += 1
                print(f"✅ Incrementing resubmit_count to: {existing_submission.resubmit_count}")

                # Update existing submission with new data
                existing_submission.caption = data.get('caption', '')
                existing_submission.file_path = data.get('file_path', '')
                existing_submission.file_type = data.get('file_type', '')
                import pytz
                manila_tz = pytz.timezone('Asia/Manila')
                # Get current time in Manila timezone
                current_time = timezone.now()
                existing_submission.last_resubmit_at = current_time
                existing_submission.submitted_at = current_time  # Update submission time

                # Check for compilation flag from request (to handle detached compilation flows)
                is_compilation_req = data.get('is_compilation', False)
                if isinstance(is_compilation_req, str):
                    is_compilation_req = is_compilation_req.lower() in ('true', '1', 'yes')
                else:
                    is_compilation_req = bool(is_compilation_req)

                # Set status logic
                is_compiled = (existing_submission.compiled if hasattr(existing_submission, 'compiled') else False) or is_compilation_req

                if is_compiled:
                    print(f"✅ Updating COMPILED submission - keeping status as SCORED")
                    existing_submission.status = 'scored'
                    # Force compilation flags if requested
                    if is_compilation_req:
                        existing_submission.compiled = True
                        existing_submission.is_compilation = True
                        existing_submission.missing = False
                        if not existing_submission.compiled_at:
                             existing_submission.compiled_at = timezone.now()
                    # Don't reset score if it's compiled (it should be None anyway, or stay as is)
                else:
                    # Regular resubmission - reset to unscored
                    existing_submission.status = 'unscored'
                    existing_submission.score = None
                    existing_submission.feedback = None
                    existing_submission.criteria_scores = None
                    existing_submission.scored_at = None

                # Check if this update is late (if not already marked as late)
                if not existing_submission.is_late and activity.due_date:
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

                # Handle multiple files for resubmission - delete old files and add new ones
                files_data = data.get('files', [])
                if files_data and len(files_data) > 0:
                    print(f"📁 Processing {len(files_data)} files for resubmission")
                    # Delete existing files
                    SubmissionFile.objects.filter(submission=existing_submission).delete()
                    print(f"🗑️ Deleted old submission files")
                    
                    # Add new files
                    for idx, f_data in enumerate(files_data):
                        if not f_data:
                            continue
                        
                        f_type = 'file'
                        if isinstance(f_data, str) and f_data.startswith('data:'):
                            format_part = f_data.split(';base64,')[0]
                            f_type = 'image' if 'image' in format_part else ('pdf' if 'pdf' in format_part else 'file')
                        
                        try:
                            sub_file = SubmissionFile.objects.create(
                                submission=existing_submission,
                                file_path=f_data,
                                file_type=f_type,
                                file_name=f"file_{idx + 1}"
                            )
                            print(f"✅ Added file {idx + 1} to resubmission (type: {f_type}): {sub_file.id}")
                        except Exception as file_error:
                            print(f"⚠️ Error adding file {idx + 1}: {str(file_error)}")

                print(f"✅ Resubmission #{existing_submission.resubmit_count} (Version {existing_submission.submission_version}) for student {request.user.username}")

                # Send notification to teacher about resubmission
                teacher = activity.folder.teacher
                print(f"📧 Sending 'submission_received' notification to {teacher.username} for resubmission")
                create_notification(
                    recipient=teacher,
                    notification_type='submission_received',
                    title='Work Resubmitted',
                    message=f'{request.user.username} resubmitted work for "{activity.title}" (Resubmission #{existing_submission.resubmit_count})',
                    submission=existing_submission,
                    activity=activity
                )

                serializer = StudentSubmissionSerializer(existing_submission, context={'request': request})
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

                # Check compilation flag
                is_compilation_req = data.get('is_compilation', False)
                if isinstance(is_compilation_req, str):
                    is_compilation_req = is_compilation_req.lower() in ('true', '1', 'yes')
                else:
                    is_compilation_req = bool(is_compilation_req)

                # Set status based on draft flag and compilation
                if is_compilation_req:
                    submission_status = 'scored'
                else:
                    submission_status = 'draft' if is_draft else 'unscored'

                # Set submitted_at for non-draft submissions
                import pytz
                manila_tz = pytz.timezone('Asia/Manila')
                submission_time = timezone.now()

                submission = StudentSubmission.objects.create(
                    activity=activity,
                    student=request.user,
                    caption=data.get('caption', ''),
                    file=file_obj if file_obj else None,  # Store actual file if provided
                    file_path=file_path,  # Store base64 as fallback
                    file_type=file_type,
                    status=submission_status,
                    post_to_feed=post_to_feed,

                    # Compilation fields
                    is_compilation=is_compilation_req,
                    compiled=is_compilation_req,
                    missing=False if is_compilation_req else True,
                    compiled_at=submission_time if is_compilation_req else None,
                    submitted_at=submission_time if (is_compilation_req or not is_draft) else None,  # Set submitted_at for compilations and final submissions
                    scored_at=submission_time if is_compilation_req else None,  # Set scored_at for compilations
                    approval_status='pending' if post_to_feed else 'approved',
                    is_late=is_late
                )

                # Handle multiple files if provided
                files_data = data.get('files', [])
                if files_data and len(files_data) > 0:
                    print(f"📁 Processing {len(files_data)} files for submission")
                    for idx, f_data in enumerate(files_data):
                        if not f_data:
                            continue
                        
                        f_type = 'file'
                        if isinstance(f_data, str) and f_data.startswith('data:'):
                            format_part = f_data.split(';base64,')[0]
                            f_type = 'image' if 'image' in format_part else ('pdf' if 'pdf' in format_part else 'file')
                        
                        try:
                            sub_file = SubmissionFile.objects.create(
                                submission=submission,
                                file_path=f_data,  # Use file_path field for base64 data
                                file_type=f_type,
                                file_name=f"file_{idx + 1}"
                            )
                            print(f"✅ Added file {idx + 1} to submission (type: {f_type}): {sub_file.id}")
                        except Exception as file_error:
                            print(f"⚠️ Error adding file {idx + 1}: {str(file_error)}")

                print(f"✅ Submission created: ID={submission.id}, status={submission_status}, file_type={file_type}, is_late={is_late}, is_draft={is_draft}")
                print(f"📎 File saved: {submission.file.url if submission.file else 'No file'}")
                print(f"📢 POST TO FEED: {post_to_feed}, APPROVAL STATUS: {submission.approval_status}")
                if post_to_feed:
                    print(f"🔔 This submission should appear in teacher's Notice page!")

                # Get teacher for notifications
                teacher = activity.folder.teacher

                # Only notify teacher if this is a final submission (not draft)
                if not is_draft:
                    print(f"📧 Sending 'submission_received' notification to {teacher.username}")
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
                    print(f"📧 Sending 'approval_requested' notification to {teacher.username}")
                    create_notification(
                        recipient=teacher,
                        notification_type='approval_requested',
                        title='Approval Requested',
                        message=f'{request.user.username} requested approval to post "{activity.title}" to newsfeed',
                        submission=submission,
                        activity=activity
                    )

                # IMPORTANT: Include request context so file_url is properly generated
                serializer = StudentSubmissionSerializer(submission, context={'request': request})
                print(f"📤 Returning file_url: {serializer.data.get('file_url')}")
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
    Also includes compiled submissions which should appear in submitted tab
    """
    if not request.user.is_authenticated or request.user.role != 'teacher':
        return Response({'error': 'Only teachers can view unscored submissions'}, status=status.HTTP_403_FORBIDDEN)

    try:
        # Clean up duplicate drafts first
        from django.db.models import Count

        # Find students with multiple draft submissions for the same activity
        duplicate_drafts = StudentSubmission.objects.filter(
            status='draft',
            is_active=True
        ).values('student', 'activity').annotate(
            count=Count('id')
        ).filter(count__gt=1)

        # Delete older duplicate drafts
        for dup in duplicate_drafts:
            drafts = StudentSubmission.objects.filter(
                student_id=dup['student'],
                activity_id=dup['activity'],
                status='draft',
                is_active=True
            ).order_by('-submitted_at')

            # Keep the most recent, delete the rest
            drafts_to_delete = drafts[1:]
            deleted_count = 0
            for draft in drafts_to_delete:
                print(f"🗑️ Cleaning up duplicate draft: {draft.id}")
                draft.delete()
                deleted_count += 1

            if deleted_count > 0:
                print(f"✅ Cleaned up {deleted_count} duplicate draft(s) for student {dup['student']}")

        # Get all unscored submissions - explicitly filter by status='unscored'
        # AND exclude any that have scores (double safety check)
        # ALSO include drafts that have resubmit_count > 0 (student is resubmitting)
        # ALSO include compiled submissions (they should appear in submitted tab)
        # Compiled submissions should appear here if they are NOT scored yet
        from django.db.models import Q, Max

        # SIMPLIFIED QUERY: Get all submissions that should appear in "Submitted" tab
        # This includes:
        # 1. Regular unscored submissions (status='unscored')
        # 2. Drafts with resubmit_count > 0 (student is resubmitting)
        # 3. Compiled submissions that don't have an actual score (score is null)
        #    - Even if scored_at is set (legacy data), if score is null, show in Submitted
        all_unscored = StudentSubmission.objects.filter(
            is_active=True
        ).filter(
            Q(status='unscored') |
            Q(status='draft', resubmit_count__gt=0) |
            # Include ANY compiled submission that doesn't have an actual score
            (Q(compiled=True) & Q(score__isnull=True)) |
            (Q(is_compilation=True) & Q(score__isnull=True))
        )

        # Debug: Log all matching submissions before grouping
        print(f"📊 All unscored/compiled submissions before grouping: {all_unscored.count()}")
        for sub in all_unscored:
            print(f"  - id={sub.id}, student={sub.student.username}, activity={sub.activity_id}, status={sub.status}, compiled={sub.compiled}, is_compilation={sub.is_compilation}, score={sub.score}, scored_at={sub.scored_at}")

        # Now group by student-activity to get latest
        latest_submissions = all_unscored.values('student', 'activity').annotate(
            latest_id=Max('id')
        )

        # Extract the IDs - filter out None values
        latest_ids = [item['latest_id'] for item in latest_submissions if item['latest_id'] is not None]

        # Get only the latest submissions (one per student per activity)
        submissions = StudentSubmission.objects.filter(
            id__in=latest_ids,
            is_active=True  # Double-check is_active
        ).order_by('-submitted_at')

        # Debug: Log compiled submissions
        compiled_count = submissions.filter(Q(compiled=True) | Q(is_compilation=True)).count()
        print(f"📊 Final unscored submissions: Found {submissions.count()} unique submissions (including {compiled_count} compiled)")
        
        # Log details of compiled submissions for debugging
        for sub in submissions.filter(Q(compiled=True) | Q(is_compilation=True)):
            print(f"  📦 Compiled submission: id={sub.id}, student={sub.student.username}, activity={sub.activity_id}, status={sub.status}")

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
    Includes submissions with status='scored' AND has a score AND has scored_at timestamp
    Also includes compiled submissions that have been scored
    """
    if not request.user.is_authenticated or request.user.role != 'teacher':
        return Response({'error': 'Only teachers can view scored submissions'}, status=status.HTTP_403_FORBIDDEN)

    try:
        from django.db.models import Q
        
        # Get submissions that are scored
        # This includes regular scored submissions AND compiled submissions that have been scored
        submissions = StudentSubmission.objects.filter(
            Q(status='scored') |  # Regular scored submissions
            (Q(compiled=True) & Q(score__isnull=False) & Q(scored_at__isnull=False)) |  # Compiled and scored
            (Q(is_compilation=True) & Q(score__isnull=False) & Q(scored_at__isnull=False))  # Compilation and scored
        ).filter(
            score__isnull=False,
            scored_at__isnull=False
        ).distinct().order_by('-scored_at', '-submitted_at')

        print(f"📊 Scored submissions query: Found {submissions.count()} submissions with score (including compiled)")

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
        # Get ALL submitted work by this student (both scored and unscored)
        # Include submissions that have been approved and posted to collection
        from django.db.models import Q

        submissions = StudentSubmission.objects.filter(
            student=request.user,
            submitted_at__isnull=False,  # Only include submissions that have been submitted (not drafts)
            is_active=True,  # Only show active submissions (not hidden from collection)
            status__in=['unscored', 'scored'],  # Include both scored and unscored submissions
        ).filter(
            # Include submissions that are approved OR have no approval status (regular activities)
            Q(approval_status='approved') | Q(approval_status__isnull=True)
        ).select_related('activity', 'activity__folder').order_by('-submitted_at')

        print(f"📦 Processing {submissions.count()} submitted works for student {request.user.username}")

        # Debug: Show what we found
        for sub in submissions:
            print(f"   - Submission #{sub.id}: {sub.activity.title if sub.activity else 'Sketch Pad'} (status: {sub.status}, approval: {sub.approval_status})")

        # Use serializer for consistent formatting and timezone handling
        serializer = StudentSubmissionSerializer(submissions, many=True, context={'request': request})

        print(f"✅ Successfully formatted {len(serializer.data)} submissions for student {request.user.username}")
        return Response(serializer.data)
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
        # Get all submissions with pending approval for this teacher's classrooms
        from django.db.models import Q

        # Get teacher's classrooms from the CURRENT school year
        # This includes classrooms where the teacher has folders
        from .models import SchoolYear
        current_sy = SchoolYear.get_current_for_teacher(request.user)
        
        # Get classroom IDs where teacher has folders in current school year
        teacher_folder_classroom_ids = []
        if current_sy:
            teacher_folder_classroom_ids = list(PortfolioFolder.objects.filter(
                teacher=request.user,
                classroom__school_year=current_sy.name,
                classroom__is_archived=False
            ).values_list('classroom_id', flat=True).distinct())
            print(f"📚 Teacher {request.user.username} has folders in classrooms: {teacher_folder_classroom_ids} (School Year: {current_sy.name})")
        
        # Also include teacher's directly assigned classroom if it's in current school year
        if request.user.classroom and current_sy:
            if request.user.classroom.school_year == current_sy.name and not request.user.classroom.is_archived:
                if request.user.classroom.id not in teacher_folder_classroom_ids:
                    teacher_folder_classroom_ids.append(request.user.classroom.id)

        if not teacher_folder_classroom_ids:
            print(f"⚠️ Teacher {request.user.username} has no classrooms in current school year")
            return Response([], status=status.HTTP_200_OK)

        # Filter by:
        # 1. Pending approval status
        # 2. Student is in one of the teacher's classrooms (current school year)
        # 3. Either has activity from teacher's folder OR is a sketch (activity_id is None)
        from django.db.models import Case, When, Value, IntegerField
        from datetime import datetime

        # Get all pending submissions from students in teacher's classrooms
        submissions = StudentSubmission.objects.filter(
            Q(approval_status='pending') &
            Q(student__classroom_id__in=teacher_folder_classroom_ids) &  # Students in teacher's classrooms
            (Q(activity__folder__teacher=request.user) | Q(activity__isnull=True))  # Teacher's activities or sketches
        ).select_related('student', 'activity', 'activity__folder')

        # Sort by post_requested_at (when student requested to post) - newest first
        # Fall back to submitted_at if post_requested_at is null
        submissions = submissions.annotate(
            has_date=Case(
                When(post_requested_at__isnull=False, then=Value(0)),
                When(submitted_at__isnull=False, then=Value(1)),
                default=Value(2),
                output_field=IntegerField()
            )
        ).order_by('has_date', '-post_requested_at', '-submitted_at')

        print(f"\n{'='*60}")
        print(f"📝 PENDING APPROVALS CHECK for teacher: {request.user.username}")
        print(f"📚 School Year: {current_sy.name if current_sy else 'None'}")
        print(f"📚 Classrooms: {teacher_folder_classroom_ids}")
        print(f"{'='*60}")
        print(f"Found {submissions.count()} pending approvals")
        print(f"\n📊 SORTED ORDER (Most Recent Request First):")

        # Debug: Print each submission with full details in sorted order
        for index, sub in enumerate(submissions, 1):
            print(f"\n   {index}. 📋 Submission #{sub.id}:")
            print(f"      Student: {sub.student.username} (Classroom: {sub.student.classroom.name if sub.student.classroom else 'None'})")
            print(f"      Activity: {sub.activity.title if sub.activity else 'Sketch Pad'}")
            print(f"      Caption: {sub.caption[:50] if sub.caption else 'No caption'}...")
            print(f"      Status: {sub.status}")
            print(f"      Approval Status: {sub.approval_status}")
            print(f"      Post to Feed: {sub.post_to_feed}")
            print(f"      File Type: {sub.file_type}")
            print(f"      ⏰ Post Requested At: {sub.post_requested_at if sub.post_requested_at else 'NO DATE'}")
            print(f"      📅 Submitted At: {sub.submitted_at if sub.submitted_at else 'NO DATE'}")

        print(f"\n{'='*60}\n")

        # Serializer will handle timezone conversion automatically
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
            activity_title = submission.activity.title if submission.activity else 'Sketch Pad'
            create_notification(
                recipient=submission.student,
                notification_type='submission_approved',
                title='Post Approved',
                message=f'Your post request for "{activity_title}" has been approved and is now visible in the newsfeed',
                submission=submission,
                activity=submission.activity
            )

            # Create a newsfeed post (now that it's approved)
            if True:  # Always create post when approved
                # Check if newsfeed post already exists for this submission
                existing_post = NewsfeedPost.objects.filter(original_submission=submission).first()

                if not existing_post:
                    from .models import NewsfeedPostFile, SubmissionFile
                    import json
                    
                    # Get selected file IDs (only these files should be posted)
                    selected_file_ids = []
                    if submission.post_file_ids:
                        try:
                            selected_file_ids = json.loads(submission.post_file_ids) if isinstance(submission.post_file_ids, str) else submission.post_file_ids
                        except (json.JSONDecodeError, TypeError):
                            selected_file_ids = []
                    
                    # Get the caption from post_caption or fallback to submission caption
                    post_caption = submission.post_caption or submission.caption or ''
                    
                    # Get files to post
                    files_to_post = []
                    if selected_file_ids:
                        # Get only the selected files
                        files_to_post = list(SubmissionFile.objects.filter(id__in=selected_file_ids, submission=submission))
                        print(f"📁 Using {len(files_to_post)} selected files for newsfeed post")
                    elif submission.files.exists():
                        # Fallback to all files if no selection
                        files_to_post = list(submission.files.all())
                        print(f"📁 Using all {len(files_to_post)} files for newsfeed post")
                    
                    # Get primary file for legacy single-file support
                    primary_file_data = None
                    primary_file_type = submission.file_type or 'image'
                    
                    if files_to_post:
                        first_file = files_to_post[0]
                        if first_file.file:
                            primary_file_data = first_file.file.url if hasattr(first_file.file, 'url') else str(first_file.file)
                        elif first_file.file_path:
                            primary_file_data = first_file.file_path
                        primary_file_type = first_file.file_type or 'image'
                    elif submission.file:
                        primary_file_data = submission.file.url if hasattr(submission.file, 'url') else str(submission.file)
                    elif submission.file_path:
                        primary_file_data = submission.file_path

                    print(f"📁 Creating newsfeed post with primary file: {primary_file_data}")

                    # Create new newsfeed post
                    newsfeed_post = NewsfeedPost.objects.create(
                        student=submission.student,
                        student_name=submission.student.username,
                        caption=post_caption,
                        file_path=primary_file_data,
                        file_type=primary_file_type,
                        activity_title=submission.activity.title if submission.activity else 'Sketch Pad',
                        activity_type=submission.activity.activity_type if submission.activity else 'Sketch',
                        classroom=submission.student.classroom,
                        original_submission=submission
                    )
                    
                    # Create NewsfeedPostFile entries for each selected file
                    for index, sub_file in enumerate(files_to_post):
                        file_url = None
                        if sub_file.file:
                            file_url = sub_file.file.url if hasattr(sub_file.file, 'url') else str(sub_file.file)
                        elif sub_file.file_path:
                            file_url = sub_file.file_path
                        
                        NewsfeedPostFile.objects.create(
                            post=newsfeed_post,
                            file_path=file_url,
                            file_type=sub_file.file_type or 'image',
                            file_name=sub_file.file_name,
                            order=index
                        )
                        print(f"   📎 Added file {index + 1}: {sub_file.file_name}")
                    
                    print(f"✅ Created newsfeed post {newsfeed_post.id} with {len(files_to_post)} files")
        elif action == 'cancel':
            # Cancel/remove the post request - reset to approved without posting
            submission.approval_status = 'approved'
            submission.post_to_feed = False  # Don't post to feed
            submission.save()

            print(f"🚫 Cancelled post request for submission {submission_id}")

            # Notify student that request was cancelled
            activity_title = submission.activity.title if submission.activity else 'Sketch Pad'
            create_notification(
                recipient=submission.student,
                notification_type='submission_rejected',
                title='Post Request Cancelled',
                message=f'Your post request for "{activity_title}" has been cancelled by your teacher',
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
    GET: Get newsfeed posts filtered by user's classroom(s)
    Supports school_year query parameter for viewing archived school years
    """
    try:
        posts = NewsfeedPost.objects.none()
        
        # Check for school year filter (for archived view mode)
        school_year_filter = request.query_params.get('school_year', None)
        
        if request.user.is_authenticated:
            if request.user.role == 'admin':
                # Admin sees all posts
                if school_year_filter:
                    posts = NewsfeedPost.objects.filter(classroom__school_year=school_year_filter).order_by('-posted_at')
                    print(f"👑 Admin viewing newsfeed for school year: {school_year_filter}")
                else:
                    posts = NewsfeedPost.objects.all().order_by('-posted_at')
                    print(f"👑 Admin viewing all newsfeed posts")
            elif request.user.role == 'teacher':
                # Teacher sees posts from classrooms where they have folders
                from .models import SchoolYear
                
                if school_year_filter:
                    # Viewing archived school year - get posts from that year
                    teacher_classroom_ids = list(PortfolioFolder.objects.filter(
                        teacher=request.user,
                        classroom__school_year=school_year_filter
                    ).values_list('classroom_id', flat=True).distinct())
                    print(f"📚 Teacher {request.user.username} viewing archived school year: {school_year_filter}, classrooms: {teacher_classroom_ids}")
                else:
                    # Current school year
                    current_sy = SchoolYear.get_current_for_teacher(request.user)
                    
                    # Get classroom IDs where teacher has folders in current school year
                    teacher_classroom_ids = []
                    if current_sy:
                        teacher_classroom_ids = list(PortfolioFolder.objects.filter(
                            teacher=request.user,
                            classroom__school_year=current_sy.name,
                            classroom__is_archived=False
                        ).values_list('classroom_id', flat=True).distinct())
                        print(f"📚 Teacher {request.user.username} has folders in classrooms: {teacher_classroom_ids} (School Year: {current_sy.name})")
                    
                    # Also include teacher's directly assigned classroom if it's in current school year
                    if request.user.classroom and current_sy:
                        if request.user.classroom.school_year == current_sy.name and not request.user.classroom.is_archived:
                            if request.user.classroom.id not in teacher_classroom_ids:
                                teacher_classroom_ids.append(request.user.classroom.id)
                
                if teacher_classroom_ids:
                    posts = NewsfeedPost.objects.filter(classroom_id__in=teacher_classroom_ids).order_by('-posted_at')
                    print(f"📊 Teacher viewing newsfeed from {len(teacher_classroom_ids)} classrooms, found {posts.count()} posts")
                else:
                    print(f"⚠️ Teacher {request.user.username} has no classrooms for the requested school year")
            elif request.user.role == 'student':
                # Check for classroom_id parameter (for archived view mode)
                classroom_id = request.query_params.get('classroom_id', None)
                
                if classroom_id:
                    # Archived view mode - verify student has access to this classroom
                    from .models import StudentPromotionHistory, StudentClassroomHistory
                    try:
                        archived_classroom = Classroom.objects.get(id=classroom_id)
                        
                        # Check if student was in this classroom (via promotion or self-archiving)
                        was_promoted_from = StudentPromotionHistory.objects.filter(
                            student=request.user,
                            previous_classroom=archived_classroom
                        ).exists()
                        
                        was_student_archived = StudentClassroomHistory.objects.filter(
                            student=request.user,
                            classroom=archived_classroom
                        ).exists()
                        
                        is_current_student = request.user.classroom == archived_classroom
                        
                        if is_current_student or was_promoted_from or was_student_archived:
                            posts = NewsfeedPost.objects.filter(classroom=archived_classroom).order_by('-posted_at')
                            print(f"📊 Student viewing archived newsfeed for classroom: {archived_classroom.name}, found {posts.count()} posts")
                        else:
                            print(f"⚠️ Student {request.user.username} does not have access to classroom {classroom_id}")
                    except Classroom.DoesNotExist:
                        print(f"⚠️ Classroom {classroom_id} not found")
                elif request.user.classroom:
                    # Normal mode - student sees posts from their assigned classroom
                    posts = NewsfeedPost.objects.filter(classroom=request.user.classroom).order_by('-posted_at')
                    print(f"📊 Student viewing newsfeed for classroom: {request.user.classroom.name}")
                else:
                    print(f"⚠️ Student {request.user.username} has no classroom assigned")
            else:
                print(f"⚠️ Unknown role: {request.user.role}")

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

            # Build full URL for file_path if it's a media file
            file_url = post.file_path
            if post.file_path and not post.file_path.startswith(('http://', 'https://', 'data:')):
                # If it's a relative path, build full URL
                if post.file_path.startswith('/media/'):
                    file_url = request.build_absolute_uri(post.file_path)
                elif not post.file_path.startswith('/'):
                    file_url = request.build_absolute_uri(f'/media/{post.file_path}')

            # Get all files for this post
            post_files = []
            try:
                for pf in post.files.all():
                    pf_url = pf.file_path
                    if pf.file_path and not pf.file_path.startswith(('http://', 'https://', 'data:')):
                        if pf.file_path.startswith('/media/'):
                            pf_url = request.build_absolute_uri(pf.file_path)
                        elif not pf.file_path.startswith('/'):
                            pf_url = request.build_absolute_uri(f'/media/{pf.file_path}')
                    post_files.append({
                        'id': pf.id,
                        'file_path': pf_url,
                        'file_type': pf.file_type,
                        'file_name': pf.file_name,
                        'order': pf.order
                    })
            except Exception as e:
                print(f"⚠️ Error loading files for post {post.id}: {e}")
            
            # If no files in the new table, use the legacy single file
            if not post_files and file_url:
                post_files = [{
                    'id': 0,
                    'file_path': file_url,
                    'file_type': post.file_type,
                    'file_name': None,
                    'order': 0
                }]

            # Build profile picture URL
            profile_picture_url = None
            if post.student and post.student.profile_picture:
                profile_picture_url = request.build_absolute_uri(post.student.profile_picture.url)

            post_dict = {
                'id': post.id,
                'student_name': post.student_name,
                'profile_picture': profile_picture_url,
                'caption': post.caption,
                'file_path': file_url,
                'file_type': post.file_type,
                'files': post_files,
                'activity_title': post.activity_title,
                'activity_type': post.activity_type,
                'posted_at': post.posted_at.isoformat(),
                'likes': likes_count,
                'is_liked': is_liked,
            }
            print(f"📸 Post {post.id}: {len(post_files)} files")
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
    # Debug logging
    print(f"🔍 Like API called for post {post_id}")
    print(f"🔍 User: {request.user}")
    print(f"🔍 Is authenticated: {request.user.is_authenticated}")
    print(f"🔍 Session key: {request.session.session_key}")
    print(f"🔍 Session data: {dict(request.session)}")

    if not request.user.is_authenticated:
        print(f"❌ Like API - User not authenticated")
        print(f"❌ Session exists: {bool(request.session.session_key)}")
        print(f"❌ User object: {request.user}")
        return Response({
            'error': 'Authentication required',
            'message': 'Please log in to like posts',
            'debug': {
                'has_session': bool(request.session.session_key),
                'user': str(request.user)
            }
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
    # Debug logging for POST requests
    if request.method == 'POST':
        print(f"🔍 Comment API called for post {post_id}")
        print(f"🔍 User: {request.user}")
        print(f"🔍 Is authenticated: {request.user.is_authenticated}")
        print(f"🔍 Session key: {request.session.session_key}")
        print(f"🔍 Session data: {dict(request.session)}")

    # Allow GET for everyone, but require auth for POST
    if request.method == 'POST' and not request.user.is_authenticated:
        print(f"❌ Comment API - User not authenticated")
        print(f"❌ Session exists: {bool(request.session.session_key)}")
        print(f"❌ User object: {request.user}")
        return Response({
            'error': 'Authentication required',
            'message': 'Please log in to comment on posts',
            'debug': {
                'has_session': bool(request.session.session_key),
                'user': str(request.user)
            }
        }, status=status.HTTP_403_FORBIDDEN)

    try:
        from .models import NewsfeedPost, PostComment, PostCommentLike

        post = NewsfeedPost.objects.get(id=post_id)

        if request.method == 'GET':
            # Get all comments for this post
            comments = PostComment.objects.filter(post=post).order_by('created_at')
            print(f"📝 Found {comments.count()} comments for post {post_id}")
            comments_data = []

            for comment in comments:
                # Get replies for this comment
                replies = comment.replies.all().order_by('created_at')
                replies_data = [{
                    'id': reply.id,
                    'user': reply.user.username,
                    'text': reply.text,
                    'created_at': reply.created_at.isoformat(),
                    'timestamp': get_time_ago(reply.created_at)
                } for reply in replies]

                # Get likes count for this comment
                likes_count = comment.likes.count()
                is_liked = PostCommentLike.objects.filter(comment=comment, user=request.user).exists() if request.user.is_authenticated else False

                comment_data = {
                    'id': comment.id,
                    'user': comment.user.username,
                    'text': comment.text,
                    'created_at': comment.created_at.isoformat(),
                    'timestamp': get_time_ago(comment.created_at),
                    'likes': likes_count,
                    'is_liked': is_liked,
                    'replies': replies_data
                }
                comments_data.append(comment_data)
                print(f"   📝 Comment {comment.id}: {comment.text[:30]}...")

            print(f"📝 Returning {len(comments_data)} comments for post {post_id}")
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


@csrf_exempt
@api_view(['POST'])
def comment_like_api(request, post_id, comment_id):
    """
    POST: Toggle like on a comment
    Body: { "liked": true/false }
    """
    print(f"\n❤️ Comment Like API called for post {post_id}, comment {comment_id}")
    print(f"User: {request.user}, Authenticated: {request.user.is_authenticated}")

    if not request.user.is_authenticated:
        print(f"❌ User not authenticated")
        return Response({
            'error': 'Authentication required',
            'message': 'Please log in to like comments'
        }, status=status.HTTP_403_FORBIDDEN)

    try:
        from .models import NewsfeedPost, PostComment, PostCommentLike

        post = NewsfeedPost.objects.get(id=post_id)
        comment = PostComment.objects.get(id=comment_id, post=post)
        liked = request.data.get('liked', True)

        print(f"✅ Found post {post_id} and comment {comment_id}")
        print(f"Liked: {liked}")

        if liked:
            # Add like (use get_or_create to avoid duplicates)
            like, created = PostCommentLike.objects.get_or_create(
                comment=comment,
                user=request.user
            )
            print(f"✅ Like created: {created}")
        else:
            # Remove like
            deleted_count, _ = PostCommentLike.objects.filter(
                comment=comment,
                user=request.user
            ).delete()
            print(f"✅ Like deleted: {deleted_count}")

        # Get updated like count
        likes_count = comment.likes.count()
        is_liked = PostCommentLike.objects.filter(comment=comment, user=request.user).exists()

        print(f"✅ Updated likes_count: {likes_count}, is_liked: {is_liked}")

        return Response({
            'success': True,
            'likes_count': likes_count,
            'is_liked': is_liked
        }, status=status.HTTP_200_OK)

    except PostComment.DoesNotExist:
        print(f"❌ Comment {comment_id} not found")
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
    except NewsfeedPost.DoesNotExist:
        print(f"❌ Post {post_id} not found")
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"❌ Error toggling comment like: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def comment_reply_api(request, post_id, comment_id):
    """
    POST: Add a reply to a comment
    Body: { "text": "reply text" }
    """
    print(f"\n💬 Comment Reply API called for post {post_id}, comment {comment_id}")
    print(f"User: {request.user}, Authenticated: {request.user.is_authenticated}")
    print(f"Request data: {request.data}")

    if not request.user.is_authenticated:
        print(f"❌ User not authenticated")
        return Response({
            'error': 'Authentication required',
            'message': 'Please log in to reply to comments'
        }, status=status.HTTP_403_FORBIDDEN)

    try:
        from .models import NewsfeedPost, PostComment, PostCommentReply

        post = NewsfeedPost.objects.get(id=post_id)
        comment = PostComment.objects.get(id=comment_id, post=post)

        text = request.data.get('text', '').strip()
        print(f"Reply text: {text}")

        if not text:
            print(f"❌ Reply text is empty")
            return Response({'error': 'Reply text is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Create reply as a nested comment
        reply = PostCommentReply.objects.create(
            comment=comment,
            user=request.user,
            text=text
        )

        print(f"✅ Reply created with ID: {reply.id}")

        return Response({
            'success': True,
            'message': 'Reply added',
            'reply': {
                'id': reply.id,
                'user': reply.user.username,
                'text': reply.text,
                'created_at': reply.created_at.isoformat(),
                'timestamp': get_time_ago(reply.created_at)
            }
        }, status=status.HTTP_201_CREATED)

    except PostComment.DoesNotExist:
        print(f"❌ Comment {comment_id} not found")
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
    except NewsfeedPost.DoesNotExist:
        print(f"❌ Post {post_id} not found")
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"❌ Error adding reply: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['DELETE'])
def delete_post_api(request, post_id):
    """
    DELETE: Delete a newsfeed post (teacher only)

    This endpoint allows teachers to remove inappropriate or unwanted posts from the newsfeed.
    When a post is deleted, all associated likes and comments are automatically removed (CASCADE).

    Args:
        request: Django request object
        post_id: ID of the newsfeed post to delete

    Returns:
        200: Post deleted successfully
        403: User is not authenticated or not a teacher
        404: Post not found
        500: Server error
    """
    # Authentication and authorization check
    if not request.user.is_authenticated:
        return Response({
            'error': 'Authentication required'
        }, status=status.HTTP_401_UNAUTHORIZED)

    if request.user.role != 'teacher':
        return Response({
            'error': 'Only teachers can delete posts'
        }, status=status.HTTP_403_FORBIDDEN)

    try:
        # Get the post
        post = NewsfeedPost.objects.get(id=post_id)

        # Store post info for logging before deletion
        student_name = post.student_name
        post_caption = post.caption[:50] if post.caption else 'No caption'

        # Delete the post (CASCADE will delete related likes and comments)
        post.delete()

        # Log the deletion
        print(f"✅ Post deleted successfully:")
        print(f"   - Post ID: {post_id}")
        print(f"   - Student: {student_name}")
        print(f"   - Caption: {post_caption}...")
        print(f"   - Deleted by: {request.user.username} (Teacher)")

        return Response({
            'success': True,
            'message': 'Post deleted successfully',
            'deleted_post_id': post_id
        }, status=status.HTTP_200_OK)

    except NewsfeedPost.DoesNotExist:
        print(f"❌ Post deletion failed: Post {post_id} not found")
        return Response({
            'error': 'Post not found'
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        print(f"❌ Error deleting post {post_id}: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({
            'error': 'An error occurred while deleting the post',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            # Return the current submission
            serializer = StudentSubmissionSerializer(submission, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'PUT':
            # Update submission
            data = request.data

            # Handle file upload (for replacing file)
            file_obj = request.FILES.get('file')
            if file_obj:
                submission.file = file_obj
                # Auto-detect file type
                content_type = file_obj.content_type
                if content_type.startswith('image/'):
                    submission.file_type = 'image'
                elif content_type == 'application/pdf':
                    submission.file_type = 'pdf'
                elif content_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                    submission.file_type = 'document'
                else:
                    submission.file_type = 'file'
                print(f"📎 File replaced: {file_obj.name} (type: {submission.file_type})")

            if 'caption' in data:
                submission.caption = data['caption']
            if 'post_to_feed' in data:
                post_to_feed_raw = data['post_to_feed']
                if isinstance(post_to_feed_raw, str):
                    submission.post_to_feed = post_to_feed_raw.lower() in ('true', '1', 'yes')
                else:
                    submission.post_to_feed = bool(post_to_feed_raw)

                # If requesting to post to feed, set approval status to pending
                if submission.post_to_feed:
                    from django.utils import timezone
                    
                    submission.approval_status = 'pending'
                    submission.post_requested_at = timezone.now()  # Set the request timestamp
                    print(f"📢 Submission {submission.id} requesting post to feed - approval_status set to pending")
                    print(f"⏰ Post requested at: {submission.post_requested_at}")

                    # Save selected file IDs for posting (only these files will be shown to teacher)
                    if 'post_file_ids' in data:
                        import json
                        post_file_ids = data['post_file_ids']
                        if isinstance(post_file_ids, list):
                            submission.post_file_ids = json.dumps(post_file_ids)
                        else:
                            submission.post_file_ids = post_file_ids
                        print(f"📁 Selected files for posting: {submission.post_file_ids}")

                    # Save post caption
                    if 'post_caption' in data:
                        submission.post_caption = data['post_caption']
                        print(f"📝 Post caption: {submission.post_caption}")

                    # Notify teacher about the post request
                    if submission.activity:
                        teacher = submission.activity.folder.teacher
                        create_notification(
                            recipient=teacher,
                            notification_type='approval_requested',
                            title='Post Approval Requested',
                            message=f'{request.user.username} requested to post "{submission.activity.title}" to the class feed',
                            submission=submission,
                            activity=submission.activity
                        )

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

                    # Increment resubmit count immediately when entering resubmission mode
                    submission.resubmit_count += 1
                    submission.last_resubmit_at = timezone.now()
                    print(f"🔄 Converting to draft for resubmission #{submission.resubmit_count}")

                submission.status = new_status

                # If changing from draft to final submission, ALWAYS update submitted_at to current time
                if old_status == 'draft' and new_status in ['unscored', 'scored']:
                    from django.utils import timezone
                    from datetime import datetime, time as dt_time

                    # Check if this is a resubmission or first submission
                    # Resubmit count is already incremented when entering resubmission mode (line 2661)
                    # So we just need to validate and log here

                    if submission.last_resubmit_at is not None:
                        # This is a resubmission - count was already incremented when entering resubmission mode
                        print(f"✅ Resubmission #{submission.resubmit_count} being turned in")
                    else:
                        # This is the FIRST submission - keep resubmit_count at 0
                        print(f"✅ First submission being turned in (resubmit_count: {submission.resubmit_count})")
                        # Ensure it's 0 (defensive programming)
                        if submission.resubmit_count != 0:
                            print(f"⚠️ WARNING: resubmit_count was {submission.resubmit_count}, resetting to 0 for first submission")
                            submission.resubmit_count = 0

                    # ALWAYS update submitted_at to current time (when student turned in)
                    import pytz
                    manila_tz = pytz.timezone('Asia/Manila')
                    now = timezone.now().astimezone(manila_tz)
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
                    import pytz

                    # Update submitted_at to current time in Manila timezone
                    manila_tz = pytz.timezone('Asia/Manila')
                    now = timezone.now().astimezone(manila_tz)
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
def upload_submission_files_api(request, activity_id):
    """
    POST: Upload multiple files for a submission (student only)
    Creates or updates a draft submission with multiple files
    """
    if not request.user.is_authenticated or request.user.role != 'student':
        return Response({'error': 'Only students can upload files'}, status=status.HTTP_403_FORBIDDEN)

    try:
        activity = PortfolioActivity.objects.get(id=activity_id)
        files = request.FILES.getlist('files')

        if not files:
            return Response({'error': 'No files provided'}, status=status.HTTP_400_BAD_REQUEST)

        print(f"📤 Uploading {len(files)} file(s) for activity {activity_id}")

        # Get or create draft submission
        existing_submission = StudentSubmission.objects.filter(
            activity=activity,
            student=request.user,
            is_active=True
        ).order_by('-submitted_at').first()

        if existing_submission and existing_submission.status == 'draft':
            submission = existing_submission
            print(f"📝 Using existing draft submission {submission.id}")
        elif existing_submission and existing_submission.status in ['unscored', 'scored']:
            # Check if can resubmit
            if existing_submission.score is not None:
                return Response({'error': 'Cannot modify scored submission'}, status=status.HTTP_400_BAD_REQUEST)
            submission = existing_submission
            print(f"📝 Using existing submission {submission.id} for file update")
        else:
            # Create new draft submission
            submission = StudentSubmission.objects.create(
                activity=activity,
                student=request.user,
                status='draft',
                is_active=True
            )
            print(f"📝 Created new draft submission {submission.id}")

        # Process each file
        uploaded_files = []
        for index, file_obj in enumerate(files):
            # Detect file type
            content_type = file_obj.content_type
            if content_type.startswith('image/'):
                file_type = 'image'
            elif content_type == 'application/pdf':
                file_type = 'pdf'
            elif content_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                file_type = 'document'
            else:
                file_type = 'file'

            # Create SubmissionFile record
            submission_file = SubmissionFile.objects.create(
                submission=submission,
                file=file_obj,
                file_type=file_type,
                file_name=file_obj.name,
                file_size=file_obj.size,
                order=index
            )
            uploaded_files.append(submission_file)
            print(f"📎 File {index + 1}: {file_obj.name} ({file_type})")

        # Also update the main submission file field with the first file for backward compatibility
        if files and not submission.file:
            first_file = files[0]
            submission.file = first_file
            content_type = first_file.content_type
            if content_type.startswith('image/'):
                submission.file_type = 'image'
            elif content_type == 'application/pdf':
                submission.file_type = 'pdf'
            elif content_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                submission.file_type = 'document'
            else:
                submission.file_type = 'file'
            submission.save()

        serializer = StudentSubmissionSerializer(submission, context={'request': request})
        return Response({
            'submission': serializer.data,
            'uploaded_count': len(uploaded_files),
            'message': f'Successfully uploaded {len(uploaded_files)} file(s)'
        }, status=status.HTTP_201_CREATED)

    except PortfolioActivity.DoesNotExist:
        return Response({'error': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        import traceback
        print(f"❌ Error uploading files: {str(e)}")
        print(traceback.format_exc())
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET', 'POST'])
def submission_files_api(request, submission_id):
    """
    GET: List all files for a submission
    POST: Add new file(s) to a submission
    """
    try:
        submission = StudentSubmission.objects.get(id=submission_id)

        # Check permissions
        if request.user.role == 'student' and submission.student != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        if request.method == 'GET':
            files = submission.files.all()
            serializer = SubmissionFileSerializer(files, many=True, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'POST':
            if request.user.role != 'student' or submission.student != request.user:
                return Response({'error': 'Only the submission owner can add files'}, status=status.HTTP_403_FORBIDDEN)

            files = request.FILES.getlist('files')
            if not files:
                return Response({'error': 'No files provided'}, status=status.HTTP_400_BAD_REQUEST)

            # Get current max order
            max_order = submission.files.count()

            uploaded_files = []
            for index, file_obj in enumerate(files):
                content_type = file_obj.content_type
                if content_type.startswith('image/'):
                    file_type = 'image'
                elif content_type == 'application/pdf':
                    file_type = 'pdf'
                elif content_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                    file_type = 'document'
                else:
                    file_type = 'file'

                submission_file = SubmissionFile.objects.create(
                    submission=submission,
                    file=file_obj,
                    file_type=file_type,
                    file_name=file_obj.name,
                    file_size=file_obj.size,
                    order=max_order + index
                )
                uploaded_files.append(submission_file)

            serializer = SubmissionFileSerializer(uploaded_files, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    except StudentSubmission.DoesNotExist:
        return Response({'error': 'Submission not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        import traceback
        print(f"❌ Error in submission_files_api: {str(e)}")
        print(traceback.format_exc())
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET', 'DELETE'])
def submission_file_detail_api(request, submission_id, file_id):
    """
    GET: Get a specific file details
    DELETE: Remove a file from submission
    """
    try:
        submission = StudentSubmission.objects.get(id=submission_id)
        submission_file = SubmissionFile.objects.get(id=file_id, submission=submission)

        # Check permissions
        if request.user.role == 'student' and submission.student != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        if request.method == 'GET':
            serializer = SubmissionFileSerializer(submission_file, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'DELETE':
            if request.user.role != 'student' or submission.student != request.user:
                return Response({'error': 'Only the submission owner can delete files'}, status=status.HTTP_403_FORBIDDEN)

            # Delete the file
            file_name = submission_file.file_name
            submission_file.delete()

            # Reorder remaining files
            remaining_files = submission.files.all().order_by('order')
            for index, f in enumerate(remaining_files):
                if f.order != index:
                    f.order = index
                    f.save()

            return Response({'message': f'File "{file_name}" deleted successfully'}, status=status.HTTP_200_OK)

    except StudentSubmission.DoesNotExist:
        return Response({'error': 'Submission not found'}, status=status.HTTP_404_NOT_FOUND)
    except SubmissionFile.DoesNotExist:
        return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        import traceback
        print(f"❌ Error in submission_file_detail_api: {str(e)}")
        print(traceback.format_exc())
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
        # Also update submitted_at to reflect when approval was requested
        from django.utils import timezone
        import pytz

        # Get current time in Asia/Manila timezone
        manila_tz = pytz.timezone('Asia/Manila')
        current_time = timezone.now().astimezone(manila_tz)

        submission.caption = caption
        submission.approval_status = 'pending'
        submission.submitted_at = current_time  # Update timestamp to current Manila time
        submission.save()

        print(f"📝 Updated submission {submission_id}:")
        print(f"   Caption: {caption}")
        print(f"   Approval status: {submission.approval_status}")
        print(f"   Submitted at: {submission.submitted_at}")
        print(f"   Timezone info: {submission.submitted_at.tzinfo}")
        print(f"   Current Manila time: {current_time}")

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
            print(f"📬 Fetching notifications for user: {request.user.username} (ID: {request.user.id}, role: {request.user.role})")
            notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
            print(f"📊 Found {notifications.count()} notifications for user {request.user.username}")

            # Debug: Print ALL notifications with recipient info
            for notif in notifications:
                print(f"  - [{notif.notification_type}] {notif.title} (recipient: {notif.recipient.username}, ID: {notif.recipient.id})")

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
@api_view(['POST', 'PUT'])
def score_submission_api(request, submission_id):
    """
    POST: Score a student submission with multiple criteria (new score)
    PUT: Update an existing score (edit score)
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
        
        # Check if this is an edit (PUT) or new score (POST)
        is_edit = request.method == 'PUT' or (submission.status == 'scored' and submission.score is not None)

        # Get scoring data from request
        score = request.data.get('score', 0)
        feedback = request.data.get('feedback', '')
        criteria_scores = request.data.get('criteria_scores', '[]')

        print(f"{'Editing' if is_edit else 'Scoring'} submission {submission_id}:")
        print(f"  Score: {score}")
        print(f"  Feedback: {feedback}")
        print(f"  Criteria scores: {criteria_scores}")

        # Store old score for comparison (for edit notification)
        old_score = submission.score if is_edit else None

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
        print(f"✅ Submission {submission_id} {'edited' if is_edit else 'scored'}")
        print(f"📝 After update - Status: {submission.status}, Score: {submission.score}, Scored at: {submission.scored_at}")

        # Check if there are any remarks and feedback for this submission
        has_remarks = Remark.objects.filter(submission=submission).exists()
        has_feedback = feedback and feedback.strip()

        # Send notification to student
        activity_title = submission.activity.title if submission.activity else 'your submission'

        # Create specific notification message based on whether it's an edit or new score
        if is_edit:
            notification_title = 'Score Updated'
            notification_type = 'score_updated'
            if old_score is not None:
                notification_message = f'Your score for "{activity_title}" has been updated from {old_score} to {score}. Check your outputs to view the updated score.'
            else:
                notification_message = f'Your score for "{activity_title}" has been updated to {score}. Check your outputs to view the updated score.'
        else:
            notification_title = 'Submission Scored'
            notification_type = 'score_added'
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
            notification_type=notification_type,
            title=notification_title,
            message=notification_message,
            submission=submission,
            activity=submission.activity
        )

        serializer = StudentSubmissionSerializer(submission)
        return Response({
            'message': f'Submission {"updated" if is_edit else "scored"} successfully',
            'submission': serializer.data,
            'is_edit': is_edit
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
    print(f"\n{'='*60}")
    print(f"🎨 SKETCH SUBMISSION REQUEST")
    print(f"{'='*60}")
    print(f"User authenticated: {request.user.is_authenticated}")
    print(f"User: {request.user.username if request.user.is_authenticated else 'Anonymous'}")
    print(f"User role: {request.user.role if request.user.is_authenticated else 'N/A'}")

    if not request.user.is_authenticated:
        print(f"❌ Authentication failed!")
        return Response({'error': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)

    if request.user.role != 'student':
        print(f"❌ User is not a student!")
        return Response({'error': 'Only students can submit sketches'}, status=status.HTTP_403_FORBIDDEN)

    try:
        data = request.data
        print(f"📝 Data received: caption={data.get('caption', '')[:50]}...")
        print(f"📝 File path length: {len(data.get('file_path', ''))}")
        print(f"📝 File type: {data.get('file_type', 'N/A')}")

        # Create a sketch submission (activity_id can be null or use a special "Sketch" activity)
        # For now, we'll create it without an activity or you can create a default "Sketch Pad" activity
        from django.utils import timezone
        import pytz

        # Get current time in Asia/Manila timezone
        manila_tz = pytz.timezone('Asia/Manila')
        current_time = timezone.now().astimezone(manila_tz)

        submission = StudentSubmission.objects.create(
            activity_id=None,  # No specific activity for sketches
            student=request.user,
            caption=data.get('caption', ''),
            file_path=data.get('file_path', ''),
            file_type='image',
            status='unscored',
            post_to_feed=True,
            approval_status='pending',
            submitted_at=current_time  # Set submission timestamp in Manila timezone
        )

        print(f"✅ Sketch submission created: ID={submission.id}")
        print(f"📢 POST TO FEED: True, APPROVAL STATUS: pending")
        print(f"⏰ SUBMITTED AT (Manila): {submission.submitted_at}")
        print(f"⏰ SUBMITTED AT (UTC): {submission.submitted_at.astimezone(pytz.UTC)}")

        # Notify teacher about sketch submission
        # Get the student's classroom teacher
        student_classroom = request.user.classroom
        if student_classroom and student_classroom.teacher:
            teacher = student_classroom.teacher
            print(f"📧 Sending 'approval_requested' notification to teacher: {teacher.username}")
            create_notification(
                recipient=teacher,
                notification_type='approval_requested',
                title='Sketch Approval Requested',
                message=f'{request.user.username} submitted a sketch and requested approval to post to newsfeed',
                submission=submission
            )
        else:
            print(f"⚠️ No teacher found for student's classroom")

        print(f"{'='*60}\n")

        serializer = StudentSubmissionSerializer(submission)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error creating sketch submission: {str(e)}")
        print(f"Stack trace:\n{error_trace}")
        print(f"{'='*60}\n")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'POST'])
def sketches_api(request):
    """
    GET: List all sketches for the authenticated student
    POST: Save a new sketch
    """
    if not request.user.is_authenticated:
        print(f"❌ Sketches API: User not authenticated")
        return Response({'error': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)

    if request.user.role != 'student':
        print(f"❌ Sketches API: User is not a student")
        return Response({'error': 'Only students can manage sketches'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        try:
            from .models import Sketch
            from .serializer import SketchSerializer

            # Get all sketches for the current student
            sketches = Sketch.objects.filter(student=request.user).order_by('-created_at')
            print(f"📚 Loaded {sketches.count()} sketches for {request.user.username}")
            serializer = SketchSerializer(sketches, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(f"❌ Error fetching sketches: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'POST':
        try:
            from .models import Sketch
            from .serializer import SketchSerializer

            data = request.data
            print(f"💾 Saving sketch for {request.user.username}")
            print(f"   Title: {data.get('title', 'Untitled Sketch')}")
            print(f"   Image data length: {len(data.get('image_data', ''))}")

            # Create new sketch
            sketch = Sketch.objects.create(
                student=request.user,
                title=data.get('title', 'Untitled Sketch'),
                image_data=data.get('image_data', '')
            )

            print(f"✅ Sketch saved: ID={sketch.id}")
            serializer = SketchSerializer(sketch)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"❌ Error saving sketch: {str(e)}")
            print(f"Stack trace:\n{error_trace}")
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
def class_record_api(request):
    """Get class record data - all activities grouped by subject with student submissions"""
    if not request.user.is_authenticated or request.user.role != 'teacher':
        return Response({'error': 'Teacher authentication required'}, status=status.HTTP_403_FORBIDDEN)

    try:
        classroom_id = request.GET.get('classroom_id', None)

        # Get teacher's folders
        teacher_folders = PortfolioFolder.objects.filter(teacher=request.user)

        # Filter by classroom if provided
        if classroom_id:
            try:
                classroom = Classroom.objects.get(id=classroom_id)
                # Only filter by the actual classroom object, not by class_name string
                # This prevents counting activities from old school years with the same class name
                teacher_folders = teacher_folders.filter(classroom=classroom)
                print(f"📚 Class record: Filtering folders for classroom ID: {classroom.id}, SY: {classroom.school_year}")
            except Classroom.DoesNotExist:
                pass

        # Get all published activities grouped by folder (subject)
        activities = PortfolioActivity.objects.filter(
            folder__in=teacher_folders,
            is_published=True
        ).select_related('folder').order_by('folder__name', 'created_at')

        # Group activities by subject (folder name)
        subjects = {}
        for activity in activities:
            folder_name = activity.folder.name
            if folder_name not in subjects:
                subjects[folder_name] = {
                    'folder_id': activity.folder.id,
                    'activities': []
                }
            subjects[folder_name]['activities'].append({
                'id': activity.id,
                'title': activity.title,
                'activity_type': activity.activity_type,
                'due_date': activity.due_date.strftime('%Y-%m-%d') if activity.due_date else None,
                'due_time': activity.due_time.strftime('%H:%M') if activity.due_time else None,
            })

        # Get all submissions for these activities
        activity_ids = [a.id for a in activities]
        submissions = StudentSubmission.objects.filter(
            activity_id__in=activity_ids
        ).select_related('student', 'activity')

        # Create submission map: "studentId-activityId" -> submission data
        submission_map = {}
        for sub in submissions:
            key = f"{sub.student_id}-{sub.activity_id}"
            
            # Calculate score display
            score_display = 'N/A'
            if sub.status == 'scored':
                if sub.criteria_scores:
                    try:
                        criteria = json.loads(sub.criteria_scores) if isinstance(sub.criteria_scores, str) else sub.criteria_scores
                        sub_score = sum(int(c.get('score', 0)) for c in criteria)
                        sub_max = sum(int(c.get('maxScore', 0)) for c in criteria)
                        score_display = f"{sub_score}/{sub_max}"
                    except:
                        score_display = f"{sub.score}/10" if sub.score else 'N/A'
                elif sub.score:
                    score_display = f"{sub.score}/10"

            submission_map[key] = {
                'id': sub.id,
                'status': sub.status,
                'score': score_display,
                'submitted_at': sub.submitted_at.strftime('%Y-%m-%d %I:%M %p') if sub.submitted_at else None,
                'is_late': sub.is_late if hasattr(sub, 'is_late') else False,
                'is_compiled': sub.compiled if hasattr(sub, 'compiled') else False,
                'resubmit_count': sub.resubmit_count if hasattr(sub, 'resubmit_count') else 0,
            }

        print(f"📊 Class record: {len(subjects)} subjects, {len(activity_ids)} activities, {len(submission_map)} submissions")

        return Response({
            'subjects': subjects,
            'submissions': submission_map,
        }, status=status.HTTP_200_OK)

    except Exception as e:
        print(f"Error fetching class record: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
def student_progress_list_api(request):
    """Get list of students with their progress summary"""
    if not request.user.is_authenticated or request.user.role != 'teacher':
        return Response({'error': 'Teacher authentication required'}, status=status.HTTP_403_FORBIDDEN)

    try:
        from django.db.models import Count, Avg, Q

        # Get classroom_id from query parameter for specific classroom filtering
        classroom_id = request.GET.get('classroom_id', None)
        class_name = request.GET.get('class', None)
        
        print(f"📊 student_progress_list_api called - classroom_id: {classroom_id}, class_name: {class_name}")
        
        students = None
        target_classroom = None
        is_archived_classroom = False
        
        # If specific class is requested, get students from that classroom
        if class_name:
            # IMPORTANT: Prioritize non-archived classrooms from the current school year
            from .models import SchoolYear
            current_sy = SchoolYear.get_current_for_teacher(request.user)
            
            # Try to find classroom in current school year first
            if current_sy:
                target_classroom = Classroom.objects.filter(
                    name=class_name,
                    school_year=current_sy.name,
                    is_archived=False
                ).first()
                print(f"🔍 Looking for classroom '{class_name}' in current school year: {current_sy.name}")
            
            # Fallback: try any non-archived classroom with this name
            if not target_classroom:
                target_classroom = Classroom.objects.filter(
                    name=class_name,
                    is_archived=False
                ).first()
                print(f"🔍 Fallback: Looking for any non-archived classroom '{class_name}'")
            
            # Last resort: any classroom with this name
            if not target_classroom:
                target_classroom = Classroom.objects.filter(name=class_name).first()
                print(f"🔍 Last resort: Any classroom named '{class_name}'")
            
        elif classroom_id:
            target_classroom = Classroom.objects.filter(id=classroom_id).first()
            print(f"🔍 Looking for classroom by ID: {classroom_id}")
        
        # If we found a target classroom, get students
        if target_classroom:
            is_archived_classroom = target_classroom.is_archived
            
            if is_archived_classroom:
                # For archived classrooms, get students from ALL sources (like classroom_detail_api)
                from .models import StudentPromotionHistory, StudentClassroomHistory
                
                # Collect student IDs from ALL sources
                student_ids = set()
                
                # 1. Get students currently assigned to this classroom
                current_students = User.objects.filter(classroom=target_classroom, role='student')
                student_ids.update(current_students.values_list('id', flat=True))
                print(f"📚 Found {current_students.count()} currently assigned students")
                
                # 2. Get students from promotion history (teacher-initiated promotions)
                promotion_records = StudentPromotionHistory.objects.filter(
                    previous_classroom=target_classroom
                ).select_related('student')
                student_ids.update(promotion_records.values_list('student_id', flat=True))
                print(f"📚 Found {promotion_records.count()} students from promotion history")
                
                # 3. Get students from classroom history (student-initiated archiving)
                classroom_history_records = StudentClassroomHistory.objects.filter(
                    classroom=target_classroom
                )
                student_ids.update(classroom_history_records.values_list('student_id', flat=True))
                print(f"📚 Found {classroom_history_records.count()} students from classroom history")
                
                # 4. Get students from submission history (fallback for any missed students)
                submission_student_ids = StudentSubmission.objects.filter(
                    activity__folder__classroom=target_classroom
                ).values_list('student_id', flat=True).distinct()
                student_ids.update(submission_student_ids)
                print(f"📚 Found {len(submission_student_ids)} students from submission history")
                
                # Get all unique students
                if student_ids:
                    students = User.objects.filter(
                        id__in=student_ids,
                        role='student'
                    ).exclude(username='admin').order_by('last_name', 'first_name')
                    print(f"📚 Total unique students for archived classroom {target_classroom.name}: {students.count()}")
                else:
                    students = User.objects.none()
                    print(f"⚠️ No students found for archived classroom {target_classroom.name}")
            else:
                # Non-archived classroom - use current assignment
                students = User.objects.filter(
                    role='student',
                    classroom=target_classroom
                ).exclude(username='admin').select_related('classroom').order_by('last_name', 'first_name')
                print(f"👥 Found {students.count()} students in classroom {target_classroom.name} (ID: {target_classroom.id}, SY: {target_classroom.school_year})")
        elif not class_name and not classroom_id:
            # No specific class - get teacher's assigned classrooms from CURRENT school year only
            from .models import SchoolYear
            current_sy = SchoolYear.get_current_for_teacher(request.user)
            
            if current_sy:
                teacher_classrooms = Classroom.objects.filter(
                    teacher=request.user,
                    school_year=current_sy.name,
                    is_archived=False
                )
                print(f"📚 Getting students from teacher's classrooms in current school year: {current_sy.name}")
            else:
                # Fallback: get non-archived classrooms
                teacher_classrooms = Classroom.objects.filter(
                    teacher=request.user,
                    is_archived=False
                )
                print(f"⚠️ No current school year, using non-archived classrooms")
            
            if teacher_classrooms.exists():
                students = User.objects.filter(
                    role='student',
                    classroom__in=teacher_classrooms
                ).exclude(username='admin').select_related('classroom').order_by('last_name', 'first_name')
                print(f"👥 Found {students.count()} students in teacher's assigned classrooms")
            else:
                print(f"⚠️ Teacher has no assigned classrooms")
                return Response([], status=status.HTTP_200_OK)
        else:
            print(f"⚠️ Classroom not found")
            return Response([], status=status.HTTP_200_OK)
        
        if students is None:
            return Response([], status=status.HTTP_200_OK)

        student_list = []
        for student in students:
            # For archived classrooms, filter submissions to only this classroom's activities
            if is_archived_classroom and target_classroom:
                total_submissions = StudentSubmission.objects.filter(
                    student=student,
                    activity__folder__classroom=target_classroom
                ).count()
                scored_submissions = StudentSubmission.objects.filter(
                    student=student,
                    activity__folder__classroom=target_classroom,
                    status='scored'
                ).count()
                avg_score = StudentSubmission.objects.filter(
                    student=student,
                    activity__folder__classroom=target_classroom,
                    status='scored',
                    score__isnull=False
                ).aggregate(Avg('score'))['score__avg'] or 0
            else:
                # Get submissions count
                total_submissions = StudentSubmission.objects.filter(student=student).count()
                scored_submissions = StudentSubmission.objects.filter(student=student, status='scored').count()
                avg_score = StudentSubmission.objects.filter(
                    student=student,
                    status='scored',
                    score__isnull=False
                ).aggregate(Avg('score'))['score__avg'] or 0

            # Get classroom info - for archived, use the target classroom info
            classroom_name = ''
            grade_level = ''
            section = ''
            teacher_name = ''
            
            if is_archived_classroom and target_classroom:
                classroom_name = target_classroom.name
                if ' - ' in classroom_name:
                    parts = classroom_name.split(' - ')
                    grade_level = parts[0].strip()
                    section = parts[1].strip()
                else:
                    grade_level = classroom_name
                    section = ''
                if target_classroom.teacher:
                    teacher_name = target_classroom.teacher.get_full_name() or target_classroom.teacher.username
            elif student.classroom:
                classroom_name = student.classroom.name
                if ' - ' in classroom_name:
                    parts = classroom_name.split(' - ')
                    grade_level = parts[0].strip()
                    section = parts[1].strip()
                else:
                    grade_level = classroom_name
                    section = ''
                if student.classroom.teacher:
                    teacher_name = student.classroom.teacher.get_full_name() or student.classroom.teacher.username

            # Build full profile picture URL
            profile_picture_url = None
            if student.profile_picture:
                profile_picture_url = request.build_absolute_uri(student.profile_picture.url)

            student_list.append({
                'id': student.id,
                'student_id': student.id_number or f'STD{str(student.id).zfill(3)}',
                'name': student.get_full_name() or student.username,
                'username': student.username,
                'email': student.email,
                'profile_picture': profile_picture_url,
                'total_outputs': total_submissions,
                'scored_outputs': scored_submissions,
                'average_score': round(avg_score, 2) if avg_score else 0,
                'classroom': classroom_name,
                'grade_level': grade_level,
                'section': section,
                'teacher': teacher_name,
                'is_historical': is_archived_classroom,  # Flag for archived data
            })

        return Response(student_list, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error fetching student progress list: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
def student_progress_detail_api(request, student_id):
    """Get detailed progress for a specific student including all activities"""
    if not request.user.is_authenticated or request.user.role != 'teacher':
        return Response({'error': 'Teacher authentication required'}, status=status.HTTP_403_FORBIDDEN)

    try:
        # Get student
        student = User.objects.get(id=student_id, role='student')

        # Check if a specific classroom_id is provided (for archived classrooms)
        classroom_id = request.GET.get('classroom_id', None)
        target_classroom = None
        is_archived_view = False
        
        if classroom_id:
            try:
                target_classroom = Classroom.objects.get(id=classroom_id)
                is_archived_view = target_classroom.is_archived
                print(f"📚 Student progress detail: Using specified classroom {target_classroom.name} (ID: {classroom_id}, archived: {is_archived_view})")
            except Classroom.DoesNotExist:
                print(f"⚠️ Classroom {classroom_id} not found, falling back to student's current classroom")

        # Get teacher's folders
        teacher_folders = PortfolioFolder.objects.filter(teacher=request.user)
        
        # Filter by the target classroom (either specified or student's current)
        if target_classroom:
            # Use the specified classroom (for archived view)
            teacher_folders = teacher_folders.filter(classroom=target_classroom)
            print(f"📚 Filtering folders for specified classroom: {target_classroom.name} (ID: {target_classroom.id}, SY: {target_classroom.school_year})")
        elif student.classroom:
            # Use student's current classroom
            teacher_folders = teacher_folders.filter(classroom=student.classroom)
            print(f"📚 Filtering folders for student's classroom: {student.classroom.name} (ID: {student.classroom.id}, SY: {student.classroom.school_year})")

        # Get ONLY PUBLISHED activities from teacher's folders (students can only see published)
        all_activities = PortfolioActivity.objects.filter(
            folder__in=teacher_folders,
            is_published=True  # Only published activities
        ).select_related('folder').order_by('folder__name', 'created_at')

        print(f"📊 Found {all_activities.count()} published activities for student {student_id}")

        # Get student's submissions
        student_submissions = StudentSubmission.objects.filter(
            student=student,
            activity__in=all_activities
        ).select_related('activity', 'activity__folder')

        # Create a map of activity_id -> submission
        submission_map = {sub.activity_id: sub for sub in student_submissions}

        # Build activities list with submission status
        activities_data = []
        total_activities = 0
        completed = 0
        scored = 0
        missing = 0

        for activity in all_activities:
            total_activities += 1
            submission = submission_map.get(activity.id)

            # Format due date and time
            due_datetime = 'N/A'
            if activity.due_date:
                due_datetime = activity.due_date.strftime('%Y-%m-%d')
                if activity.due_time:
                    due_datetime += f' {activity.due_time.strftime("%I:%M %p")}'

            if submission:
                # Format submitted date and time
                submitted_datetime = 'N/A'
                if submission.submitted_at:
                    submitted_datetime = submission.submitted_at.strftime('%Y-%m-%d %I:%M %p')

                # Determine status based on submission state
                # Status options: Submitted, Submitted Late, Resubmitted, Pending (scored but waiting)
                resubmit_count = submission.resubmit_count or 0
                is_late = submission.is_late or False

                if submission.status == 'scored':
                    if resubmit_count > 0:
                        status_text = 'Resubmitted'
                    elif is_late:
                        status_text = 'Submitted Late'
                    else:
                        status_text = 'Submitted'
                    scored += 1
                    completed += 1
                    # Calculate score
                    if submission.criteria_scores:
                        try:
                            criteria = json.loads(submission.criteria_scores) if isinstance(submission.criteria_scores, str) else submission.criteria_scores
                            sub_score = sum(int(c.get('score', 0)) for c in criteria)
                            sub_max = sum(int(c.get('maxScore', 0)) for c in criteria)
                            score_display = f"{sub_score}/{sub_max}"
                        except:
                            score_display = f"{submission.score}/10" if submission.score else 'N/A'
                    elif submission.score:
                        score_display = f"{submission.score}/10"
                    else:
                        score_display = 'N/A'
                else:
                    # Unscored submission - Pending
                    if resubmit_count > 0:
                        status_text = 'Resubmitted'
                    elif is_late:
                        status_text = 'Submitted Late'
                    else:
                        status_text = 'Pending'
                    completed += 1
                    score_display = 'N/A'

                activities_data.append({
                    'title': activity.title,
                    'folder_name': activity.folder.name,
                    'activity_type': activity.activity_type,
                    'due_datetime': due_datetime,
                    'submitted_datetime': submitted_datetime,
                    'status': status_text,
                    'score': score_display,
                })
            else:
                # Not submitted
                missing += 1
                is_past_due = activity.due_date and timezone.now().date() > activity.due_date
                status_text = 'Missing' if is_past_due else 'Pending'

                activities_data.append({
                    'title': activity.title,
                    'folder_name': activity.folder.name,
                    'activity_type': activity.activity_type,
                    'due_datetime': due_datetime,
                    'submitted_datetime': 'N/A',
                    'status': status_text,
                    'score': 'N/A',
                })

        response_data = {
            'student': {
                'id': student.id,
                'student_id': student.id_number or f'STD{str(student.id).zfill(3)}',
                'name': student.get_full_name() or student.username,
                'username': student.username,
                'email': student.email,
                'grade_level': student.grade_level,
                'section': student.section,
                'classroom': str(student.classroom) if student.classroom else 'N/A',
            },
            'activities': activities_data,
            'summary': {
                'total_activities': total_activities,
                'completed': completed,
                'scored': scored,
                'missing': missing,
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error fetching student progress detail: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Remark API Endpoints
@api_view(['GET', 'POST'])
def remark_list(request):
    """
    GET: List all remarks (filtered by teacher or student)
    POST: Create a new remark (teacher only)
    Supports classroom_id parameter for archived view mode
    """
    if request.method == 'GET':
        # Get query parameters
        student_id = request.query_params.get('student_id')
        teacher_id = request.query_params.get('teacher_id')
        classroom_id = request.query_params.get('classroom_id')  # For archived view mode

        # Filter remarks - exclude submission-linked remarks for both teachers and students
        remarks = Remark.objects.filter(submission__isnull=True)

        if student_id:
            remarks = remarks.filter(student_id=student_id)

        if teacher_id:
            remarks = remarks.filter(teacher_id=teacher_id)

        # For students, only show their own remarks
        if request.user.role == 'student':
            remarks = remarks.filter(student=request.user)
            
            # If classroom_id is provided (archived view mode), filter by teachers from that classroom
            if classroom_id:
                from .models import StudentPromotionHistory, StudentClassroomHistory
                try:
                    archived_classroom = Classroom.objects.get(id=classroom_id)
                    
                    # Verify student has access to this classroom
                    was_promoted_from = StudentPromotionHistory.objects.filter(
                        student=request.user,
                        previous_classroom=archived_classroom
                    ).exists()
                    
                    was_student_archived = StudentClassroomHistory.objects.filter(
                        student=request.user,
                        classroom=archived_classroom
                    ).exists()
                    
                    is_current_student = request.user.classroom == archived_classroom
                    
                    if is_current_student or was_promoted_from or was_student_archived:
                        # Get teachers who have folders in this classroom
                        teacher_ids = PortfolioFolder.objects.filter(
                            classroom=archived_classroom
                        ).values_list('teacher_id', flat=True).distinct()
                        
                        remarks = remarks.filter(teacher_id__in=teacher_ids)
                        print(f"📝 Student viewing archived remarks from {len(teacher_ids)} teachers in classroom {archived_classroom.name}")
                except Classroom.DoesNotExist:
                    print(f"⚠️ Classroom {classroom_id} not found for remarks filter")

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
@api_view(['PUT'])
def convert_draft_to_final_api(request, activity_id, submission_id):
    """Convert a draft submission to a final submission"""
    try:
        submission = StudentSubmission.objects.get(id=submission_id, activity_id=activity_id, student=request.user)

        if submission.status != 'draft':
            return Response({'error': 'Submission is not a draft'}, status=status.HTTP_400_BAD_REQUEST)

        # Convert to final submission
        submission.status = 'unscored'
        submission.save()

        print(f"✅ Converted draft submission {submission_id} to final submission (status='unscored')")

        # Notify teacher
        teacher = submission.activity.folder.teacher
        if teacher:
            create_notification(
                recipient=teacher,
                notification_type='submission_received',
                title='New Submission Received',
                message=f'{request.user.username} submitted work for "{submission.activity.title}"',
                submission=submission,
                activity=submission.activity
            )

        serializer = StudentSubmissionSerializer(submission, context={'request': request})
        return Response(serializer.data)
    except StudentSubmission.DoesNotExist:
        return Response({'error': 'Submission not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error converting draft: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
    Supports classroom_id parameter for archived view mode
    """
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # Get classroom_id for archived view mode
        classroom_id = request.query_params.get('classroom_id')
        
        # Get all submissions for this student
        submissions = StudentSubmission.objects.filter(student=request.user)
        
        # If classroom_id is provided (archived view mode), filter submissions by classroom
        if classroom_id:
            from .models import StudentPromotionHistory, StudentClassroomHistory
            try:
                archived_classroom = Classroom.objects.get(id=classroom_id)
                
                # Verify student has access to this classroom
                was_promoted_from = StudentPromotionHistory.objects.filter(
                    student=request.user,
                    previous_classroom=archived_classroom
                ).exists()
                
                was_student_archived = StudentClassroomHistory.objects.filter(
                    student=request.user,
                    classroom=archived_classroom
                ).exists()
                
                is_current_student = request.user.classroom == archived_classroom
                
                if is_current_student or was_promoted_from or was_student_archived:
                    # Filter submissions to only those from this classroom
                    submissions = submissions.filter(activity__folder__classroom=archived_classroom)
                    print(f"📝 Student viewing archived submission remarks for classroom {archived_classroom.name}")
            except Classroom.DoesNotExist:
                print(f"⚠️ Classroom {classroom_id} not found for submission remarks filter")

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

        # Find the classroom instance - prioritize current school year
        from .models import SchoolYear
        current_sy = SchoolYear.get_current_for_teacher(request.user)
        
        classroom = None
        try:
            # First try to find classroom in current school year
            if current_sy:
                classroom = Classroom.objects.filter(
                    name=class_name,
                    school_year=current_sy.name,
                    is_archived=False
                ).first()
                print(f"📚 Looking for classroom in current school year: {current_sy.name}")
            
            # Fallback: any non-archived classroom with this name
            if not classroom:
                classroom = Classroom.objects.filter(
                    name=class_name,
                    is_archived=False
                ).first()
            
            # Last resort: any classroom with this name
            if not classroom:
                classroom = Classroom.objects.filter(name=class_name).first()
            
            if not classroom:
                return Response({'error': f'Classroom "{class_name}" not found.'}, status=status.HTTP_404_NOT_FOUND)
            
            print(f"✅ Found classroom: {classroom.name} (ID: {classroom.id}, School Year: {classroom.school_year})")
        except Exception as e:
            print(f"❌ Error finding classroom: {str(e)}")
            return Response({'error': f'Error finding classroom: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Create or update compilation request for this specific classroom
        print(f"Creating/updating compilation request for classroom: {classroom.id}")
        compilation_request, created = PortfolioCompilationRequest.objects.get_or_create(
            classroom=classroom,
            requested_by=request.user,
            defaults={'is_active': True, 'class_name': class_name}
        )
        print(f"Compilation request {'created' if created else 'updated'}: {compilation_request.id}")

        if not created:
            # Update existing request
            compilation_request.is_active = True
            compilation_request.class_name = class_name
            compilation_request.requested_at = timezone.now()
            compilation_request.save()

        # Get students from the specific classroom requested
        if not classroom:
            return Response({
                'error': 'Classroom could not be determined from the request.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Extract section from classroom name (e.g., "Grade 1 - A" -> "A")
        try:
            # Split by '-' and take the last part, then strip whitespace
            classroom_section = classroom.name.split('-')[-1].strip()
        except (IndexError, AttributeError):
            # Fallback if name format is unexpected
            classroom_section = None

        if classroom_section:
            students = User.objects.filter(
                Q(role='student') &
                (
                    Q(classroom=classroom) |
                    Q(student_profile__grade_level=classroom.grade_level, student_profile__section=classroom_section)
                )
            ).distinct()
        else:
            # If section can't be determined, fall back to classroom link only
            students = User.objects.filter(role='student', classroom=classroom).distinct()

        print(f"📢 Found {students.count()} students in {classroom.name} to notify")

        # Create notifications for all students in a single, efficient query
        notifications_to_create = [
            Notification(
                recipient=student,
                notification_type='portfolio_compilation',
                title=f'Portfolio Compilation - {class_name}',
                message=f'Your teacher has asked you to start compiling your portfolio for {class_name}.'
            )
            for student in students
        ]

        if notifications_to_create:
            Notification.objects.bulk_create(notifications_to_create)
            print(f"✅ Successfully created {len(notifications_to_create)} notifications in bulk.")

        notifications_created = len(notifications_to_create)

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
def check_portfolio_compilation_status_api(request, classroom_id):
    """
    GET: Check if portfolio compilation has been requested for a class
    DELETE: Drop/cancel portfolio compilation request for a class (teacher only)
    """
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        try:
            classroom = None
            # Handle based on user role
            if request.user.role == 'student':
                # Try to get classroom from user directly
                if hasattr(request.user, 'classroom') and request.user.classroom:
                    classroom = request.user.classroom
                    print(f"✅ Found classroom from user.classroom: {classroom.id}")
                else:
                    # Try student_profile as fallback
                    try:
                        student_profile = request.user.student_profile
                        classroom = student_profile.classroom
                        print(f"✅ Found classroom from student_profile: {classroom.id}")
                    except AttributeError:
                        print(f"❌ No classroom found for student {request.user.username}")
                        return Response({'error': 'Student has no classroom assigned.'}, status=status.HTTP_404_NOT_FOUND)

                # Verify classroom ID matches
                if not classroom or classroom.id != classroom_id:
                    print(f"⚠️ Classroom mismatch: student classroom={classroom.id if classroom else None}, requested={classroom_id}")
                    return Response({'error': 'Classroom mismatch for student.'}, status=status.HTTP_403_FORBIDDEN)

            elif request.user.role == 'teacher':
                try:
                    # First try to find classroom where teacher is assigned
                    classroom = Classroom.objects.filter(id=classroom_id, teacher=request.user).first()
                    if classroom:
                        print(f"✅ Found assigned classroom for teacher: {classroom.id}")
                    else:
                        # If not assigned, check if teacher has folders in this classroom
                        has_folders = PortfolioFolder.objects.filter(
                            classroom_id=classroom_id,
                            teacher=request.user
                        ).exists()
                        if has_folders:
                            classroom = Classroom.objects.get(id=classroom_id)
                            print(f"✅ Found classroom where teacher has folders: {classroom.id}")
                        else:
                            print(f"❌ Classroom {classroom_id} not found for teacher {request.user.username}")
                            return Response({'error': 'Classroom not found or you have no access.'}, status=status.HTTP_404_NOT_FOUND)
                except Classroom.DoesNotExist:
                    print(f"❌ Classroom {classroom_id} does not exist")
                    return Response({'error': 'Classroom not found.'}, status=status.HTTP_404_NOT_FOUND)

            else:
                return Response({'error': 'Unauthorized role.'}, status=status.HTTP_403_FORBIDDEN)

            if not classroom:
                 return Response({'error': 'Could not determine classroom.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check for an active compilation request tied to the specific classroom
            compilation_request = PortfolioCompilationRequest.objects.filter(
                classroom=classroom,
                is_active=True
            ).first()

            if compilation_request:
                # Also check if the student has a notification for this
                class_name_str = f"Grade {classroom.grade_level} - {classroom.section}"
                has_notification = Notification.objects.filter(
                    recipient=request.user,
                    notification_type='portfolio_compilation',
                    message__icontains=class_name_str
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
            # Get the classroom object
            try:
                classroom = Classroom.objects.get(id=classroom_id, teacher=request.user)
                class_name = f"Grade {classroom.grade_level} - {classroom.section}"
                print(f"🗑️ Dropping portfolio compilation for class: {class_name}")
            except Classroom.DoesNotExist:
                return Response({'error': 'Classroom not found or you are not the teacher.'}, status=status.HTTP_404_NOT_FOUND)

            # Find and deactivate the compilation request
            compilation_request = PortfolioCompilationRequest.objects.filter(
                classroom=classroom,
                is_active=True
            ).first()

            if not compilation_request:
                return Response({'error': 'No active compilation request found for this class'}, status=status.HTTP_404_NOT_FOUND)

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

            # Get students in the classroom to notify about cancellation
            students = User.objects.filter(
                role='student',
                classroom=classroom
            ).exclude(username='admin')

            print(f"📢 Notifying {students.count()} students in {class_name} about cancellation")

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
            # Get classroom by name and student's classroom
            student_classroom = request.user.classroom
            if student_classroom:
                compilation_request = PortfolioCompilationRequest.objects.filter(
                    classroom=student_classroom,
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
            else:
                print(f"⚠️ Student has no classroom assigned")

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
    """Get all activities (submitted, resubmitted, late, and missing) for a student's portfolio - ONLY from their assigned classroom"""
    try:
        from .models import PortfolioActivity, StudentSubmission, PortfolioFolder
        from datetime import datetime, time as datetime_time

        print(f"📚 Fetching portfolio activities for student: {request.user.username} in class: {class_name}")

        # Get student's classroom
        student_classroom = request.user.classroom

        if not student_classroom:
            print(f"⚠️ Student {request.user.username} has no assigned classroom")
            return Response({
                'all_activities': [],
                'submitted_activities': [],
                'resubmitted_activities': [],
                'late_activities': [],
                'missing_activities': [],
                'submitted_count': 0,
                'resubmitted_count': 0,
                'late_count': 0,
                'missing_count': 0
            }, status=status.HTTP_200_OK)

        print(f"✅ Student classroom: {student_classroom.name} (ID: {student_classroom.id})")

        # Get ONLY portfolio folders for this student's assigned classroom
        folders = PortfolioFolder.objects.filter(
            classroom=student_classroom,
            class_name=class_name
        )

        print(f"📁 Found {folders.count()} folders for classroom {student_classroom.name}")

        activity_list = []
        submitted_activities = []
        resubmitted_activities = []
        late_activities = []
        missing_activities = []
        processed_activity_ids = set()  # Track processed activities to avoid duplicates

        for folder in folders:
            # Get only published activities in this folder (students should not see drafts)
            activities = PortfolioActivity.objects.filter(folder=folder, is_published=True).order_by('created_at')

            for activity in activities:
                # Skip if already processed (avoid duplicates)
                if activity.id in processed_activity_ids:
                    print(f"   ⚠️ Skipping duplicate activity {activity.id} ({activity.title})")
                    continue
                processed_activity_ids.add(activity.id)

                # Get the LATEST SCORED submission for this activity
                # This handles resubmissions - we want the most recent SCORED version
                # Get the LATEST SCORED or COMPILED submission for this activity
                from django.db.models import Q
                submission = StudentSubmission.objects.filter(
                    activity=activity,
                    student=request.user,
                    is_active=True
                ).filter(
                    Q(status='scored') | Q(compiled=True)
                ).order_by('-submitted_at').first()

                # Also check if there are any unscored submissions (for debugging)
                unscored_count = StudentSubmission.objects.filter(
                    activity=activity,
                    student=request.user,
                    is_active=True
                ).exclude(status__in=['draft', 'scored']).count()

                if unscored_count > 0:
                    print(f"   📝 Activity {activity.id} has {unscored_count} unscored submission(s) - treating as missing")

                # Get submission file path with better error handling
                submission_file = None
                if submission:
                    try:
                        # Try file field first (for uploaded files) - check if file exists
                        if submission.file:
                            try:
                                if hasattr(submission.file, 'path') and os.path.exists(submission.file.path):
                                    # File exists, build full URL
                                    submission_file = request.build_absolute_uri(submission.file.url)
                                    print(f"   📎 Using file.url: {submission_file[:100]}...")
                                else:
                                    print(f"   ⚠️ File field exists but file not found on disk")
                            except Exception as e:
                                print(f"   ⚠️ Error checking file: {str(e)}")

                        # Fallback to file_path (for base64 or legacy data)
                        if not submission_file and submission.file_path:
                            submission_file = submission.file_path
                            print(f"   📎 Using file_path (base64): {submission_file[:100]}...")

                        if not submission_file:
                            print(f"   ⚠️ No file found for submission {submission.id}")
                    except Exception as file_error:
                        print(f"⚠️ Error getting submission file for activity {activity.id}: {file_error}")
                        submission_file = None

                # Convert submission time to local timezone if exists
                local_submitted_time = None
                submitted_date_str = None
                submitted_time_str = None

                if submission and submission.submitted_at:
                    try:
                        import pytz
                        manila_tz = pytz.timezone('Asia/Manila')
                        
                        # Convert to Manila timezone
                        if timezone.is_naive(submission.submitted_at):
                            # Make it aware in UTC first, then convert to Manila
                            aware_time = timezone.make_aware(submission.submitted_at, timezone=pytz.UTC)
                            local_submitted_time = aware_time.astimezone(manila_tz)
                        else:
                            local_submitted_time = submission.submitted_at.astimezone(manila_tz)
                        
                        submitted_date_str = local_submitted_time.strftime('%b %d, %Y')
                        submitted_time_str = local_submitted_time.strftime('%I:%M %p')
                    except Exception as date_error:
                        # Fallback: use the datetime directly without timezone conversion
                        try:
                            submitted_date_str = submission.submitted_at.strftime('%b %d, %Y')
                            submitted_time_str = submission.submitted_at.strftime('%I:%M %p')
                            local_submitted_time = submission.submitted_at
                        except:
                            print(f"⚠️ Error formatting submission date: {date_error}")

                # Determine submission status and category
                # Since we're ONLY getting scored submissions now, logic is simpler
                submission_status = 'missing'
                is_late = False
                is_resubmitted = False
                is_compilation = False  # Initialize is_compilation before the if block
                has_pending_submission = False

                # Check if there's a pending (unscored) submission that is NOT a compilation
                # Compilation submissions should show as "compiled" even if unscored
                if not submission and unscored_count > 0:
                    # Check if the unscored submission is a compilation
                    unscored_submission = StudentSubmission.objects.filter(
                        activity=activity,
                        student=request.user,
                        is_active=True
                    ).exclude(status__in=['draft', 'scored']).first()
                    
                    if unscored_submission and (unscored_submission.compiled or unscored_submission.is_compilation):
                        # This is a compiled submission - use it
                        submission = unscored_submission
                        is_compilation = True
                        submission_status = 'compiled'
                        
                        # Get the submitted_at time for compiled submissions
                        if submission.submitted_at:
                            try:
                                import pytz
                                manila_tz = pytz.timezone('Asia/Manila')
                                if timezone.is_naive(submission.submitted_at):
                                    aware_time = timezone.make_aware(submission.submitted_at, timezone=pytz.UTC)
                                    local_submitted_time = aware_time.astimezone(manila_tz)
                                else:
                                    local_submitted_time = submission.submitted_at.astimezone(manila_tz)
                                submitted_date_str = local_submitted_time.strftime('%b %d, %Y')
                                submitted_time_str = local_submitted_time.strftime('%I:%M %p')
                            except Exception as date_error:
                                # Try without timezone conversion
                                try:
                                    submitted_date_str = submission.submitted_at.strftime('%b %d, %Y')
                                    submitted_time_str = submission.submitted_at.strftime('%I:%M %p')
                                    local_submitted_time = submission.submitted_at
                                except:
                                    pass
                        elif submission.compiled_at:
                            try:
                                import pytz
                                manila_tz = pytz.timezone('Asia/Manila')
                                if timezone.is_naive(submission.compiled_at):
                                    aware_time = timezone.make_aware(submission.compiled_at, timezone=pytz.UTC)
                                    local_submitted_time = aware_time.astimezone(manila_tz)
                                else:
                                    local_submitted_time = submission.compiled_at.astimezone(manila_tz)
                                submitted_date_str = local_submitted_time.strftime('%b %d, %Y')
                                submitted_time_str = local_submitted_time.strftime('%I:%M %p')
                            except Exception as date_error:
                                try:
                                    submitted_date_str = submission.compiled_at.strftime('%b %d, %Y')
                                    submitted_time_str = submission.compiled_at.strftime('%I:%M %p')
                                    local_submitted_time = submission.compiled_at
                                except:
                                    pass
                        
                        # Fallback to scored_at if no submitted_at or compiled_at
                        if not local_submitted_time and submission.scored_at:
                            try:
                                import pytz
                                manila_tz = pytz.timezone('Asia/Manila')
                                if timezone.is_naive(submission.scored_at):
                                    aware_time = timezone.make_aware(submission.scored_at, timezone=pytz.UTC)
                                    local_submitted_time = aware_time.astimezone(manila_tz)
                                else:
                                    local_submitted_time = submission.scored_at.astimezone(manila_tz)
                                submitted_date_str = local_submitted_time.strftime('%b %d, %Y')
                                submitted_time_str = local_submitted_time.strftime('%I:%M %p')
                            except:
                                pass
                        
                        # Final fallback to current time if nothing else available
                        if not local_submitted_time:
                            try:
                                import pytz
                                manila_tz = pytz.timezone('Asia/Manila')
                                local_submitted_time = timezone.now().astimezone(manila_tz)
                                submitted_date_str = local_submitted_time.strftime('%b %d, %Y')
                                submitted_time_str = local_submitted_time.strftime('%I:%M %p')
                                print(f"   ⚠️ Using current time as fallback for compiled submission date")
                            except:
                                pass
                        
                        # Get submission file for compiled submission
                        if submission.file:
                            try:
                                if hasattr(submission.file, 'path') and os.path.exists(submission.file.path):
                                    submission_file = request.build_absolute_uri(submission.file.url)
                            except:
                                pass
                        if not submission_file and submission.file_path:
                            submission_file = submission.file_path
                        
                        print(f"   📦 Activity {activity.id} has COMPILED submission (not scored yet)")
                    else:
                        has_pending_submission = True
                        submission_status = 'pending'
                        print(f"   ⏳ Activity {activity.id} has pending submission (not scored yet)")

                if submission:
                    # Check if it's a resubmission
                    is_resubmitted = submission.resubmit_count > 0 if hasattr(submission, 'resubmit_count') else False

                    # Check if submitted late
                    if activity.due_date and submission.submitted_at:
                        try:
                            # Combine due date and time for accurate comparison
                            if activity.due_time:
                                due_datetime_naive = datetime.combine(activity.due_date, activity.due_time)
                            else:
                                # If no time specified, use end of day (23:59:59)
                                due_datetime_naive = datetime.combine(activity.due_date, datetime_time(23, 59, 59))

                            # Make sure due_datetime is timezone-aware
                            if timezone.is_naive(due_datetime_naive):
                                due_datetime = timezone.make_aware(due_datetime_naive)
                            else:
                                due_datetime = due_datetime_naive

                            # Ensure submission.submitted_at is timezone-aware
                            submitted_at = submission.submitted_at
                            if timezone.is_naive(submitted_at):
                                submitted_at = timezone.make_aware(submitted_at)

                            is_late = submitted_at > due_datetime
                        except Exception as date_error:
                            print(f"⚠️ Error checking late status for activity {activity.id}: {date_error}")
                            is_late = False

                    # Determine status based on flags
                    # Check if this is a compilation submission
                    is_compilation = submission.compiled if hasattr(submission, 'compiled') else getattr(submission, 'is_compilation', False)

                    # Check if the submission has been scored (has a score value)
                    has_score = submission.score is not None

                    if is_compilation and not has_score:
                        # Compiled but not yet scored by teacher
                        submission_status = 'compiled'
                    elif is_compilation and has_score:
                        # Compiled AND scored by teacher - show as scored with compilation flag
                        submission_status = 'scored'
                    elif is_resubmitted:
                        submission_status = 'scored_resubmitted'
                    elif is_late:
                        submission_status = 'scored_late'
                    else:
                        submission_status = 'scored'

                    print(f"   ✅ Found SCORED submission: ID={submission.id}, Score={submission.score}, Compilation={is_compilation}, HasScore={has_score}, Resubmit={is_resubmitted}, Late={is_late}")

                # Get submission files (multiple files support)
                submission_files = []
                if submission:
                    try:
                        from .models import SubmissionFile
                        files = SubmissionFile.objects.filter(submission=submission)
                        for f in files:
                            # Build proper file URL - use absolute URL for file field, or file_path for base64
                            file_url = None
                            if f.file:
                                try:
                                    file_url = request.build_absolute_uri(f.file.url)
                                except:
                                    file_url = f.file_path
                            else:
                                file_url = f.file_path
                            
                            submission_files.append({
                                'id': f.id,
                                'path': file_url,
                                'type': f.file_type,
                                'name': f.file_name or f'file_{f.id}'
                            })
                        print(f"   📁 Found {len(submission_files)} files for submission {submission.id}")
                        
                        # Fallback: if no files in SubmissionFile table, use the single file from submission
                        if len(submission_files) == 0 and submission_file:
                            file_type = 'image' if (submission_file.startswith('data:image') or submission_file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))) else 'file'
                            submission_files.append({
                                'id': 0,
                                'path': submission_file,
                                'type': file_type,
                                'name': 'submission_file'
                            })
                            print(f"   📁 Added fallback single file to submission_files")
                    except Exception as files_error:
                        print(f"⚠️ Error getting submission files: {files_error}")

                # Calculate max_score from scoring_criteria
                max_score = None
                scoring_criteria_data = None
                try:
                    import json
                    if activity.scoring_criteria:
                        criteria = json.loads(activity.scoring_criteria) if isinstance(activity.scoring_criteria, str) else activity.scoring_criteria
                        scoring_criteria_data = criteria  # Store the criteria for frontend
                        if criteria and isinstance(criteria, list):
                            max_score = sum(int(c.get('maxScore', 0)) for c in criteria)
                except Exception as score_error:
                    print(f"⚠️ Error calculating max_score: {score_error}")

                # Get instruction files for this activity
                instruction_files_data = []
                try:
                    for inst_file in activity.instruction_files.all():
                        instruction_files_data.append({
                            'id': inst_file.id,
                            'file_name': inst_file.file_name,
                            'file_url': request.build_absolute_uri(inst_file.file.url) if inst_file.file else None,
                            'file_type': inst_file.file_type
                        })
                except Exception as inst_error:
                    print(f"⚠️ Error getting instruction files: {inst_error}")

                activity_data = {
                    'id': activity.id,
                    'title': activity.title,
                    'description': activity.description,
                    'scoring_criteria': scoring_criteria_data,  # Include scoring criteria for frontend
                    'instruction_files': instruction_files_data,  # Include instruction files
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
                    'submission_files': submission_files,  # Multiple files support
                    'submission_caption': submission.caption if submission else None,
                    'submission_score': submission.score if submission else None,
                    'max_score': max_score,  # Maximum possible score from criteria
                    'submission_feedback': submission.feedback if submission else None,
                    'submission_status': submission_status,
                    'scored_at': submission.scored_at.isoformat() if submission and submission.scored_at else None,
                    'is_scored': submission is not None and submission.status == 'scored',  # True only if actually scored
                    'is_late': is_late,
                    'is_resubmitted': is_resubmitted,
                    'is_compilation': is_compilation,  # True if this is a compilation submission
                    'has_pending_submission': has_pending_submission,  # True if submitted but not scored
                    'resubmit_count': submission.resubmit_count if submission and hasattr(submission, 'resubmit_count') else 0,
                    'last_resubmit_at': submission.last_resubmit_at.isoformat() if submission and hasattr(submission, 'last_resubmit_at') and submission.last_resubmit_at else None,
                    'folder_name': folder.name
                }

                print(f"📝 Activity {activity.id} ({activity.title}): status={submission_status}, late={is_late}, resubmitted={is_resubmitted}, compilation={is_compilation}")

                activity_list.append(activity_data)

                # Categorize into separate lists
                # Now we have compiled, scored_resubmitted, scored_late, scored, pending, and missing
                if submission_status == 'compiled':
                    submitted_activities.append(activity_data)  # Compiled activities go to submitted list
                    print(f"   📦 Added compiled activity to submitted list: {activity.title}")
                elif submission_status == 'scored_resubmitted':
                    resubmitted_activities.append(activity_data)
                    submitted_activities.append(activity_data)  # Also include in submitted since it's scored
                elif submission_status == 'scored_late':
                    late_activities.append(activity_data)
                    submitted_activities.append(activity_data)  # Also include in submitted since it's scored
                elif submission_status == 'scored':
                    submitted_activities.append(activity_data)  # Regular scored submission
                elif submission_status == 'pending':
                    # Pending submissions (submitted but not scored) - DO NOT show in missing
                    # These are waiting for teacher to score, not missing
                    print(f"   ⏳ Skipping pending activity from missing list: {activity.title}")
                    pass  # Don't add to any list - it's in limbo waiting for score
                else:  # truly missing (never submitted)
                    # Check if there's ANY submission for this activity (compiled, unscored, or otherwise)
                    has_any_submission = StudentSubmission.objects.filter(
                        activity=activity,
                        student=request.user,
                        is_active=True
                    ).filter(
                        Q(compiled=True) | Q(is_compilation=True) | Q(missing=False) | Q(status='unscored')
                    ).exists()

                    if has_any_submission:
                        print(f"   ✅ Activity {activity.id} ({activity.title}) has submission - skipping from missing")
                        continue  # Skip this activity, it has a submission

                    # Only add to missing if:
                    # 1. Activity is published
                    # 2. Due date has PASSED
                    if not activity.is_published:
                        print(f"   ⚠️ Activity {activity.id} ({activity.title}) is NOT PUBLISHED - skipping from missing")
                        continue

                    is_overdue = False
                    if activity.due_date:
                        try:
                            # Combine due date and time for accurate comparison
                            if activity.due_time:
                                due_datetime_naive = datetime.combine(activity.due_date, activity.due_time)
                            else:
                                # If no time specified, use end of day (23:59:59)
                                due_datetime_naive = datetime.combine(activity.due_date, datetime_time(23, 59, 59))

                            # Make sure due_datetime is timezone-aware
                            if timezone.is_naive(due_datetime_naive):
                                due_datetime = timezone.make_aware(due_datetime_naive)
                            else:
                                due_datetime = due_datetime_naive

                            # Check if current time is past the due date
                            current_time = timezone.now()
                            is_overdue = current_time > due_datetime

                            if is_overdue:
                                print(f"   ❌ Activity {activity.id} ({activity.title}) is OVERDUE - adding to missing")
                                missing_activities.append(activity_data)
                            else:
                                print(f"   ⏰ Activity {activity.id} ({activity.title}) is NOT YET DUE - skipping from missing")
                        except Exception as date_error:
                            print(f"⚠️ Error checking due date for activity {activity.id}: {date_error}")
                            # If we can't determine, don't add to missing to be safe
                    else:
                        # No due date set - don't consider it missing
                        print(f"   ℹ️ Activity {activity.id} ({activity.title}) has no due date - skipping from missing")

        # Sort submitted_activities by submission_date (most recent first)
        submitted_activities.sort(key=lambda x: x.get('submission_date') or '', reverse=True)
        
        print(f"✅ Categorized activities:")
        print(f"   - Submitted: {len(submitted_activities)}")
        print(f"   - Resubmitted: {len(resubmitted_activities)}")
        print(f"   - Late: {len(late_activities)}")
        print(f"   - Missing: {len(missing_activities)}")

        return Response({
            'all_activities': activity_list,
            'submitted_activities': submitted_activities,
            'resubmitted_activities': resubmitted_activities,
            'late_activities': late_activities,
            'missing_activities': missing_activities,
            'total_count': len(activity_list),
            'submitted_count': len(submitted_activities),
            'resubmitted_count': len(resubmitted_activities),
            'late_count': len(late_activities),
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
    """Submit a missing activity from portfolio compilation (supports multiple files)"""
    try:
        from .models import PortfolioActivity, StudentSubmission, SubmissionFile
        import base64
        from django.core.files.base import ContentFile

        print(f"📝 Submitting missing activity {activity_id} for student: {request.user.username}")

        # Get the activity
        activity = PortfolioActivity.objects.get(id=activity_id)

        # Get submission data
        file_data = request.data.get('file')
        files_data = request.data.get('files', [])  # Multiple files support
        caption = request.data.get('caption', '')

        print(f"📥 Received file_data: {bool(file_data)}, files_data count: {len(files_data) if isinstance(files_data, list) else 'not a list'}")
        print(f"📥 files_data type: {type(files_data)}")

        # Ensure files_data is a list
        if not isinstance(files_data, list):
            files_data = [files_data] if files_data else []

        if not file_data and not files_data:
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

        # Handle primary file upload
        primary_file_path = file_data
        primary_file_type = 'file'
        
        if file_data and file_data.startswith('data:'):
            # Base64 encoded file
            format, filestr = file_data.split(';base64,')
            ext = format.split('/')[-1]
            file_name = f"submission_{request.user.id}_{activity_id}.{ext}"
            primary_file_type = 'image' if 'image' in format else ('pdf' if ext == 'pdf' else 'file')

            # Create submission with file - mark as compiled since it's from missing activity compilation
            submission = StudentSubmission.objects.create(
                activity=activity,
                student=request.user,
                caption=caption,
                file=ContentFile(base64.b64decode(filestr), name=file_name),
                file_path=file_data,  # Keep base64 for compatibility
                file_type=primary_file_type,
                status='unscored',
                approval_status='pending',
                post_to_feed=False,
                is_compilation=True,  # Mark as compilation submission
                compiled=True,  # Mark as compiled
                missing=False,  # No longer missing
                is_active=True,  # Explicitly set as active
                compiled_at=timezone.now(),  # Set compilation timestamp
                submitted_at=timezone.now()  # Set submission timestamp
            )
        else:
            # Regular file path - mark as compiled since it's from missing activity compilation
            submission = StudentSubmission.objects.create(
                activity=activity,
                student=request.user,
                caption=caption,
                file_path=file_data if file_data else '',
                file_type=primary_file_type,
                status='unscored',
                approval_status='pending',
                post_to_feed=False,
                is_compilation=True,  # Mark as compilation submission
                compiled=True,  # Mark as compiled
                missing=False,  # No longer missing
                is_active=True,  # Explicitly set as active
                compiled_at=timezone.now(),  # Set compilation timestamp
                submitted_at=timezone.now()  # Set submission timestamp
            )

        # Handle additional files - save ALL files to SubmissionFile table
        submission_files = []
        # Use files_data if available, otherwise use file_data as single file
        all_files = files_data if files_data and len(files_data) > 0 else ([file_data] if file_data else [])
        
        print(f"📁 Processing {len(all_files)} files for SubmissionFile table")
        
        for idx, f_data in enumerate(all_files):
            if not f_data:
                print(f"⚠️ Skipping empty file at index {idx}")
                continue
                
            file_type = 'file'
            file_url = f_data
            
            if isinstance(f_data, str) and f_data.startswith('data:'):
                format_part = f_data.split(';base64,')[0]
                file_type = 'image' if 'image' in format_part else ('pdf' if 'pdf' in format_part else 'file')
            
            # Create SubmissionFile record
            try:
                sub_file = SubmissionFile.objects.create(
                    submission=submission,
                    file_path=file_url,  # Use file_path field for base64 data
                    file_type=file_type,
                    file_name=f"file_{idx + 1}"
                )
                submission_files.append({
                    'id': sub_file.id,
                    'path': sub_file.file_url,
                    'type': sub_file.file_type,
                    'name': sub_file.file_name
                })
                print(f"✅ Added file {idx + 1} to submission (type: {file_type})")
            except Exception as file_error:
                print(f"⚠️ Error adding file {idx + 1}: {str(file_error)}")

        print(f"✅ Missing activity submitted successfully: {submission.id} with {len(submission_files)} files")

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
                'status': submission.status,
                'files': submission_files
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
@api_view(['POST'])
def compile_activity_api(request):
    """
    POST: Compile an activity (mark as compiled and not missing)
    This creates an UNSCORED submission that will appear in teacher's Submitted tab
    """
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)

    activity_id = request.data.get('activity_id')
    if not activity_id:
        return Response({'error': 'Activity ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        from .models import PortfolioActivity, StudentSubmission
        from django.utils import timezone

        # Get the activity
        activity = PortfolioActivity.objects.get(id=activity_id)

        # Get or create submission
        submission, created = StudentSubmission.objects.get_or_create(
            student=request.user,
            activity=activity,
            defaults={
                'status': 'unscored',  # Changed from 'scored' to 'unscored' so it appears in Submitted tab
                'approval_status': 'pending',
                'is_active': True,
                'submitted_at': timezone.now(),
                'scored_at': None  # Don't set scored_at - teacher needs to score it
            }
        )

        # Update fields
        submission.is_compilation = True  # Mark as compilation submission
        submission.compiled = True
        submission.missing = False
        submission.compiled_at = timezone.now()

        # For existing submissions, update status to unscored if not already scored by teacher
        if not created and submission.score is None:
            submission.status = 'unscored'
            submission.scored_at = None

        if not submission.submitted_at:
            submission.submitted_at = timezone.now()

        submission.save()

        print(f"✅ Activity {activity_id} compiled for user {request.user.username} (status: {submission.status})")

        return Response({
            'success': True,
            'message': 'Activity compiled successfully',
            'data': {
                'id': submission.id,
                'activity_id': activity.id,
                'compiled': True,
                'missing': False,
                'compiled_at': submission.compiled_at.isoformat()
            }
        })

    except PortfolioActivity.DoesNotExist:
        return Response({'error': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"❌ Error compiling activity: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['POST'])
def submit_compilation_api(request, activity_id):
    """Submit a compilation from portfolio - creates a scored submission for Activity Compilation carousel"""
    try:
        from .models import PortfolioActivity, StudentSubmission
        import base64
        from django.core.files.base import ContentFile

        print(f"📝 Submitting compilation for activity {activity_id}, student: {request.user.username}")

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
            student=request.user,
            is_active=True
        ).exclude(status='draft').first()

        if existing_submission:
            # Update existing submission instead of erroring
            submission = existing_submission
            submission.caption = caption
            # Handle file update logic if needed
            print(f"🔄 Updating existing submission {submission.id} for compilation")
        else:
             # Handle file upload
            if file_data.startswith('data:'):
                # Base64 encoded file
                format, filestr = file_data.split(';base64,')
                ext = format.split('/')[-1]
                file_name = f"compilation_{request.user.id}_{activity_id}.{ext}"

                # Determine file type
                file_type = 'image' if 'image' in format else 'pdf' if 'pdf' in format else 'file'

                # Create submission with SCORED status so it appears in Activity Compilation
                submission = StudentSubmission.objects.create(
                    activity=activity,
                    student=request.user,
                    caption=caption,
                    file=ContentFile(base64.b64decode(filestr), name=file_name),
                    file_path=file_data,  # Keep base64 for compatibility
                    file_type=file_type,
                    status='scored',  # Set as scored to appear in Activity Compilation
                    score=None,  # No score for compilation submissions
                    approval_status='approved',  # Auto-approve compilation submissions
                    post_to_feed=False,
                    is_active=True
                )
            else:
                # Regular file path
                submission = StudentSubmission.objects.create(
                    activity=activity,
                    student=request.user,
                    caption=caption,
                    file_path=file_data,
                    file_type='file',
                    status='scored',  # Set as scored to appear in Activity Compilation
                    score=None,  # No score for compilation submissions
                    approval_status='approved',
                    post_to_feed=False,
                    is_active=True
                )

        # Update compilation status fields
        submission.is_compilation = True  # Mark as compilation submission
        submission.compiled = True
        submission.missing = False
        submission.compiled_at = timezone.now()
        submission.save()

        print(f"✅ Compilation submitted successfully: {submission.id} (status: scored)")

        # Notify teacher
        try:
            teacher = activity.folder.teacher
            notification_title = f'Portfolio Compilation Submitted - {activity.title}'
            notification_message = f'{request.user.username} has submitted a portfolio compilation for "{activity.title}" in {activity.folder.class_name}.'

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
            'message': 'Compilation submitted successfully',
            'submission': {
                'id': submission.id,
                'activity_id': activity.id,
                'activity_title': activity.title,
                'caption': submission.caption,
                'submitted_at': submission.submitted_at.isoformat() if submission.submitted_at else timezone.now().isoformat(),
                'scored_at': submission.scored_at.isoformat() if submission.scored_at else None,
                'status': submission.status,
                'score': submission.score,
                'compiled': True,
                'missing': False
            }
        }, status=status.HTTP_201_CREATED)

    except PortfolioActivity.DoesNotExist:
        return Response({'error': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        import traceback
        print(f"❌ Error submitting compilation: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
def get_portfolio_envelopes_api(request, class_name):
    """Get all portfolio envelopes for a class (teacher only) - filtered by student's actual classroom assignment"""
    try:
        from .models import PortfolioEnvelope, Classroom

        print(f"📋 Fetching portfolio envelopes for class: {class_name}")

        # Check if user is a teacher
        if request.user.role != 'teacher':
            return Response({
                'error': 'Only teachers can view portfolio envelopes'
            }, status=status.HTTP_403_FORBIDDEN)

        # Get the classroom for this class_name - prioritize current school year
        # IMPORTANT: Prioritize non-archived classrooms from the current school year
        from .models import SchoolYear
        current_sy = SchoolYear.get_current_for_teacher(request.user)
        
        target_classroom = None
        if current_sy:
            target_classroom = Classroom.objects.filter(
                name=class_name,
                school_year=current_sy.name,
                is_archived=False
            ).first()
            print(f"🔍 Looking for classroom '{class_name}' in current school year: {current_sy.name}")
        
        # Fallback: try any non-archived classroom
        if not target_classroom:
            target_classroom = Classroom.objects.filter(
                name=class_name,
                is_archived=False
            ).first()
        
        # Last resort: any classroom with this name
        if not target_classroom:
            target_classroom = Classroom.objects.filter(name=class_name).first()

        if not target_classroom:
            print(f"⚠️ Classroom {class_name} not found")
            return Response({
                'envelopes': [],
                'count': 0
            }, status=status.HTTP_200_OK)

        print(f"📚 Found classroom: {target_classroom.name} (ID: {target_classroom.id})")

        # Get all envelopes for students who are actually assigned to this classroom
        # This ensures we filter by the student's actual classroom assignment, not just the class_name in the envelope
        envelopes = PortfolioEnvelope.objects.filter(
            class_name=class_name,
            student__classroom=target_classroom  # Filter by student's actual classroom assignment
        ).select_related('student', 'student__classroom')

        envelope_list = []
        for envelope in envelopes:
            # Convert UTC time to local timezone (Asia/Manila)
            local_time = timezone.localtime(envelope.created_at)
            submitted_time = timezone.localtime(envelope.submitted_at) if envelope.submitted_at else local_time

            # Count activities for this student in this class
            from .models import StudentSubmission, PortfolioFolder, PortfolioActivity
            from django.db.models import Q
            
            # Get folders for this class - ONLY from the target classroom (current school year)
            # This prevents counting activities from old school years
            folders = PortfolioFolder.objects.filter(
                classroom=target_classroom
            )

            # Get all unique published activity IDs using a single query
            all_activity_ids = list(PortfolioActivity.objects.filter(
                folder__in=folders,
                is_published=True
            ).values_list('id', flat=True).distinct())
            
            total_activities = len(all_activity_ids)
            
            # Count compiled activities in a single query
            compiled_count = StudentSubmission.objects.filter(
                activity_id__in=all_activity_ids,
                student=envelope.student,
                is_active=True
            ).filter(
                Q(status='scored') | Q(compiled=True) | Q(is_compilation=True)
            ).values('activity_id').distinct().count()
            
            missing_count = total_activities - compiled_count
            
            # Determine status based on is_submitted flag only
            # In Progress = student is still working on compilation
            # Done = student has submitted their portfolio
            if envelope.is_submitted:
                status_text = 'Done'
            else:
                status_text = 'In Progress'
            
            activity_count = 0  # Not needed for simple status

            # Build profile picture URL
            profile_picture_url = None
            if envelope.student.profile_picture:
                profile_picture_url = request.build_absolute_uri(envelope.student.profile_picture.url)

            envelope_list.append({
                'id': envelope.id,
                'student_id': envelope.student.id,
                'student_name': envelope.student_name,
                'name': envelope.student_name,  # Add 'name' field for consistency
                'student_username': envelope.student.username,
                'id_number': envelope.student.id_number if envelope.student.id_number else str(envelope.student.id),
                'profile_picture': profile_picture_url,
                'title': envelope.title,
                'color': envelope.color,
                'pattern': envelope.pattern,
                'class_name': class_name,
                'is_submitted': envelope.is_submitted,
                'status': status_text,
                'created_at': local_time.isoformat(),
                'submitted_at': submitted_time.isoformat() if envelope.is_submitted else None,
                'date_created': local_time.strftime('%b %d, %Y'),
                'time_created': local_time.strftime('%I:%M %p'),
                'activity_count': activity_count,
                'total_activities': total_activities,
                'compiled_count': compiled_count
            })

        print(f"✅ Found {len(envelope_list)} portfolio envelopes for {class_name} (filtered by student's classroom assignment)")

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

        # Verify student has a classroom assigned
        if not student.classroom:
            print(f"⚠️ Student {student.username} has no assigned classroom")
            return Response({
                'error': 'Student has no assigned classroom',
                'all_activities': [],
                'submitted_activities': [],
                'missing_activities': [],
                'total_count': 0,
                'submitted_count': 0,
                'missing_count': 0,
                'student_name': student.username
            }, status=status.HTTP_200_OK)

        print(f"✅ Student {student.username} is in classroom: {student.classroom.name} (ID: {student.classroom.id})")

        # Get all portfolio folders for this class that belong to the logged-in teacher AND the student's classroom
        folders = PortfolioFolder.objects.filter(
            class_name=class_name,
            teacher=request.user,  # IMPORTANT: Only get folders created by this teacher
            classroom=student.classroom  # IMPORTANT: Only get folders for the student's classroom
        )

        print(f"📁 Found {folders.count()} folders for teacher {request.user.username} in classroom {student.classroom.name}")

        activity_list = []
        for folder in folders:
            # Get all activities in this folder
            activities = PortfolioActivity.objects.filter(folder=folder).order_by('created_at')

            for activity in activities:
                # Get the LATEST SCORED or COMPILED submission for this activity
                from django.db.models import Q
                submission = StudentSubmission.objects.filter(
                    activity=activity,
                    student=student,
                    is_active=True
                ).filter(
                    Q(status='scored') | Q(compiled=True) | Q(is_compilation=True)
                ).order_by('-submitted_at').first()  # Get the latest submission

                # Get submission file path with better error handling
                submission_file = None
                if submission:
                    try:
                        # Try file field first (for uploaded files) - check if file exists
                        if submission.file:
                            try:
                                if hasattr(submission.file, 'path') and os.path.exists(submission.file.path):
                                    # File exists, build full URL
                                    submission_file = request.build_absolute_uri(submission.file.url)
                                    print(f"   📎 Using file.url: {submission_file[:100]}...")
                                else:
                                    print(f"   ⚠️ File field exists but file not found on disk")
                            except Exception as e:
                                print(f"   ⚠️ Error checking file: {str(e)}")

                        # Fallback to file_path (for base64 or legacy data)
                        if not submission_file and submission.file_path:
                            submission_file = submission.file_path
                            print(f"   📎 Using file_path (base64): {submission_file[:100]}...")

                        if not submission_file:
                            print(f"   ⚠️ No file found for submission {submission.id}")
                    except Exception as file_error:
                        print(f"⚠️ Error getting submission file for activity {activity.id}: {file_error}")
                        submission_file = None

                # Convert submission time to local timezone if exists
                local_submitted_time = None
                submitted_date_str = None
                submitted_time_str = None
                submission_date_iso = None

                if submission and submission.submitted_at:
                    try:
                        import pytz
                        manila_tz = pytz.timezone('Asia/Manila')
                        
                        # Convert to Manila timezone
                        if timezone.is_naive(submission.submitted_at):
                            aware_time = timezone.make_aware(submission.submitted_at, timezone=pytz.UTC)
                            local_submitted_time = aware_time.astimezone(manila_tz)
                        else:
                            local_submitted_time = submission.submitted_at.astimezone(manila_tz)
                        
                        submission_date_iso = local_submitted_time.isoformat()
                        submitted_date_str = local_submitted_time.strftime('%b %d, %Y')
                        submitted_time_str = local_submitted_time.strftime('%I:%M %p')
                    except Exception as date_error:
                        print(f"⚠️ Error formatting submission date: {date_error}")

                # Get submission files (multiple files support)
                submission_files = []
                if submission:
                    try:
                        from .models import SubmissionFile
                        files = SubmissionFile.objects.filter(submission=submission)
                        for f in files:
                            # Build proper file URL - use absolute URL for file field, or file_path for base64
                            file_url = None
                            if f.file:
                                try:
                                    file_url = request.build_absolute_uri(f.file.url)
                                except:
                                    file_url = f.file_path
                            else:
                                file_url = f.file_path
                            
                            submission_files.append({
                                'id': f.id,
                                'path': file_url,
                                'type': f.file_type,
                                'name': f.file_name or f'file_{f.id}'
                            })
                        print(f"   📁 Found {len(submission_files)} files for submission {submission.id}")
                        
                        # Fallback: if no files in SubmissionFile table, use the single file from submission
                        if len(submission_files) == 0 and submission_file:
                            file_type = 'image' if (submission_file.startswith('data:image') or submission_file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))) else 'file'
                            submission_files.append({
                                'id': 0,
                                'path': submission_file,
                                'type': file_type,
                                'name': 'submission_file'
                            })
                            print(f"   📁 Added fallback single file to submission_files")
                    except Exception as files_error:
                        print(f"⚠️ Error getting submission files: {files_error}")

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
                    'submission_files': submission_files,  # Multiple files support
                    'submission_caption': submission.caption if submission else None,
                    'submission_score': submission.score if submission else None,
                    'max_score': None,  # Will be calculated below
                    'submission_feedback': submission.feedback if submission else None,
                    'submission_status': 'scored' if submission else 'missing',  # Default status
                    'folder_name': folder.name,
                    'is_scored': submission is not None,  # Add flag for scored status
                    'is_compilation': submission.is_compilation if submission and hasattr(submission, 'is_compilation') else False,
                    'is_late': submission.is_late if submission and hasattr(submission, 'is_late') else False,
                    'resubmit_count': submission.resubmit_count if submission and hasattr(submission, 'resubmit_count') else 0,
                    'scored_at': submission.scored_at.isoformat() if submission and hasattr(submission, 'scored_at') and submission.scored_at else None
                }

                # Calculate max_score from scoring_criteria
                try:
                    import json
                    if activity.scoring_criteria:
                        criteria = json.loads(activity.scoring_criteria) if isinstance(activity.scoring_criteria, str) else activity.scoring_criteria
                        if criteria and isinstance(criteria, list):
                            activity_data['max_score'] = sum(int(c.get('maxScore', 0)) for c in criteria)
                except Exception as score_error:
                    print(f"⚠️ Error calculating max_score: {score_error}")

                # Determine proper status
                if submission:
                    is_compilation = submission.compiled if hasattr(submission, 'compiled') else getattr(submission, 'is_compilation', False)
                    is_resubmitted = submission.resubmit_count > 0 if hasattr(submission, 'resubmit_count') else False
                    is_late = submission.is_late if hasattr(submission, 'is_late') else False
                    has_score = submission.score is not None
                    
                    if is_compilation and not has_score:
                        # Compiled but not yet scored by teacher
                        activity_data['submission_status'] = 'compiled'
                    elif is_compilation and has_score:
                        # Compiled AND scored by teacher - show as scored
                        activity_data['submission_status'] = 'scored'
                    elif is_resubmitted:
                        activity_data['submission_status'] = 'scored_resubmitted'
                    elif is_late:
                        activity_data['submission_status'] = 'scored_late'
                    else:
                        activity_data['submission_status'] = 'scored'

                activity_list.append(activity_data)

        # Separate submitted and missing activities
        submitted_activities = [a for a in activity_list if a['has_submission']]
        missing_activities = [a for a in activity_list if not a['has_submission']]
        
        # Sort submitted activities by submission date (latest first)
        submitted_activities.sort(key=lambda x: x.get('submission_date') or '', reverse=True)

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
            # Get classroom by name and student's classroom
            student_classroom = request.user.classroom
            if student_classroom:
                compilation_request = PortfolioCompilationRequest.objects.filter(
                    classroom=student_classroom,
                    is_active=True
                ).first()
            else:
                compilation_request = None

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


# ============================================
# Student Management API Views
# ============================================

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def student_list_api(request):
    """List students - for teachers, show students based on query parameters or their assigned classroom(s)"""
    if request.method == 'GET':
        # Get query parameters
        grade_level = request.query_params.get('grade_level', '').strip() or None
        section = request.query_params.get('section', '').strip() or None
        search = request.query_params.get('search', '').strip() or None
        
        print(f"📥 student_list_api called - grade_level: {grade_level}, section: {section}, user: {request.user.username}")

        students_data = []
        
        # Filter based on user role
        if request.user.role == 'teacher':
            # If specific grade_level and section are provided, find students for that class
            if grade_level and section:
                # Extract grade number from "Grade 4" format
                extracted_grade = None
                if isinstance(grade_level, str) and 'Grade ' in grade_level:
                    try:
                        parts = grade_level.split('Grade ')
                        if len(parts) > 1:
                            grade_part = parts[1].strip()
                            # Handle "Grade 4" -> 4
                            if grade_part.isdigit():
                                extracted_grade = int(grade_part)
                    except (IndexError, ValueError):
                        pass
                elif str(grade_level).isdigit():
                    extracted_grade = int(grade_level)
                
                print(f"🔢 Extracted grade: {extracted_grade}")
                
                if extracted_grade is not None:
                    # First, try to get students from User model via Classroom (these are actual login accounts)
                    # IMPORTANT: Prioritize non-archived classrooms from the current school year
                    from .models import SchoolYear
                    current_sy = SchoolYear.get_current_for_teacher(request.user)
                    
                    # Try to find classroom in current school year first
                    target_classroom = None
                    if current_sy:
                        target_classroom = Classroom.objects.filter(
                            grade_level=extracted_grade,
                            section=section,
                            school_year=current_sy.name,
                            is_archived=False
                        ).first()
                        print(f"🔍 Looking for classroom in current school year: {current_sy.name}")
                    
                    # Fallback: try any non-archived classroom
                    if not target_classroom:
                        target_classroom = Classroom.objects.filter(
                            grade_level=extracted_grade,
                            section=section,
                            is_archived=False
                        ).first()
                        print(f"🔍 Fallback: Looking for any non-archived classroom")
                    
                    # Last resort: any classroom with this grade/section
                    if not target_classroom:
                        target_classroom = Classroom.objects.filter(
                            grade_level=extracted_grade,
                            section=section
                        ).first()
                        print(f"🔍 Last resort: Any classroom with grade {extracted_grade} section {section}")
                    
                    if target_classroom:
                        users = User.objects.filter(
                            role='student',
                            classroom=target_classroom
                        ).order_by('last_name', 'first_name')
                        print(f"📚 Found {users.count()} users in classroom: {target_classroom.name} (ID: {target_classroom.id}, School Year: {target_classroom.school_year}, Archived: {target_classroom.is_archived})")
                        
                        for student in users:
                            students_data.append({
                                'id': student.id,
                                'name': f"{student.first_name} {student.last_name}".strip() or student.username,
                                'student_id': student.id_number,
                                'first_name': student.first_name,
                                'last_name': student.last_name,
                                'username': student.username,
                                'email': student.email,
                                'grade_level': student.grade_level,
                                'section': student.section,
                                'classroom': {
                                    'id': target_classroom.id,
                                    'name': target_classroom.name,
                                    'room_number': target_classroom.room_number
                                },
                                'is_active': student.is_active
                            })
                    else:
                        # Fallback: try to get from Student model (comprehensive records)
                        print(f"⚠️ No classroom found for Grade {extracted_grade} - {section}, trying Student model")
                        student_records = Student.objects.filter(
                            grade_level=extracted_grade,
                            section=section,
                            is_active=True
                        ).order_by('last_name', 'first_name')
                        
                        print(f"📚 Found {student_records.count()} students in Student model")
                        
                        for student in student_records:
                            user_account = student.user
                            students_data.append({
                                'id': user_account.id if user_account else student.id,
                                'name': f"{student.first_name} {student.last_name}".strip(),
                                'student_id': student.student_id,
                                'first_name': student.first_name,
                                'last_name': student.last_name,
                                'username': user_account.username if user_account else student.student_id,
                                'email': student.email or (user_account.email if user_account else ''),
                                'grade_level': f"Grade {student.grade_level}",
                                'section': student.section,
                                'classroom': {
                                    'id': None,
                                    'name': f"Grade {student.grade_level} - {student.section}",
                                    'room_number': ''
                                },
                                'is_active': student.is_active
                            })
                else:
                    print(f"⚠️ Could not extract grade number from: {grade_level}")
            else:
                # No specific class requested - get teacher's assigned classrooms
                teacher_classrooms = Classroom.objects.filter(teacher=request.user)

                if teacher_classrooms.exists():
                    users = User.objects.filter(
                        role='student',
                        classroom__in=teacher_classrooms
                    ).order_by('classroom__grade_level', 'classroom__section', 'last_name', 'first_name')
                    
                    for student in users:
                        students_data.append({
                            'id': student.id,
                            'name': f"{student.first_name} {student.last_name}".strip() or student.username,
                            'student_id': student.id_number,
                            'first_name': student.first_name,
                            'last_name': student.last_name,
                            'username': student.username,
                            'email': student.email,
                            'grade_level': student.grade_level,
                            'section': student.section,
                            'classroom': {
                                'id': student.classroom.id,
                                'name': student.classroom.name,
                                'room_number': student.classroom.room_number
                            } if student.classroom else None,
                            'is_active': student.is_active
                        })
                        
        elif request.user.role == 'admin':
            # Admin can see all students
            if grade_level and section:
                extracted_grade = None
                if isinstance(grade_level, str) and 'Grade ' in grade_level:
                    try:
                        parts = grade_level.split('Grade ')
                        if len(parts) > 1 and parts[1].strip().isdigit():
                            extracted_grade = int(parts[1].strip())
                    except (IndexError, ValueError):
                        pass
                elif str(grade_level).isdigit():
                    extracted_grade = int(grade_level)
                
                if extracted_grade is not None:
                    student_records = Student.objects.filter(
                        grade_level=extracted_grade,
                        section=section,
                        is_active=True
                    ).order_by('last_name', 'first_name')
                    
                    for student in student_records:
                        user_account = student.user
                        students_data.append({
                            'id': user_account.id if user_account else student.id,
                            'name': f"{student.first_name} {student.last_name}".strip(),
                            'student_id': student.student_id,
                            'first_name': student.first_name,
                            'last_name': student.last_name,
                            'username': user_account.username if user_account else student.student_id,
                            'email': student.email or (user_account.email if user_account else ''),
                            'grade_level': f"Grade {student.grade_level}",
                            'section': student.section,
                            'classroom': None,
                            'is_active': student.is_active
                        })
            else:
                users = User.objects.filter(role='student').order_by('last_name', 'first_name')
                for student in users:
                    students_data.append({
                        'id': student.id,
                        'name': f"{student.first_name} {student.last_name}".strip() or student.username,
                        'student_id': student.id_number,
                        'first_name': student.first_name,
                        'last_name': student.last_name,
                        'username': student.username,
                        'email': student.email,
                        'grade_level': student.grade_level,
                        'section': student.section,
                        'classroom': {
                            'id': student.classroom.id,
                            'name': student.classroom.name,
                            'room_number': student.classroom.room_number
                        } if student.classroom else None,
                        'is_active': student.is_active
                    })
        else:
            # Students can only see themselves
            student = request.user
            if student.role == 'student':
                students_data.append({
                    'id': student.id,
                    'name': f"{student.first_name} {student.last_name}".strip() or student.username,
                    'student_id': student.id_number,
                    'first_name': student.first_name,
                    'last_name': student.last_name,
                    'username': student.username,
                    'email': student.email,
                    'grade_level': student.grade_level,
                    'section': student.section,
                    'classroom': {
                        'id': student.classroom.id,
                        'name': student.classroom.name,
                        'room_number': student.classroom.room_number
                    } if student.classroom else None,
                    'is_active': student.is_active
                })

        # Apply search filter if provided
        if search:
            search_lower = search.lower()
            students_data = [
                s for s in students_data
                if search_lower in (s.get('student_id') or '').lower()
                or search_lower in (s.get('first_name') or '').lower()
                or search_lower in (s.get('last_name') or '').lower()
                or search_lower in (s.get('username') or '').lower()
                or search_lower in (s.get('email') or '').lower()
            ]

        print(f"📤 Returning {len(students_data)} students")
        return Response({
            'count': len(students_data),
            'students': students_data
        })

    elif request.method == 'POST':
        # Only admin and teachers can create students
        if request.user.role not in ['admin', 'teacher']:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        from .serializer import StudentSerializer
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def student_detail_api(request, pk):
    """Retrieve, update or delete a student"""
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        from .serializer import StudentSerializer
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Only admin and teachers can update folders
        if request.user.role not in ['admin', 'teacher']:
            return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = PortfolioFolderSerializer(folder, data=request.data, partial=True) # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Ensure only the teacher who owns the folder can delete it
        if folder.teacher != request.user:
            return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        folder.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_folder_api(request, folder_id):
    try:
        folder = PortfolioFolder.objects.get(id=folder_id, teacher=request.user)
        if folder.activities.count() > 0:
            return Response({'error': 'Cannot delete a folder that contains activities.'}, status=status.HTTP_400_BAD_REQUEST)

        # Notify students in the class
        classroom = folder.classroom
        if classroom:
            students = classroom.students.all()
            for student in students:
                if student.id != request.user.id:
                    Notification.objects.create(
                        recipient=student,
                        title=f'Folder Dropped: {folder.name}',
                        message=f'Your teacher, {request.user.get_full_name()}, has dropped the folder "{folder.name}".',
                        notification_type='portfolio_deleted'
                    )

        folder.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except PortfolioFolder.DoesNotExist:
        return Response({'error': 'Folder not found or you do not have permission to delete it.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error deleting folder: {e}")
        return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def students_by_grade_section_api(request):
    """Get students by grade level and section"""
    grade_level = request.query_params.get('grade_level')
    section = request.query_params.get('section')

    if not grade_level or not section:
        return Response(
            {'error': 'Both grade_level and section are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    students = Student.objects.filter(
        grade_level=grade_level,
        section=section,
        is_active=True
    ).order_by('last_name', 'first_name')

    from .serializer import StudentListSerializer
    serializer = StudentListSerializer(students, many=True)

    return Response({
        'grade_level': grade_level,
        'section': section,
        'total_students': students.count(),
        'male_count': students.filter(gender='M').count(),
        'female_count': students.filter(gender='F').count(),
        'students': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_statistics_api(request):
    """Get comprehensive student statistics"""
    from django.db.models import Avg, Count

    # Overall statistics
    total_students = Student.objects.count()
    active_students = Student.objects.filter(is_active=True).count()

    # Gender distribution
    gender_stats = Student.objects.values('gender').annotate(count=Count('id'))
    gender_distribution = {stat['gender']: stat['count'] for stat in gender_stats}

    # Grade level distribution
    grade_distribution = []
    for grade in range(1, 7):
        students_in_grade = Student.objects.filter(grade_level=grade)
        grade_data = {
            'grade': grade,
            'total': students_in_grade.count(),
            'section_a': students_in_grade.filter(section='A').count(),
            'section_b': students_in_grade.filter(section='B').count(),
            'male': students_in_grade.filter(gender='M').count(),
            'female': students_in_grade.filter(gender='F').count(),
        }
        grade_distribution.append(grade_data)

    # Academic performance
    performance = Student.objects.aggregate(
        avg_grade=Avg('current_average'),
        avg_attendance=Avg('attendance_percentage')
    )

    # Top performers (top 10)
    top_performers = Student.objects.filter(
        current_average__isnull=False
    ).order_by('-current_average')[:10]

    from .serializer import StudentListSerializer
    top_performers_data = StudentListSerializer(top_performers, many=True).data

    # Students with low attendance (< 80%)
    low_attendance = Student.objects.filter(
        attendance_percentage__lt=80
    ).count()

    return Response({
        'overview': {
            'total_students': total_students,
            'active_students': active_students,
            'inactive_students': total_students - active_students,
        },
        'gender_distribution': gender_distribution,
        'grade_distribution': grade_distribution,
        'academic_performance': {
            'average_grade': round(performance['avg_grade'], 2) if performance['avg_grade'] else 0,
            'average_attendance': round(performance['avg_attendance'], 2) if performance['avg_attendance'] else 0,
            'low_attendance_count': low_attendance,
        },
        'top_performers': top_performers_data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_search_api(request):
    """Advanced search for students"""
    query = request.query_params.get('q', '')

    if not query:
        return Response(
            {'error': 'Search query is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Search in multiple fields
    students = Student.objects.filter(
        Q(student_id__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(email__icontains=query) |
        Q(guardian_name__icontains=query)
    ).order_by('grade_level', 'section', 'last_name')

    from .serializer import StudentListSerializer
    serializer = StudentListSerializer(students, many=True)

    return Response({
        'query': query,
        'count': students.count(),
        'results': serializer.data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_student_grades_api(request, pk):
    """Update student's current average"""
    if request.user.role not in ['admin', 'teacher']:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

    new_average = request.data.get('current_average')
    if new_average is None:
        return Response(
            {'error': 'current_average is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        new_average = float(new_average)
        if new_average < 0 or new_average > 100:
            raise ValueError("Average must be between 0 and 100")
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

    student.current_average = new_average
    student.save()

    from .serializer import StudentSerializer
    serializer = StudentSerializer(student)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_student_attendance_api(request, pk):
    """Update student's attendance percentage"""
    if request.user.role not in ['admin', 'teacher']:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

    new_attendance = request.data.get('attendance_percentage')
    if new_attendance is None:
        return Response(
            {'error': 'attendance_percentage is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        new_attendance = float(new_attendance)
        if new_attendance < 0 or new_attendance > 100:
            raise ValueError("Attendance must be between 0 and 100")
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

    student.attendance_percentage = new_attendance
    student.save()

    from .serializer import StudentSerializer
    serializer = StudentSerializer(student)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_update_section_api(request):
    """Bulk update section for multiple students"""
    if request.user.role not in ['admin', 'teacher']:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    student_ids = request.data.get('student_ids', [])
    new_section = request.data.get('section')

    if not student_ids or not new_section:
        return Response(
            {'error': 'student_ids and section are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if new_section not in ['A', 'B']:
        return Response(
            {'error': 'Section must be either A or B'},
            status=status.HTTP_400_BAD_REQUEST
        )

    updated_count = Student.objects.filter(
        id__in=student_ids
    ).update(section=new_section)

    return Response({
        'message': f'Successfully updated {updated_count} students',
        'updated_count': updated_count
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_students_api(request):
    """Export student data as JSON (can be extended to CSV/Excel)"""
    if request.user.role not in ['admin', 'teacher']:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    # Get filter parameters
    grade_level = request.query_params.get('grade_level')
    section = request.query_params.get('section')

    students = Student.objects.all()

    if grade_level:
        students = students.filter(grade_level=grade_level)
    if section:
        students = students.filter(section=section)

    students = students.order_by('grade_level', 'section', 'last_name', 'first_name')

    from .serializer import StudentSerializer
    serializer = StudentSerializer(students, many=True)

    # Create JSON response with download headers
    response = HttpResponse(
        json.dumps(serializer.data, indent=2),
        content_type='application/json'
    )

    filename = f"students_export_{timezone.now().strftime('%Y%m%d_%H%M%S')}.json"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response


@api_view(['GET'])
def classroom_list_api(request):
    """
    GET: List all classrooms with teacher and student information
    For teachers: 
        - Default: Show their assigned classroom(s)
        - ?all=true: Show ALL classrooms for the current school year (for ManageClass page)
        - ?all=true&include_archived=true: Show ALL classrooms including from archived school years
        - ?school_year=XXXX-XXXX: Filter by specific school year (for archived view mode)
    For students: Show their classroom
    Only shows non-archived classrooms by default
    """
    try:
        # Check if requesting all classrooms (for manage class page)
        show_all = request.query_params.get('all', 'false').lower() == 'true'
        include_archived = request.query_params.get('include_archived', 'false').lower() == 'true'
        school_year_filter = request.query_params.get('school_year', None)
        
        if request.user.role == 'teacher':
            if school_year_filter:
                # Viewing specific school year (archived view mode)
                classrooms = Classroom.objects.filter(
                    teacher=request.user,
                    school_year=school_year_filter
                ).order_by('grade_level', 'section')
                print(f"📚 Loading teacher's classrooms for school year: {school_year_filter}")
            elif show_all:
                if include_archived:
                    # For folder creation: show ALL classrooms from all school years (current + archived)
                    # Get teacher's school years
                    teacher_school_years = SchoolYear.objects.filter(teacher=request.user).values_list('name', flat=True)
                    
                    # Get all classrooms from teacher's school years
                    classrooms = Classroom.objects.filter(
                        school_year__in=teacher_school_years
                    ).order_by('school_year', 'grade_level', 'section')
                    print(f"📚 Loading ALL classrooms from {len(teacher_school_years)} school years")
                else:
                    # For ManageClass page: show ALL non-archived classrooms for the current school year
                    current_sy = SchoolYear.get_current_for_teacher(request.user)
                    
                    if current_sy:
                        # Filter by current school year
                        classrooms = Classroom.objects.filter(
                            is_archived=False,
                            school_year=current_sy.name
                        ).order_by('grade_level', 'section')
                        print(f"📚 Loading classrooms for school year: {current_sy.name}")
                    else:
                        # Fallback: show all non-archived classrooms
                        classrooms = Classroom.objects.filter(
                            is_archived=False
                        ).order_by('grade_level', 'section')
                        print("⚠️ No current school year found, showing all non-archived classrooms")
            else:
                # Default: show only teacher's assigned classrooms (non-archived) from CURRENT school year
                current_sy = SchoolYear.get_current_for_teacher(request.user)
                
                if current_sy:
                    classrooms = Classroom.objects.filter(
                        teacher=request.user, 
                        is_archived=False,
                        school_year=current_sy.name
                    ).order_by('grade_level', 'section')
                    print(f"📚 Loading teacher's classrooms for current school year: {current_sy.name}")
                else:
                    # Fallback: show all non-archived classrooms assigned to teacher
                    classrooms = Classroom.objects.filter(
                        teacher=request.user, 
                        is_archived=False
                    ).order_by('grade_level', 'section')
                    print("⚠️ No current school year, showing all non-archived teacher classrooms")
        elif request.user.role == 'student':
            # Get the student's classroom (only if not archived)
            if request.user.classroom and not request.user.classroom.is_archived:
                classrooms = Classroom.objects.filter(id=request.user.classroom.id, is_archived=False)
            else:
                return Response({
                    'classrooms': [],
                    'message': 'You are not assigned to any classroom yet'
                })
        else:
            # Admin can see all non-archived classrooms
            classrooms = Classroom.objects.filter(is_archived=False)

        classrooms_data = []
        for classroom in classrooms:
            # For archived classrooms, get students from promotion history
            if classroom.is_archived:
                from .models import StudentPromotionHistory
                
                # Get students from promotion history
                promotion_student_ids = StudentPromotionHistory.objects.filter(
                    previous_classroom=classroom
                ).values_list('student_id', flat=True).distinct()
                
                # Also check for students still assigned (shouldn't happen but just in case)
                current_student_ids = User.objects.filter(
                    classroom=classroom, role='student'
                ).values_list('id', flat=True)
                
                all_student_ids = set(promotion_student_ids) | set(current_student_ids)
                students = User.objects.filter(id__in=all_student_ids, role='student').order_by('last_name', 'first_name')
                student_count = students.count()
            else:
                # Get students in this classroom
                students = User.objects.filter(classroom=classroom, role='student').order_by('last_name', 'first_name')
                student_count = students.count()

            # Get ALL teachers who have folders in this classroom (including via ManageClass)
            teachers_with_subjects = []
            classroom_folders = PortfolioFolder.objects.filter(classroom=classroom).select_related('teacher')
            
            # Group folders by teacher
            teacher_subjects = {}
            for folder in classroom_folders:
                if folder.teacher:
                    teacher_id = folder.teacher.id
                    if teacher_id not in teacher_subjects:
                        # Safely get profile picture URL
                        profile_pic_url = None
                        if folder.teacher.profile_picture:
                            try:
                                profile_pic_url = request.build_absolute_uri(folder.teacher.profile_picture.url)
                            except (ValueError, AttributeError):
                                profile_pic_url = None
                        
                        teacher_subjects[teacher_id] = {
                            'id': folder.teacher.id,
                            'name': f"{folder.teacher.first_name} {folder.teacher.last_name}".strip() or folder.teacher.username,
                            'email': folder.teacher.email,
                            'profile_picture': profile_pic_url,
                            'subjects': []
                        }
                    teacher_subjects[teacher_id]['subjects'].append(folder.name)
            
            # Convert to list
            teachers_with_subjects = list(teacher_subjects.values())
            
            # If assigned teacher has no folders, still include them
            if classroom.teacher and classroom.teacher.id not in teacher_subjects:
                profile_pic_url = None
                if classroom.teacher.profile_picture:
                    try:
                        profile_pic_url = request.build_absolute_uri(classroom.teacher.profile_picture.url)
                    except (ValueError, AttributeError):
                        profile_pic_url = None
                
                teachers_with_subjects.insert(0, {
                    'id': classroom.teacher.id,
                    'name': f"{classroom.teacher.first_name} {classroom.teacher.last_name}".strip() or classroom.teacher.username,
                    'email': classroom.teacher.email,
                    'profile_picture': profile_pic_url,
                    'subjects': [],
                    'is_assigned': True
                })
            else:
                # Mark the assigned teacher
                for t in teachers_with_subjects:
                    if classroom.teacher and t['id'] == classroom.teacher.id:
                        t['is_assigned'] = True
                        break

            classroom_data = {
                'id': classroom.id,
                'name': classroom.name,
                'grade_level': classroom.grade_level,
                'section': classroom.section,
                'room_number': classroom.room_number,
                'capacity': classroom.capacity,
                'school_year': classroom.school_year,
                'class_code': classroom.class_code,  # Class code for student enrollment
                'is_archived': classroom.is_archived,
                'teacher': {
                    'id': classroom.teacher.id,
                    'name': f"{classroom.teacher.first_name} {classroom.teacher.last_name}".strip() or classroom.teacher.username,
                    'email': classroom.teacher.email,
                    'department': classroom.teacher.department,
                    'profile_picture': request.build_absolute_uri(classroom.teacher.profile_picture.url) if classroom.teacher.profile_picture else None
                } if classroom.teacher else None,
                'teachers': teachers_with_subjects,  # All teachers with their subjects
                'student_count': student_count,
                'historical_student_count': student_count if classroom.is_archived else 0,
                'is_full': student_count >= classroom.capacity,
                'students': [
                    {
                        'id': student.id,
                        'name': f"{student.first_name} {student.last_name}".strip() or student.username,
                        'email': student.email,
                        'id_number': student.id_number,
                        'profile_picture': request.build_absolute_uri(student.profile_picture.url) if student.profile_picture else None,
                        'is_historical': classroom.is_archived
                    } for student in students
                ]
            }
            classrooms_data.append(classroom_data)

        return Response({
            'classrooms': classrooms_data,
            'total': len(classrooms_data)
        })

    except Exception as e:
        print(f"Error fetching classrooms: {str(e)}")
        return Response({
            'error': 'Failed to fetch classrooms',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def classroom_detail_api(request, classroom_id):
    """
    GET: Get detailed information about a specific classroom
    For archived classrooms, returns students from promotion history and classroom history
    """
    try:
        classroom = Classroom.objects.get(id=classroom_id)

        # Check permissions
        if request.user.role == 'teacher':
            # Allow if teacher is assigned to this classroom OR has folders in this classroom
            is_assigned = classroom.teacher == request.user
            has_folders = PortfolioFolder.objects.filter(teacher=request.user, classroom=classroom).exists()
            
            if not is_assigned and not has_folders:
                return Response({
                    'error': 'You do not have permission to view this classroom'
                }, status=status.HTTP_403_FORBIDDEN)

        if request.user.role == 'student':
            # Check if student is currently in this classroom
            is_current_student = request.user.classroom == classroom
            
            # Check if student was previously in this classroom via teacher promotion
            from .models import StudentPromotionHistory, StudentClassroomHistory
            was_promoted_from = StudentPromotionHistory.objects.filter(
                student=request.user,
                previous_classroom=classroom
            ).exists()
            
            # Check if student archived this classroom themselves
            was_student_archived = StudentClassroomHistory.objects.filter(
                student=request.user,
                classroom=classroom
            ).exists()
            
            if not is_current_student and not was_promoted_from and not was_student_archived:
                return Response({
                    'error': 'You do not have permission to view this classroom'
                }, status=status.HTTP_403_FORBIDDEN)

        # Get students from multiple sources to ensure complete history
        # This handles both archived classrooms AND students viewing their archived school year
        students_data = []
        from .models import StudentPromotionHistory, StudentClassroomHistory
        
        # Collect student IDs from ALL sources
        student_ids = set()
        
        # 1. Get students currently assigned to this classroom
        current_students = User.objects.filter(classroom=classroom, role='student')
        student_ids.update(current_students.values_list('id', flat=True))
        print(f"📚 Found {current_students.count()} currently assigned students")
        
        # 2. Get students from promotion history (teacher-initiated promotions)
        promotion_records = StudentPromotionHistory.objects.filter(
            previous_classroom=classroom
        ).select_related('student')
        student_ids.update(promotion_records.values_list('student_id', flat=True))
        print(f"📚 Found {promotion_records.count()} students from promotion history")
        
        # 3. Get students from classroom history (student-initiated archiving)
        classroom_history_records = StudentClassroomHistory.objects.filter(
            classroom=classroom
        )
        student_ids.update(classroom_history_records.values_list('student_id', flat=True))
        print(f"📚 Found {classroom_history_records.count()} students from classroom history")
        
        # 4. Get students from submission history (fallback for any missed students)
        submission_student_ids = StudentSubmission.objects.filter(
            activity__folder__classroom=classroom
        ).values_list('student_id', flat=True).distinct()
        student_ids.update(submission_student_ids)
        print(f"📚 Found {len(submission_student_ids)} students from submission history")
        
        # Get all unique students
        if student_ids:
            students = User.objects.filter(id__in=student_ids, role='student').order_by('last_name', 'first_name')
            print(f"📚 Total unique students for classroom {classroom.name}: {students.count()}")
        else:
            students = User.objects.none()
            print(f"⚠️ No students found for classroom {classroom.name}")
        
        for student in students:
            # Get student's submissions for this classroom's activities
            recent_submissions = StudentSubmission.objects.filter(
                student=student,
                activity__folder__classroom=classroom
            ).order_by('-submitted_at')[:5]
            
            # Safely get profile picture URL
            profile_pic_url = None
            if student.profile_picture:
                try:
                    pic_url = student.profile_picture.url
                    if pic_url and not pic_url.startswith(('http://', 'https://')):
                        profile_pic_url = request.build_absolute_uri(pic_url)
                    else:
                        profile_pic_url = pic_url
                except (ValueError, AttributeError):
                    profile_pic_url = None
            
            # Determine if student is historical (not currently assigned)
            is_historical = student.classroom != classroom
            
            students_data.append({
                'id': student.id,
                'name': f"{student.first_name} {student.last_name}".strip() or student.username,
                'email': student.email,
                'id_number': student.id_number,
                'profile_picture': profile_pic_url,
                'is_historical': is_historical,
                'recent_submissions': [
                    {
                        'id': sub.id,
                        'activity': sub.activity.title if sub.activity else 'Sketch',
                        'submitted_at': sub.submitted_at.isoformat() if sub.submitted_at else None,
                        'status': sub.status,
                        'score': sub.score
                    } for sub in recent_submissions
                ]
            })

        # Safely build assigned teacher data
        teacher_data = None
        if classroom.teacher:
            # Build profile picture URL
            teacher_profile_pic_url = None
            if classroom.teacher.profile_picture:
                try:
                    pic_url = classroom.teacher.profile_picture.url
                    if pic_url and not pic_url.startswith(('http://', 'https://')):
                        teacher_profile_pic_url = request.build_absolute_uri(pic_url)
                    else:
                        teacher_profile_pic_url = pic_url
                except (ValueError, AttributeError):
                    teacher_profile_pic_url = None
            
            teacher_data = {
                'id': classroom.teacher.id,
                'name': f"{classroom.teacher.first_name} {classroom.teacher.last_name}".strip() or classroom.teacher.username,
                'email': classroom.teacher.email,
                'department': getattr(classroom.teacher, 'department', None),
                'phone': getattr(classroom.teacher, 'phone_number', None),
                'profile_picture': teacher_profile_pic_url
            }

        # Get ALL teachers who have folders in this classroom (including via ManageClass)
        # This includes both the assigned teacher and teachers who created folders via ManageClass
        teachers_with_subjects = []
        
        # Get all folders for this classroom
        classroom_folders = PortfolioFolder.objects.filter(classroom=classroom).select_related('teacher')
        
        # Group folders by teacher
        teacher_subjects = {}
        for folder in classroom_folders:
            if folder.teacher:
                teacher_id = folder.teacher.id
                if teacher_id not in teacher_subjects:
                    # Safely get profile picture URL - build absolute URL
                    profile_pic_url = None
                    if folder.teacher.profile_picture:
                        try:
                            pic_url = folder.teacher.profile_picture.url
                            if pic_url and not pic_url.startswith(('http://', 'https://')):
                                profile_pic_url = request.build_absolute_uri(pic_url)
                            else:
                                profile_pic_url = pic_url
                        except (ValueError, AttributeError):
                            profile_pic_url = None
                    
                    teacher_subjects[teacher_id] = {
                        'id': folder.teacher.id,
                        'name': f"{folder.teacher.first_name} {folder.teacher.last_name}".strip() or folder.teacher.username,
                        'email': folder.teacher.email,
                        'profile_picture': profile_pic_url,
                        'subjects': []
                    }
                teacher_subjects[teacher_id]['subjects'].append(folder.name)
        
        # Convert to list
        teachers_with_subjects = list(teacher_subjects.values())
        
        # If assigned teacher has no folders, still include them
        if classroom.teacher and classroom.teacher.id not in teacher_subjects:
            profile_pic_url = None
            if classroom.teacher.profile_picture:
                try:
                    pic_url = classroom.teacher.profile_picture.url
                    if pic_url and not pic_url.startswith(('http://', 'https://')):
                        profile_pic_url = request.build_absolute_uri(pic_url)
                    else:
                        profile_pic_url = pic_url
                except (ValueError, AttributeError):
                    profile_pic_url = None
            
            teachers_with_subjects.insert(0, {
                'id': classroom.teacher.id,
                'name': f"{classroom.teacher.first_name} {classroom.teacher.last_name}".strip() or classroom.teacher.username,
                'email': classroom.teacher.email,
                'profile_picture': profile_pic_url,
                'subjects': [],
                'is_assigned': True
            })
        else:
            # Mark the assigned teacher
            for t in teachers_with_subjects:
                if classroom.teacher and t['id'] == classroom.teacher.id:
                    t['is_assigned'] = True
                    break

        classroom_data = {
            'id': classroom.id,
            'name': classroom.name,
            'grade_level': classroom.grade_level,
            'section': classroom.section,
            'room_number': classroom.room_number,
            'capacity': classroom.capacity,
            'school_year': classroom.school_year,
            'is_archived': classroom.is_archived,
            'teacher': teacher_data,
            'teachers': teachers_with_subjects,  # All teachers with their subjects
            'student_count': len(students_data),
            'historical_student_count': len(students_data) if classroom.is_archived else 0,
            'is_full': len(students_data) >= classroom.capacity,
            'students': students_data,
            'created_at': classroom.created_at.isoformat() if classroom.created_at else None,
            'updated_at': classroom.updated_at.isoformat() if classroom.updated_at else None
        }

        return Response(classroom_data)

    except Classroom.DoesNotExist:
        return Response({
            'error': 'Classroom not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error fetching classroom details: {str(e)}")
        return Response({
            'error': 'Failed to fetch classroom details',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================
# USER SETTINGS API
# ============================================

@api_view(['GET', 'PUT'])
def user_settings_api(request):
    """
    GET: Get user settings
    PUT: Update user settings
    """
    if not request.user.is_authenticated:
        return Response({
            'error': 'Authentication required'
        }, status=status.HTTP_403_FORBIDDEN)

    try:
        from .models import UserSettings

        # Get or create user settings
        settings, created = UserSettings.objects.get_or_create(
            user=request.user,
            defaults={
                'email_notifications': True,
                'push_notifications': True,
                'activity_reminders': True,
                'score_notifications': True,
                'remark_notifications': True,
                'submission_alerts': True,
                'profile_visibility': 'public',
                'show_email': False,
                'show_phone': False,
                'language': 'en',
                'theme': 'light',
                'timezone': 'Asia/Manila',
                'date_format': 'MM/DD/YYYY'
            }
        )

        if created:
            print(f"✅ Created new settings for user: {request.user.username}")

        if request.method == 'GET':
            # Return current settings
            return Response({
                'notifications': {
                    'emailNotifications': settings.email_notifications,
                    'pushNotifications': settings.push_notifications,
                    'submissionAlerts': settings.submission_alerts,
                    'remarkAlerts': settings.remark_notifications,
                    'activityReminders': settings.activity_reminders
                },
                'privacy': {
                    'profileVisibility': settings.profile_visibility,
                    'showEmail': settings.show_email,
                    'showPhone': settings.show_phone
                },
                'preferences': {
                    'language': settings.language,
                    'timezone': settings.timezone,
                    'dateFormat': settings.date_format,
                    'theme': settings.theme
                }
            })

        elif request.method == 'PUT':
            # Update settings
            data = request.data

            # Update notifications
            if 'notifications' in data:
                notif = data['notifications']
                settings.email_notifications = notif.get('emailNotifications', settings.email_notifications)
                settings.push_notifications = notif.get('pushNotifications', settings.push_notifications)
                settings.submission_alerts = notif.get('submissionAlerts', settings.submission_alerts)
                settings.remark_notifications = notif.get('remarkAlerts', settings.remark_notifications)
                settings.activity_reminders = notif.get('activityReminders', settings.activity_reminders)

            # Update privacy
            if 'privacy' in data:
                privacy = data['privacy']
                settings.profile_visibility = privacy.get('profileVisibility', settings.profile_visibility)
                settings.show_email = privacy.get('showEmail', settings.show_email)
                settings.show_phone = privacy.get('showPhone', settings.show_phone)

            # Update preferences
            if 'preferences' in data:
                prefs = data['preferences']
                settings.language = prefs.get('language', settings.language)
                settings.timezone = prefs.get('timezone', settings.timezone)
                settings.date_format = prefs.get('dateFormat', settings.date_format)
                settings.theme = prefs.get('theme', settings.theme)

                print(f"🎨 Updated theme for {request.user.username}: {settings.theme}")

            settings.save()

            # Return updated settings
            return Response({
                'notifications': {
                    'emailNotifications': settings.email_notifications,
                    'pushNotifications': settings.push_notifications,
                    'submissionAlerts': settings.submission_alerts,
                    'remarkAlerts': settings.remark_notifications,
                    'activityReminders': settings.activity_reminders
                },
                'privacy': {
                    'profileVisibility': settings.profile_visibility,
                    'showEmail': settings.show_email,
                    'showPhone': settings.show_phone
                },
                'preferences': {
                    'language': settings.language,
                    'timezone': settings.timezone,
                    'dateFormat': settings.date_format,
                    'theme': settings.theme
                }
            })

    except Exception as e:
        print(f"❌ Error in user settings API: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({
            'error': 'Failed to process settings',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# AI Test Endpoint
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ai_test(request):
    """Test endpoint to verify AI API is working"""
    return Response({'message': 'AI API is working!'}, status=status.HTTP_200_OK)


# AI Question Generation API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_ai_questions(request):
    """Generate questions using OpenAI API based on topic, grade level, and question types"""
    try:
        # Get data
        topic = request.data.get('topic', '')
        grade_level = request.data.get('grade_level', '')
        num_questions = request.data.get('num_questions', 5)
        question_types = request.data.get('question_types', [])
        difficulty = request.data.get('difficulty', 'medium')
        additional_instructions = request.data.get('additional_instructions', '')

        # Convert to int
        try:
            num_questions = int(num_questions)
        except:
            num_questions = 5

        # Validate required fields
        if not topic or not grade_level or not question_types:
            return Response({
                'error': 'Missing required fields'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Try to use OpenAI API, fallback to mock if not configured
        try:
            content = generate_questions_with_openai(topic, grade_level, num_questions, question_types, difficulty, additional_instructions)
        except Exception as openai_error:
            print(f"⚠️ OpenAI API error: {str(openai_error)}, falling back to mock generation")
            content = generate_realistic_questions(topic, grade_level, num_questions, question_types, difficulty)

        return Response({
            'content': content,
            'topic': topic,
            'grade_level': grade_level,
            'num_questions': num_questions,
            'question_types': question_types
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def generate_questions_with_openai(topic, grade_level, num_questions, question_types, difficulty, additional_instructions):
    """Generate questions using OpenAI API"""
    import os
    from openai import OpenAI

    # Get API key from environment
    api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        raise ValueError("OPENAI_API_KEY not configured in environment")

    client = OpenAI(api_key=api_key)

    # Build question types string
    types_str = ", ".join(question_types)

    # Build the prompt
    prompt = f"""Generate exactly {num_questions} educational questions about "{topic}" for {grade_level} students.

Difficulty Level: {difficulty}
Question Types: {types_str}

Requirements:
1. Generate EXACTLY {num_questions} questions
2. Distribute the questions evenly among the selected types: {types_str}
3. Make questions appropriate for {grade_level} level
4. Ensure {difficulty} difficulty level
5. Include correct answers and explanations
6. Format each question clearly with type label

{f"Additional Instructions: {additional_instructions}" if additional_instructions else ""}

Format the output as follows for each question:
**Question [number]: [Type]**
[Question text]

[For Multiple Choice: A) option, B) option, C) option, D) option]
[For True/False: Statement]
[For Short Answer: Question prompt]
[For Essay: Essay prompt with key points]

**Answer:** [Correct answer]
**Explanation:** [Brief explanation]

---

Generate the questions now:"""

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an expert educational content creator. Generate high-quality, engaging questions that are appropriate for the specified grade level and difficulty."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=2000
    )

    # Extract content
    content = response.choices[0].message.content

    print(f"✅ Generated {num_questions} questions using OpenAI API")
    return content


def generate_realistic_questions(topic, grade_level, num_questions, question_types, difficulty):
    """Generate realistic questions based on selected types"""

    questions = []
    question_count = 0
    type_list = list(question_types) if question_types else []

    # Cycle through question types to distribute them evenly
    type_index = 0

    while question_count < num_questions:
        if not type_list:
            break

        q_type = str(type_list[type_index % len(type_list)]).strip().lower()
        type_index += 1
        question_count += 1

        if q_type == 'multiple_choice':
            questions.append(generate_multiple_choice(topic, grade_level, difficulty, question_count))
        elif q_type == 'true_false':
            questions.append(generate_true_false(topic, grade_level, difficulty, question_count))
        elif q_type == 'short_answer':
            questions.append(generate_short_answer(topic, grade_level, difficulty, question_count))
        elif q_type == 'essay':
            questions.append(generate_essay(topic, grade_level, difficulty, question_count))

    return "\n\n---\n\n".join(questions)


def generate_multiple_choice(topic, grade_level, difficulty, question_num):
    """Generate a multiple choice question"""
    return f"""**Question {question_num}: Multiple Choice**

Which of the following best describes {topic}?

A) A fundamental concept that is essential to understanding modern science
B) A theoretical framework with limited practical applications
C) An outdated approach no longer used in contemporary practice
D) A specialized field relevant only to advanced professionals

**Correct Answer: A**
**Explanation:** {topic} is a core concept that forms the foundation for understanding many related topics and has widespread practical applications."""


def generate_true_false(topic, grade_level, difficulty, question_num):
    """Generate a true/false question"""
    statements = [
        f"{topic} is an important concept in {grade_level} education.",
        f"Understanding {topic} requires advanced mathematical knowledge.",
        f"{topic} has practical applications in everyday life.",
        f"{topic} was first introduced in the 21st century."
    ]

    statement = statements[(question_num - 1) % len(statements)]
    answer = "True" if (question_num % 2 == 1) else "False"

    return f"""**Question {question_num}: True/False**

{statement}

**Answer: {answer}**"""


def generate_short_answer(topic, grade_level, difficulty, question_num):
    """Generate a short answer question"""
    return f"""**Question {question_num}: Short Answer**

Briefly explain what {topic} is and provide one example of how it is used.

**Sample Answer:** {topic} is a key concept that refers to [definition]. For example, it can be applied in [real-world context] to achieve [specific outcome]."""


def generate_essay(topic, grade_level, difficulty, question_num):
    """Generate an essay question"""
    return f"""**Question {question_num}: Essay**

Write a comprehensive essay about {topic}. Your essay should include:

1. **Introduction** - Define {topic} and explain its significance
2. **Main Points** - Discuss at least 3 key aspects or characteristics
3. **Examples** - Provide real-world examples or case studies
4. **Analysis** - Explain how {topic} relates to broader concepts
5. **Conclusion** - Summarize the importance and implications

**Key Points to Address:**
- The definition and scope of {topic}
- Historical or contextual background
- Current relevance and applications
- Challenges or limitations
- Future implications or developments"""


def generate_mock_questions(topic, grade_level, num_questions, question_types, difficulty):
    """Generate mock questions for demonstration purposes"""

    try:
        print(f"Generating mock questions: topic={topic}, grade={grade_level}, num={num_questions}, types={question_types}")
        questions = []
        question_num = 1

        # Simple difficulty mapping
        difficulty_map = {
            'easy': 'basic',
            'medium': 'intermediate',
            'hard': 'advanced',
            'mixed': 'mixed'
        }
        difficulty_level = difficulty_map.get(difficulty, 'intermediate')

        # Generate questions based on types
        type_list = list(question_types) if question_types else []

        for q_type in type_list:
            if question_num > num_questions:
                break

            q_type = str(q_type).strip().lower()

            if q_type == 'multiple_choice':
                questions.append(f"Question {question_num}: Multiple Choice\n\nAbout {topic} ({grade_level} level, {difficulty_level}):\n\nA) Option 1\nB) Option 2 (Correct)\nC) Option 3\nD) Option 4\n\nAnswer: B\n")
                question_num += 1

            elif q_type == 'true_false':
                questions.append(f"Question {question_num}: True/False\n\n{topic} is important in {grade_level} education.\n\nAnswer: True\n")
                question_num += 1

            elif q_type == 'short_answer':
                questions.append(f"Question {question_num}: Short Answer\n\nExplain {topic} briefly.\n\nSample Answer: {topic} is a key concept in {grade_level} studies.\n")
                question_num += 1

            elif q_type == 'essay':
                questions.append(f"Question {question_num}: Essay\n\nWrite about {topic}.\n\nKey Points:\n- Definition\n- Importance\n- Applications\n- Conclusion\n")
                question_num += 1

        # Fill remaining questions if needed
        while question_num <= num_questions:
            questions.append(f"Question {question_num}: Comprehension\n\nExplain how {topic} applies to {grade_level} level.\n\nAnswer: {topic} is relevant and applicable in various ways.\n")
            question_num += 1

        result = "\n---\n".join(questions[:num_questions])
        print(f"Generated {len(questions)} questions, total length: {len(result)} chars")
        return result

    except Exception as e:
        print(f"Error in generate_mock_questions: {str(e)}")
        import traceback
        traceback.print_exc()
        raise


# ============================================
# EXPORT/DOWNLOAD API ENDPOINTS
# ============================================


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_progress_records_api(request):
    """
    Export student progress records for teachers.
    """
    print(f"🚀 EXPORT API HIT! User: {request.user.username}, Role: {request.user.role}")
    if request.user.role != 'teacher':
        print(f"❌ User {request.user.username} is not a teacher (Role: {request.user.role})")
        return Response({'error': 'Only teachers can export progress records'}, status=status.HTTP_403_FORBIDDEN)

    export_type = request.query_params.get('type', 'all_students')
    classroom_id = request.query_params.get('classroom_id')
    class_name = request.query_params.get('class_name')  # Add class_name parameter
    student_id = request.query_params.get('student_id')
    file_format = request.query_params.get('format', 'csv')  # csv or json

    try:
        # Debug logging
        print(f"📊 Export type: {export_type}, Classroom ID: {classroom_id}, Class name: {class_name}")
        
        # Get teacher's folders first
        folders = PortfolioFolder.objects.filter(teacher=request.user)
        print(f"Total folders for teacher: {folders.count()}")
        
        # Filter by classroom_id if provided
        if classroom_id:
            # Try to get the classroom to find its name
            try:
                classroom_obj = Classroom.objects.get(id=classroom_id)
                print(f"Classroom {classroom_id} name: {classroom_obj.name}, SY: {classroom_obj.school_year}")
                
                # Filter by classroom_id ONLY (not by class_name to avoid cross-school-year issues)
                folders = folders.filter(classroom_id=classroom_id)
                print(f"Folders after classroom filter: {folders.count()}")
            except Classroom.DoesNotExist:
                folders = folders.filter(classroom_id=classroom_id)
                print(f"Folders after classroom_id filter: {folders.count()}")
        # Otherwise filter by class_name if provided
        elif class_name:
            # When filtering by class_name, prioritize current school year
            from .models import SchoolYear
            current_sy = SchoolYear.get_current_for_teacher(request.user)
            
            if current_sy:
                # First try to find folders in current school year
                current_sy_folders = folders.filter(
                    class_name=class_name,
                    classroom__school_year=current_sy.name,
                    classroom__is_archived=False
                )
                if current_sy_folders.exists():
                    folders = current_sy_folders
                    print(f"Folders after class_name filter (current SY): {folders.count()}")
                else:
                    # Fallback to any non-archived classroom
                    folders = folders.filter(
                        class_name=class_name,
                        classroom__is_archived=False
                    )
                    print(f"Folders after class_name filter (non-archived): {folders.count()}")
            else:
                folders = folders.filter(class_name=class_name)
                print(f"Folders after class_name filter: {folders.count()}")
        
        if not folders.exists():
            return Response({'error': 'No portfolio folders found for this class'}, status=status.HTTP_404_NOT_FOUND)

        # Get classrooms from folders
        classroom_ids = folders.exclude(classroom__isnull=True).values_list('classroom_id', flat=True).distinct()
        classrooms = Classroom.objects.filter(id__in=classroom_ids)

        # Get students - either from classrooms or from submissions
        if classrooms.exists():
            students_query = User.objects.filter(
                role='student',
                classroom__in=classrooms
            ).exclude(username='admin').order_by('last_name', 'first_name')
            print(f"Students from classrooms: {students_query.count()}")
        else:
            # Fallback: get students who have submissions in teacher's activities
            activities = PortfolioActivity.objects.filter(folder__in=folders)
            student_ids = StudentSubmission.objects.filter(
                activity__in=activities
            ).values_list('student_id', flat=True).distinct()
            students_query = User.objects.filter(
                id__in=student_ids,
                role='student'
            ).exclude(username='admin').order_by('last_name', 'first_name')
            print(f"Students from submissions: {students_query.count()}")

        if student_id:
            students_query = students_query.filter(id=student_id)

        # Get all activities from teacher's folders ONLY
        # Filter by folders owned by this teacher (already filtered above)
        # Only include published activities for export (students can only see published ones)
        activities = PortfolioActivity.objects.filter(
            folder__in=folders,
            folder__teacher=request.user  # Double-check teacher ownership
        ).select_related('folder')
        print(f"Total activities from teacher's folders: {activities.count()}")
        
        # Check if we have any data to export
        if not students_query.exists():
            return Response({'error': 'No students found in this class. Make sure students are assigned to the classroom.'}, status=status.HTTP_404_NOT_FOUND)
        
        if not activities.exists():
            return Response({'error': 'No activities found in your portfolios for this class.'}, status=status.HTTP_404_NOT_FOUND)

        print(f"Processing {students_query.count()} students and {activities.count()} activities")

        # Build export data
        export_data = []

        for student in students_query:
            student_name = f"{student.first_name} {student.last_name}".strip() or student.username
            student_submissions = StudentSubmission.objects.filter(
                student=student,
                activity__in=activities
            ).select_related('activity', 'activity__folder')

            # Calculate stats
            total_activities = activities.count()
            submitted_count = student_submissions.filter(status__in=['unscored', 'scored']).count()
            scored_count = student_submissions.filter(status='scored').count()
            missing_count = total_activities - submitted_count

            # Calculate average score
            scored_submissions = student_submissions.filter(status='scored')
            total_score = 0
            max_possible = 0
            for sub in scored_submissions:
                if sub.criteria_scores:
                    try:
                        criteria = json.loads(sub.criteria_scores) if isinstance(sub.criteria_scores, str) else sub.criteria_scores
                        for c in criteria:
                            total_score += int(c.get('score', 0))
                            max_possible += int(c.get('maxScore', 0))
                    except:
                        if sub.score:
                            total_score += sub.score
                            max_possible += 10
                elif sub.score:
                    total_score += sub.score
                    max_possible += 10

            avg_score = round((total_score / max_possible * 100), 1) if max_possible > 0 else 0

            if export_type == 'summary':
                export_data.append({
                    'student_id': student.id_number or f'STD{str(student.id).zfill(3)}',
                    'student_name': student_name,
                    'classroom': str(student.classroom) if student.classroom else 'N/A',
                    'total_activities': total_activities,
                    'completed': submitted_count,
                    'scored': scored_count,
                    'missing': missing_count,
                    'average_score': f'{avg_score}%'
                })
            elif export_type == 'scored_only':
                for sub in scored_submissions:
                    score_display = 'N/A'
                    if sub.criteria_scores:
                        try:
                            criteria = json.loads(sub.criteria_scores) if isinstance(sub.criteria_scores, str) else sub.criteria_scores
                            t = sum(int(c.get('score', 0)) for c in criteria)
                            m = sum(int(c.get('maxScore', 0)) for c in criteria)
                            score_display = f'{t}/{m}'
                        except:
                            score_display = f'{sub.score}/10' if sub.score else 'N/A'
                    elif sub.score:
                        score_display = f'{sub.score}/10'

                    export_data.append({
                        'student_id': student.id_number or f'STD{str(student.id).zfill(3)}',
                        'student_name': student_name,
                        'folder': sub.activity.folder.name if sub.activity and sub.activity.folder else 'N/A',
                        'activity': sub.activity.title if sub.activity else 'N/A',
                        'activity_type': sub.activity.activity_type if sub.activity else 'N/A',
                        'score': score_display,
                        'submitted_at': sub.submitted_at.strftime('%Y-%m-%d %H:%M') if sub.submitted_at else 'N/A',
                        'scored_at': sub.scored_at.strftime('%Y-%m-%d %H:%M') if sub.scored_at else 'N/A'
                    })
            elif export_type == 'missing_only':
                submitted_activity_ids = set(student_submissions.values_list('activity_id', flat=True))
                for activity in activities:
                    if activity.id not in submitted_activity_ids:
                        export_data.append({
                            'student_id': student.id_number or f'STD{str(student.id).zfill(3)}',
                            'student_name': student_name,
                            'folder': activity.folder.name,
                            'activity': activity.title,
                            'activity_type': activity.activity_type,
                            'due_date': activity.due_date.strftime('%Y-%m-%d') if activity.due_date else 'N/A',
                            'status': 'Missing' if activity.due_date and timezone.now().date() > activity.due_date else 'Pending'
                        })
            else:  # all_students or single_student
                for activity in activities:
                    submission = student_submissions.filter(activity=activity).first()
                    if submission:
                        score_display = 'N/A'
                        if submission.criteria_scores:
                            try:
                                criteria = json.loads(submission.criteria_scores) if isinstance(submission.criteria_scores, str) else submission.criteria_scores
                                t = sum(int(c.get('score', 0)) for c in criteria)
                                m = sum(int(c.get('maxScore', 0)) for c in criteria)
                                score_display = f'{t}/{m}'
                            except:
                                score_display = f'{submission.score}/10' if submission.score else 'N/A'
                        elif submission.score:
                            score_display = f'{submission.score}/10'

                        export_data.append({
                            'student_id': student.id_number or f'STD{str(student.id).zfill(3)}',
                            'student_name': student_name,
                            'folder': activity.folder.name,
                            'activity': activity.title,
                            'activity_type': activity.activity_type,
                            'due_date': activity.due_date.strftime('%Y-%m-%d') if activity.due_date else 'N/A',
                            'status': 'Scored' if submission.status == 'scored' else 'Submitted',
                            'score': score_display,
                            'submitted_at': submission.submitted_at.strftime('%Y-%m-%d %H:%M') if submission.submitted_at else 'N/A',
                            'is_late': 'Yes' if submission.is_late else 'No',
                            'resubmit_count': submission.resubmit_count or 0
                        })
                    else:
                        status = 'Missing' if activity.due_date and timezone.now().date() > activity.due_date else 'Pending'
                        export_data.append({
                            'student_id': student.id_number or f'STD{str(student.id).zfill(3)}',
                            'student_name': student_name,
                            'folder': activity.folder.name,
                            'activity': activity.title,
                            'activity_type': activity.activity_type,
                            'due_date': activity.due_date.strftime('%Y-%m-%d') if activity.due_date else 'N/A',
                            'status': status,
                            'score': 'N/A',
                            'submitted_at': 'N/A',
                            'is_late': 'N/A',
                            'resubmit_count': 0
                        })

        # Generate filename
        if classrooms.exists():
            classroom_name = classrooms.first().name.replace(' ', '_')
        else:
            # Use folder name as fallback
            classroom_name = folders.first().class_name.replace(' ', '_') if folders.exists() else 'All'
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        filename = f"Progress_{classroom_name}_{export_type}_{timestamp}"

        if file_format == 'json':
            response = HttpResponse(
                json.dumps(export_data, indent=2),
                content_type='application/json'
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}.json"'
        else:  # CSV
            if not export_data:
                error_messages = {
                    'scored_only': 'No scored submissions found. Try "All Students" or "Summary" export instead.',
                    'missing_only': 'No missing activities found - all students have submitted!',
                    'summary': 'No student data available for this class.',
                    'all_students': 'No student records found for this class.'
                }
                print(f"No data to export for type: {export_type}")
                return Response({'error': error_messages.get(export_type, 'No data to export')}, status=status.HTTP_404_NOT_FOUND)

            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=export_data[0].keys())
            writer.writeheader()
            writer.writerows(export_data)

            response = HttpResponse(output.getvalue(), content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

        return response

    except Exception as e:
        print(f"Export error: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_activity_results_api(request, activity_id):
    """
    Export activity-specific results for teachers.
    Supports multiple export types:
    - submitted: Only submitted students
    - not_submitted: Only students who haven't submitted
    - scores_only: Just scores
    - complete: Full activity report with timestamps and remarks
    """
    if request.user.role != 'teacher':
        return Response({'error': 'Only teachers can export activity results'}, status=status.HTTP_403_FORBIDDEN)

    export_type = request.query_params.get('type', 'complete')
    file_format = request.query_params.get('format', 'csv')

    try:
        activity = PortfolioActivity.objects.select_related('folder', 'folder__classroom').get(id=activity_id)

        # Verify teacher owns this activity
        if activity.folder.teacher != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        classroom = activity.folder.classroom
        
        # Get all students - either from classroom or from class_name
        if classroom:
            all_students = User.objects.filter(
                role='student',
                classroom=classroom
            ).exclude(username='admin').order_by('last_name', 'first_name')
        else:
            # Fallback: get students who have submitted to this activity
            student_ids = StudentSubmission.objects.filter(activity=activity).values_list('student_id', flat=True).distinct()
            all_students = User.objects.filter(
                id__in=student_ids,
                role='student'
            ).exclude(username='admin').order_by('last_name', 'first_name')

        # Get submissions for this activity
        submissions = StudentSubmission.objects.filter(activity=activity).select_related('student')
        submission_map = {sub.student_id: sub for sub in submissions}

        export_data = []

        for student in all_students:
            student_name = f"{student.first_name} {student.last_name}".strip() or student.username
            submission = submission_map.get(student.id)

            if export_type == 'submitted' and not submission:
                continue
            if export_type == 'not_submitted' and submission:
                continue

            if submission:
                score_display = 'N/A'
                if submission.criteria_scores:
                    try:
                        criteria = json.loads(submission.criteria_scores) if isinstance(submission.criteria_scores, str) else submission.criteria_scores
                        t = sum(int(c.get('score', 0)) for c in criteria)
                        m = sum(int(c.get('maxScore', 0)) for c in criteria)
                        score_display = f'{t}/{m}'
                    except:
                        score_display = f'{submission.score}/10' if submission.score else 'N/A'
                elif submission.score:
                    score_display = f'{submission.score}/10'

                # Get remarks for this submission
                remarks = Remark.objects.filter(submission=submission).order_by('-created_at')
                remarks_text = '; '.join([r.text for r in remarks]) if remarks.exists() else ''

                row = {
                    'student_id': student.id_number or f'STD{str(student.id).zfill(3)}',
                    'student_name': student_name,
                    'status': 'Scored' if submission.status == 'scored' else 'Submitted',
                    'score': score_display,
                    'submitted_at': submission.submitted_at.strftime('%Y-%m-%d %H:%M') if submission.submitted_at else 'N/A',
                }

                if export_type == 'complete':
                    row.update({
                        'is_late': 'Yes' if submission.is_late else 'No',
                        'resubmit_count': submission.resubmit_count or 0,
                        'scored_at': submission.scored_at.strftime('%Y-%m-%d %H:%M') if submission.scored_at else 'N/A',
                        'feedback': submission.feedback or '',
                        'remarks': remarks_text
                    })

                if export_type != 'scores_only':
                    export_data.append(row)
                else:
                    export_data.append({
                        'student_id': student.id_number or f'STD{str(student.id).zfill(3)}',
                        'student_name': student_name,
                        'score': score_display
                    })
            else:
                # Not submitted
                status = 'Missing' if activity.due_date and timezone.now().date() > activity.due_date else 'Pending'
                row = {
                    'student_id': student.id_number or f'STD{str(student.id).zfill(3)}',
                    'student_name': student_name,
                    'status': status,
                    'score': 'N/A',
                    'submitted_at': 'N/A',
                }

                if export_type == 'complete':
                    row.update({
                        'is_late': 'N/A',
                        'resubmit_count': 0,
                        'scored_at': 'N/A',
                        'feedback': '',
                        'remarks': ''
                    })

                if export_type not in ['submitted', 'scores_only']:
                    export_data.append(row)

        # Generate filename
        activity_name = activity.title.replace(' ', '_')[:30]
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        filename = f"Activity_{activity_name}_{export_type}_{timestamp}"

        if file_format == 'json':
            response = HttpResponse(
                json.dumps({
                    'activity': {
                        'title': activity.title,
                        'type': activity.activity_type,
                        'folder': activity.folder.name,
                        'due_date': activity.due_date.strftime('%Y-%m-%d') if activity.due_date else None
                    },
                    'data': export_data
                }, indent=2),
                content_type='application/json'
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}.json"'
        else:  # CSV
            if not export_data:
                return Response({'error': 'No data to export'}, status=status.HTTP_404_NOT_FOUND)

            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=export_data[0].keys())
            writer.writeheader()
            writer.writerows(export_data)

            response = HttpResponse(output.getvalue(), content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

        return response

    except PortfolioActivity.DoesNotExist:
        return Response({'error': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Export error: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_student_record_api(request, student_id):
    """
    Export individual student's complete record.
    Includes all activities, scores, missing submissions, and teacher remarks.
    """
    if request.user.role != 'teacher':
        return Response({'error': 'Only teachers can export student records'}, status=status.HTTP_403_FORBIDDEN)

    file_format = request.query_params.get('format', 'csv')

    try:
        student = User.objects.get(id=student_id, role='student')
        student_name = f"{student.first_name} {student.last_name}".strip() or student.username

        # Verify teacher has access to this student's classroom
        if student.classroom and student.classroom.teacher != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        # Get all activities from teacher's folders in student's classroom
        folders = PortfolioFolder.objects.filter(teacher=request.user)
        if student.classroom:
            folders = folders.filter(classroom=student.classroom)

        activities = PortfolioActivity.objects.filter(folder__in=folders, is_published=True)

        # Get student's submissions
        submissions = StudentSubmission.objects.filter(
            student=student,
            activity__in=activities
        ).select_related('activity', 'activity__folder')
        submission_map = {sub.activity_id: sub for sub in submissions}

        export_data = []

        for activity in activities:
            submission = submission_map.get(activity.id)

            if submission:
                score_display = 'N/A'
                if submission.criteria_scores:
                    try:
                        criteria = json.loads(submission.criteria_scores) if isinstance(submission.criteria_scores, str) else submission.criteria_scores
                        t = sum(int(c.get('score', 0)) for c in criteria)
                        m = sum(int(c.get('maxScore', 0)) for c in criteria)
                        score_display = f'{t}/{m}'
                    except:
                        score_display = f'{submission.score}/10' if submission.score else 'N/A'
                elif submission.score:
                    score_display = f'{submission.score}/10'

                # Get remarks
                remarks = Remark.objects.filter(submission=submission).order_by('-created_at')
                remarks_text = '; '.join([r.text for r in remarks]) if remarks.exists() else ''

                export_data.append({
                    'folder': activity.folder.name,
                    'activity': activity.title,
                    'activity_type': activity.activity_type,
                    'due_date': activity.due_date.strftime('%Y-%m-%d') if activity.due_date else 'N/A',
                    'status': 'Scored' if submission.status == 'scored' else 'Submitted',
                    'score': score_display,
                    'submitted_at': submission.submitted_at.strftime('%Y-%m-%d %H:%M') if submission.submitted_at else 'N/A',
                    'is_late': 'Yes' if submission.is_late else 'No',
                    'resubmit_count': submission.resubmit_count or 0,
                    'feedback': submission.feedback or '',
                    'remarks': remarks_text
                })
            else:
                status = 'Missing' if activity.due_date and timezone.now().date() > activity.due_date else 'Pending'
                export_data.append({
                    'folder': activity.folder.name,
                    'activity': activity.title,
                    'activity_type': activity.activity_type,
                    'due_date': activity.due_date.strftime('%Y-%m-%d') if activity.due_date else 'N/A',
                    'status': status,
                    'score': 'N/A',
                    'submitted_at': 'N/A',
                    'is_late': 'N/A',
                    'resubmit_count': 0,
                    'feedback': '',
                    'remarks': ''
                })

        # Generate filename
        student_name_clean = student_name.replace(' ', '_')[:20]
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        filename = f"Student_{student_name_clean}_Record_{timestamp}"

        if file_format == 'json':
            response = HttpResponse(
                json.dumps({
                    'student': {
                        'id': student.id_number or f'STD{str(student.id).zfill(3)}',
                        'name': student_name,
                        'email': student.email,
                        'classroom': str(student.classroom) if student.classroom else 'N/A'
                    },
                    'records': export_data
                }, indent=2),
                content_type='application/json'
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}.json"'
        else:  # CSV
            if not export_data:
                return Response({'error': 'No data to export'}, status=status.HTTP_404_NOT_FOUND)

            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=export_data[0].keys())
            writer.writeheader()
            writer.writerows(export_data)

            response = HttpResponse(output.getvalue(), content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

        return response

    except User.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Export error: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================
# SCHOOL YEAR MANAGEMENT API
# ============================================

from .models import SchoolYear

@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def school_year_api(request):
    """
    GET: List all school years for the current teacher
    POST: Create a new school year (teacher only)
    """
    if request.method == 'GET':
        try:
            # Filter by current teacher
            if request.user.role == 'teacher':
                school_years = SchoolYear.objects.filter(teacher=request.user).order_by('-start_date')
            else:
                school_years = SchoolYear.objects.none()
            
            data = []
            for sy in school_years:
                # Count classrooms and students for this school year (teacher's classrooms only)
                classrooms = Classroom.objects.filter(school_year=sy.name, teacher=request.user)
                student_count = User.objects.filter(
                    role='student',
                    classroom__in=classrooms
                ).count()
                
                data.append({
                    'id': sy.id,
                    'name': sy.name,
                    'start_date': sy.start_date.isoformat() if sy.start_date else None,
                    'end_date': sy.end_date.isoformat() if sy.end_date else None,
                    'is_current': sy.is_current,
                    'is_archived': sy.is_archived,
                    'promotion_done': sy.promotion_done,
                    'archived_at': sy.archived_at.isoformat() if sy.archived_at else None,
                    'classroom_count': classrooms.count(),
                    'student_count': student_count,
                    'created_at': sy.created_at.isoformat() if sy.created_at else None
                })
            
            current = next((sy for sy in data if sy['is_current'] and not sy['is_archived']), None)
            
            return Response({
                'school_years': data,
                'current': current
            })
        except Exception as e:
            print(f"Error fetching school years: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'POST':
        if request.user.role != 'teacher':
            return Response({'error': 'Only teachers can create school years'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            data = request.data
            name = data.get('name')
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            set_as_current = data.get('set_as_current', False)
            
            if not name or not start_date or not end_date:
                return Response({'error': 'Name, start_date, and end_date are required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if school year already exists for this teacher
            if SchoolYear.objects.filter(name=name, teacher=request.user).exists():
                return Response({'error': f'School year {name} already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            school_year = SchoolYear.objects.create(
                name=name,
                teacher=request.user,
                start_date=start_date,
                end_date=end_date,
                is_current=set_as_current
            )
            
            return Response({
                'id': school_year.id,
                'name': school_year.name,
                'start_date': school_year.start_date.isoformat(),
                'end_date': school_year.end_date.isoformat(),
                'is_current': school_year.is_current,
                'message': 'School year created successfully'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"Error creating school year: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def school_year_detail_api(request, school_year_id):
    """
    GET: Get school year details with classrooms where teacher has folders
    PUT: Update school year
    DELETE: Delete school year (only if no data)
    """
    try:
        school_year = SchoolYear.objects.get(id=school_year_id, teacher=request.user)
    except SchoolYear.DoesNotExist:
        return Response({'error': 'School year not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        from .models import StudentPromotionHistory
        
        # Get classrooms where teacher has folders (not just assigned classrooms)
        # This includes classrooms created via ManageClass by other teachers
        teacher_folders = PortfolioFolder.objects.filter(
            teacher=request.user,
            classroom__school_year=school_year.name
        ).select_related('classroom')
        
        # Get unique classrooms from folders
        classroom_ids = set(f.classroom_id for f in teacher_folders if f.classroom_id)
        classrooms = Classroom.objects.filter(id__in=classroom_ids).order_by('grade_level', 'section')
        
        classrooms_data = []
        for classroom in classrooms:
            # For archived school years, get student count from promotion history
            if school_year.is_archived:
                # The promotion history records previous_classroom
                student_count = StudentPromotionHistory.objects.filter(
                    previous_classroom=classroom
                ).count()
                # Fall back to current students if no promotion history
                if student_count == 0:
                    student_count = User.objects.filter(classroom=classroom, role='student').count()
            else:
                student_count = User.objects.filter(classroom=classroom, role='student').count()
            
            folders = PortfolioFolder.objects.filter(classroom=classroom, teacher=request.user)
            
            classrooms_data.append({
                'id': classroom.id,
                'name': classroom.name,
                'grade_level': classroom.grade_level,
                'section': classroom.section,
                'student_count': student_count,
                'folder_count': folders.count(),
                'teacher': {
                    'id': classroom.teacher.id,
                    'name': f"{classroom.teacher.first_name} {classroom.teacher.last_name}".strip() or classroom.teacher.username
                } if classroom.teacher else None
            })
        
        return Response({
            'id': school_year.id,
            'name': school_year.name,
            'start_date': school_year.start_date.isoformat() if school_year.start_date else None,
            'end_date': school_year.end_date.isoformat() if school_year.end_date else None,
            'is_current': school_year.is_current,
            'is_archived': school_year.is_archived,
            'classrooms': classrooms_data
        })
    
    elif request.method == 'PUT':
        if request.user.role != 'teacher':
            return Response({'error': 'Only teachers can update school years'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            data = request.data
            old_name = school_year.name
            
            if 'name' in data:
                new_name = data['name'].strip()
                if new_name and new_name != old_name:
                    # Check if new name already exists for this teacher
                    if SchoolYear.objects.filter(name=new_name, teacher=request.user).exclude(id=school_year.id).exists():
                        return Response({'error': f'School year "{new_name}" already exists'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    # Update the school year name
                    school_year.name = new_name
                    
                    # Also update all classrooms that reference this school year
                    updated_classrooms = Classroom.objects.filter(school_year=old_name).update(school_year=new_name)
                    print(f"📚 Updated {updated_classrooms} classrooms from school year '{old_name}' to '{new_name}'")
            
            if 'start_date' in data:
                school_year.start_date = data['start_date']
            if 'end_date' in data:
                school_year.end_date = data['end_date']
            if 'is_current' in data:
                school_year.is_current = data['is_current']
            
            school_year.save()
            
            return Response({
                'id': school_year.id,
                'name': school_year.name,
                'is_current': school_year.is_current,
                'message': 'School year updated successfully'
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'DELETE':
        if request.user.role != 'teacher':
            return Response({'error': 'Only teachers can delete school years'}, status=status.HTTP_403_FORBIDDEN)
        
        # Check if school year has any data
        classrooms = Classroom.objects.filter(school_year=school_year.name)
        if classrooms.exists():
            return Response({
                'error': 'Cannot delete school year with existing classrooms. Archive it instead.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        school_year.delete()
        return Response({'message': 'School year deleted successfully'})


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def archive_school_year_api(request, school_year_id):
    """
    Archive a school year - preserves all data but marks it as archived
    """
    if request.user.role != 'teacher':
        return Response({'error': 'Only teachers can archive school years'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        school_year = SchoolYear.objects.get(id=school_year_id)
        
        if school_year.is_archived:
            return Response({'error': 'School year is already archived'}, status=status.HTTP_400_BAD_REQUEST)
        
        if school_year.is_current:
            return Response({'error': 'Cannot archive the current school year. Set another as current first.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Archive the school year
        school_year.is_archived = True
        school_year.archived_at = timezone.now()
        school_year.save()
        
        # Archive all classrooms in this school year
        classrooms = Classroom.objects.filter(school_year=school_year.name)
        classrooms.update(is_archived=True, archived_at=timezone.now())
        
        return Response({
            'message': f'School year {school_year.name} archived successfully',
            'archived_classrooms': classrooms.count()
        })
    except SchoolYear.DoesNotExist:
        return Response({'error': 'School year not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_new_school_year_api(request):
    """
    Start a new school year for a teacher:
    1. Archive current school year (students become unassigned)
    2. Create new classrooms (copy only teacher's assigned classrooms)
    3. Generate class codes for students to join
    
    Rules:
    - Each student can only be in ONE classroom at a time
    - Students from archived classrooms need to join new classrooms via class code
    - No automatic student assignment - students self-enroll using class codes
    """
    if request.user.role != 'teacher':
        return Response({'error': 'Only teachers can start a new school year'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        data = request.data
        new_year_name = data.get('name')  # e.g., "2025-2026"
        copy_classrooms = data.get('copy_classrooms', True)
        
        if not new_year_name:
            return Response({'error': 'School year name is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Normalize the school year name (trim whitespace)
        new_year_name = new_year_name.strip()
        
        print(f"🔍 Starting new school year for teacher: {request.user.username} (ID: {request.user.id})")
        print(f"🔍 New year name: '{new_year_name}' (repr: {repr(new_year_name)})")
        
        # Check if school year already exists for this teacher
        existing_sy = SchoolYear.objects.filter(name=new_year_name, teacher=request.user).first()
        if existing_sy:
            print(f"❌ School year already exists: {existing_sy.name} (ID: {existing_sy.id})")
            return Response({'error': f'School year {new_year_name} already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get current school year for this teacher
        current_sy = SchoolYear.get_current_for_teacher(request.user)
        
        # ============================================
        # STEP 0: Save classrooms to copy BEFORE archiving
        # ============================================
        classrooms_to_copy = []
        if copy_classrooms:
            # Get ALL non-archived classrooms assigned to this teacher
            teacher_classrooms_to_copy = Classroom.objects.filter(
                teacher=request.user,
                is_archived=False
            )
            
            # Save the classroom data before archiving
            for classroom in teacher_classrooms_to_copy:
                classrooms_to_copy.append({
                    'name': classroom.name,
                    'grade_level': classroom.grade_level,
                    'section': classroom.section,
                    'room_number': classroom.room_number,
                    'capacity': classroom.capacity
                })
            print(f"📋 Saved {len(classrooms_to_copy)} classrooms to copy")
            
            # If no non-archived classrooms, try to get from ANY classroom (including archived)
            if not classrooms_to_copy:
                any_classroom = Classroom.objects.filter(teacher=request.user).order_by('-id').first()
                if any_classroom:
                    classrooms_to_copy.append({
                        'name': any_classroom.name,
                        'grade_level': any_classroom.grade_level,
                        'section': any_classroom.section,
                        'room_number': any_classroom.room_number,
                        'capacity': any_classroom.capacity
                    })
                    print(f"📋 Using archived classroom as template: {any_classroom.name}")
        
        # ============================================
        # EARLY CHECK: Ensure we have classrooms to copy BEFORE making any changes
        # ============================================
        if copy_classrooms and not classrooms_to_copy:
            print(f"❌ No classrooms found for teacher {request.user.username}")
            return Response({
                'error': 'No classrooms to copy. Please assign yourself to at least one classroom first.',
                'detail': 'You need to have at least one classroom assigned to you before starting a new school year.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # ============================================
        # STEP 1: Archive current school year and unassign ALL students from teacher's classrooms
        # ============================================
        archived_students_count = 0
        
        # Archive current school year if exists
        if current_sy:
            current_sy.is_current = False
            current_sy.is_archived = True
            current_sy.archived_at = timezone.now()
            current_sy.save()
            print(f"📦 Archived school year: {current_sy.name} for teacher {request.user.username}")
        
        # Get ALL non-archived classrooms assigned to this teacher (regardless of school year)
        teacher_classrooms = Classroom.objects.filter(
            teacher=request.user,
            is_archived=False
        )
        
        # Unassign students from ALL teacher's classrooms (make them available)
        for classroom in teacher_classrooms:
            students_in_classroom = User.objects.filter(
                classroom=classroom,
                role='student'
            ).exclude(username='admin')
            
            archived_students_count += students_in_classroom.count()
            
            # Unassign students - they go back to available pool
            students_in_classroom.update(
                classroom=None,
                grade_level=None,
                section=None
            )
            print(f"📤 Unassigned {students_in_classroom.count()} students from {classroom.name} ({classroom.school_year})")
        
        # Archive ALL non-archived classrooms for this teacher
        teacher_classrooms.update(is_archived=True, archived_at=timezone.now())
        print(f"📦 Archived {teacher_classrooms.count()} classrooms")
        
        # ============================================
        # STEP 2: Create new school year and classrooms
        # ============================================
        new_school_year = SchoolYear.objects.create(
            name=new_year_name,
            teacher=request.user,
            is_current=True
        )
        
        created_classrooms = []
        new_classroom_objects = []
        
        # Create new classrooms from saved data
        for classroom_data in classrooms_to_copy:
            # Check if we already created a classroom with this name in this school year
            if Classroom.objects.filter(
                name=classroom_data['name'],
                school_year=new_year_name,
                teacher=request.user
            ).exists():
                print(f"⚠️ Skipping duplicate classroom: {classroom_data['name']}")
                continue
            
            new_classroom = Classroom.objects.create(
                name=classroom_data['name'],
                grade_level=classroom_data['grade_level'],
                section=classroom_data['section'],
                room_number=classroom_data['room_number'],
                capacity=classroom_data['capacity'],
                school_year=new_year_name,
                school_year_obj=new_school_year,
                teacher=request.user
            )
            created_classrooms.append({
                'id': new_classroom.id,
                'name': new_classroom.name,
                'grade_level': new_classroom.grade_level,
                'section': new_classroom.section
            })
            new_classroom_objects.append(new_classroom)
            print(f"✅ Created new classroom: {new_classroom.name}")
        
        # This should not happen since we check early, but just in case
        if not new_classroom_objects:
            # Delete the school year we just created since no classrooms were made
            new_school_year.delete()
            return Response({
                'error': 'Failed to create classrooms. Please try again.',
                'detail': 'An unexpected error occurred while creating classrooms.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # ============================================
        # STEP 3: Students will join via class code (no automatic assignment)
        # ============================================
        assignment_stats = {
            'total_assigned': 0,
            'classrooms_filled': 0,
            'students_made_available': archived_students_count,
            'classrooms_created': len(new_classroom_objects)
        }
        
        # Get class codes for the new classrooms
        class_codes = []
        for classroom in new_classroom_objects:
            class_codes.append({
                'classroom': classroom.name,
                'class_code': classroom.class_code
            })
            print(f"📋 Class code for {classroom.name}: {classroom.class_code}")
        
        return Response({
            'message': f'School year {new_year_name} started successfully. Share class codes with students to let them join.',
            'school_year': {
                'id': new_school_year.id,
                'name': new_school_year.name,
                'is_current': new_school_year.is_current
            },
            'created_classrooms': created_classrooms,
            'class_codes': class_codes,
            'assignment_stats': assignment_stats
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(f"Error starting new school year: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def undo_promotion_api(request, school_year_id):
    """
    Undo student promotions for a school year - revert students to their original grade/section (per teacher)
    """
    if request.user.role != 'teacher':
        return Response({'error': 'Only teachers can undo promotions'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        from .models import StudentPromotionHistory
        
        school_year = SchoolYear.objects.get(id=school_year_id, teacher=request.user)
        
        if not school_year.promotion_done:
            return Response({'error': 'No promotion was done for this school year'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get all promotion records for this school year by this teacher that haven't been undone
        promotions = StudentPromotionHistory.objects.filter(
            school_year=school_year,
            teacher=request.user,
            is_undone=False
        )
        
        if not promotions.exists():
            return Response({'error': 'No promotions to undo'}, status=status.HTTP_400_BAD_REQUEST)
        
        undo_stats = {
            'reverted': 0,
            'graduated_restored': 0,
            'errors': 0
        }
        
        for promotion in promotions:
            try:
                student = promotion.student
                
                # Restore original classroom assignment
                student.classroom = promotion.previous_classroom
                student.grade_level = str(promotion.previous_grade_level) if promotion.previous_grade_level else None
                student.section = promotion.previous_section
                student.save()
                
                # Mark promotion as undone
                promotion.is_undone = True
                promotion.save()
                
                if promotion.is_graduated:
                    undo_stats['graduated_restored'] += 1
                else:
                    undo_stats['reverted'] += 1
                    
            except Exception as e:
                print(f"Error undoing promotion for student {promotion.student_id}: {str(e)}")
                undo_stats['errors'] += 1
        
        # Mark school year promotion as undone
        school_year.promotion_done = False
        school_year.save()
        
        return Response({
            'message': 'Promotions undone successfully',
            'stats': undo_stats
        })
        
    except SchoolYear.DoesNotExist:
        return Response({'error': 'School year not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error undoing promotions: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def promotion_status_api(request, school_year_id):
    """
    Get promotion status and stats for a school year
    """
    try:
        from .models import StudentPromotionHistory
        
        school_year = SchoolYear.objects.get(id=school_year_id)
        
        promotions = StudentPromotionHistory.objects.filter(school_year=school_year)
        
        stats = {
            'total': promotions.count(),
            'promoted': promotions.filter(is_graduated=False, new_grade_level__isnull=False).count(),
            'graduated': promotions.filter(is_graduated=True).count(),
            'new_grade1': promotions.filter(previous_grade_level__isnull=True, new_grade_level=1).count(),
            'undone': promotions.filter(is_undone=True).count(),
            'promotion_done': school_year.promotion_done
        }
        
        # Get detailed list
        promotion_list = []
        for p in promotions[:50]:  # Limit to 50 for performance
            promotion_list.append({
                'student_id': p.student.id,
                'student_name': f"{p.student.first_name} {p.student.last_name}".strip() or p.student.username,
                'previous_grade': p.previous_grade_level,
                'previous_section': p.previous_section,
                'new_grade': p.new_grade_level,
                'new_section': p.new_section,
                'is_graduated': p.is_graduated,
                'is_undone': p.is_undone
            })
        
        return Response({
            'school_year': school_year.name,
            'stats': stats,
            'promotions': promotion_list
        })
        
    except SchoolYear.DoesNotExist:
        return Response({'error': 'School year not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def archived_school_years_api(request):
    """
    Get all archived school years with their data summary (per teacher)
    Shows classrooms where teacher has folders, not just assigned classrooms
    """
    try:
        print(f"📦 archived_school_years_api called by user: {request.user.username} (ID: {request.user.id})")
        
        # Filter by current teacher
        archived_years = SchoolYear.objects.filter(
            is_archived=True,
            teacher=request.user
        ).order_by('-archived_at')
        
        print(f"📦 Found {archived_years.count()} archived school years for this teacher")
        
        data = []
        for sy in archived_years:
            print(f"📦 Processing school year: {sy.name} (ID: {sy.id})")
            
            # Get classrooms where teacher has folders (not just assigned classrooms)
            # This includes classrooms created via ManageClass
            teacher_folders = PortfolioFolder.objects.filter(
                teacher=request.user,
                classroom__school_year=sy.name,
                classroom__is_archived=True
            ).select_related('classroom')
            
            # Get unique classrooms from folders
            classroom_ids = set(f.classroom_id for f in teacher_folders if f.classroom_id)
            classrooms = Classroom.objects.filter(id__in=classroom_ids)
            
            print(f"📦 Found {classrooms.count()} classrooms with teacher's folders")
            
            # Get summary stats - use promotion history for student count
            from .models import StudentPromotionHistory
            total_students = 0
            total_folders = 0
            total_activities = 0
            total_submissions = 0
            
            for classroom in classrooms:
                # Count students from promotion history (who WERE in this classroom)
                # The promotion history records the previous_classroom, linked to the NEW school year
                # So we need to find promotions where previous_classroom matches
                promotion_count = StudentPromotionHistory.objects.filter(
                    previous_classroom=classroom
                ).count()
                
                if promotion_count > 0:
                    total_students += promotion_count
                else:
                    # Fall back to current students if no promotion history
                    students = User.objects.filter(classroom=classroom, role='student')
                    total_students += students.count()
                
                folders = PortfolioFolder.objects.filter(classroom=classroom, teacher=request.user)
                total_folders += folders.count()
                
                for folder in folders:
                    activities = PortfolioActivity.objects.filter(folder=folder)
                    total_activities += activities.count()
                    
                    for activity in activities:
                        total_submissions += StudentSubmission.objects.filter(activity=activity).count()
            
            data.append({
                'id': sy.id,
                'name': sy.name,
                'start_date': sy.start_date.isoformat() if sy.start_date else None,
                'end_date': sy.end_date.isoformat() if sy.end_date else None,
                'archived_at': sy.archived_at.isoformat() if sy.archived_at else None,
                'stats': {
                    'classrooms': classrooms.count(),
                    'students': total_students,
                    'folders': total_folders,
                    'activities': total_activities,
                    'submissions': total_submissions
                }
            })
        
        print(f"📦 Returning {len(data)} archived school years")
        return Response({'archived_school_years': data})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def archived_classroom_detail_api(request, school_year_id, classroom_id):
    """
    Get detailed view of an archived classroom including all data (per teacher)
    Teacher can view any classroom where they have folders
    Shows students who WERE in this classroom (from promotion history)
    """
    try:
        from .models import StudentPromotionHistory
        
        school_year = SchoolYear.objects.get(id=school_year_id, is_archived=True, teacher=request.user)
        classroom = Classroom.objects.get(id=classroom_id, school_year=school_year.name)
        
        # Verify teacher has folders in this classroom (not just assigned to it)
        has_folders = PortfolioFolder.objects.filter(classroom=classroom, teacher=request.user).exists()
        if not has_folders and classroom.teacher != request.user:
            return Response({'error': 'You do not have access to this classroom'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get students who WERE in this classroom (from promotion history)
        # The promotion history records previous_classroom
        promotion_records = StudentPromotionHistory.objects.filter(
            previous_classroom=classroom
        ).select_related('student')
        
        # If no promotion history, fall back to current students (for non-promoted classrooms)
        if promotion_records.exists():
            students = [p.student for p in promotion_records]
        else:
            students = list(User.objects.filter(classroom=classroom, role='student'))
        
        # Only show teacher's own folders
        folders = PortfolioFolder.objects.filter(classroom=classroom, teacher=request.user)
        
        # Get remarks for students in this classroom (only from this teacher)
        remarks_data = []
        for student in students:
            student_remarks = Remark.objects.filter(student=student, teacher=request.user).order_by('-created_at')
            for remark in student_remarks:
                remarks_data.append({
                    'id': remark.id,
                    'student': f"{student.first_name} {student.last_name}".strip() or student.username,
                    'teacher': f"{remark.teacher.first_name} {remark.teacher.last_name}".strip() or remark.teacher.username,
                    'text': remark.text,
                    'created_at': remark.created_at.isoformat()
                })
        
        # Get notifications for this classroom
        notifications_data = []
        for student in students:
            student_notifications = Notification.objects.filter(recipient=student).order_by('-created_at')[:20]
            for notif in student_notifications:
                notifications_data.append({
                    'id': notif.id,
                    'recipient': f"{student.first_name} {student.last_name}".strip() or student.username,
                    'title': notif.title,
                    'message': notif.message,
                    'type': notif.notification_type,
                    'created_at': notif.created_at.isoformat()
                })
        
        # Build folders with activities and submissions
        folders_data = []
        for folder in folders:
            activities = PortfolioActivity.objects.filter(folder=folder)
            activities_data = []
            
            for activity in activities:
                submissions = StudentSubmission.objects.filter(activity=activity)
                submissions_data = []
                
                for sub in submissions:
                    submissions_data.append({
                        'id': sub.id,
                        'student': f"{sub.student.first_name} {sub.student.last_name}".strip() or sub.student.username,
                        'status': sub.status,
                        'score': sub.score,
                        'submitted_at': sub.submitted_at.isoformat() if sub.submitted_at else None
                    })
                
                activities_data.append({
                    'id': activity.id,
                    'title': activity.title,
                    'type': activity.activity_type,
                    'due_date': activity.due_date.isoformat() if activity.due_date else None,
                    'submissions': submissions_data
                })
            
            folders_data.append({
                'id': folder.id,
                'name': folder.name,
                'activities': activities_data
            })
        
        return Response({
            'school_year': {
                'id': school_year.id,
                'name': school_year.name
            },
            'classroom': {
                'id': classroom.id,
                'name': classroom.name,
                'grade_level': classroom.grade_level,
                'section': classroom.section,
                'teacher': {
                    'id': classroom.teacher.id,
                    'name': f"{classroom.teacher.first_name} {classroom.teacher.last_name}".strip() or classroom.teacher.username
                } if classroom.teacher else None
            },
            'students': [{
                'id': s.id,
                'name': f"{s.first_name} {s.last_name}".strip() or s.username,
                'email': s.email
            } for s in students],
            'folders': folders_data,
            'remarks': remarks_data,
            'notifications': notifications_data
        })
        
    except SchoolYear.DoesNotExist:
        return Response({'error': 'Archived school year not found'}, status=status.HTTP_404_NOT_FOUND)
    except Classroom.DoesNotExist:
        return Response({'error': 'Classroom not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================
# STUDENT SCHOOL YEAR MANAGEMENT APIs
# ============================================

@csrf_exempt
@api_view(['GET'])
def student_school_year_info_api(request):
    """
    Get student's current school year and classroom information
    Uses BOTH StudentClassroomHistory (student-initiated archiving) and 
    StudentPromotionHistory (teacher-initiated promotions) to get archived school year data
    """
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.user.role != 'student':
        return Response({'error': 'Only students can access this endpoint'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        from .models import StudentPromotionHistory, StudentClassroomHistory
        
        student = request.user
        classroom = student.classroom
        
        # Get current classroom info
        current_classroom = None
        if classroom:
            current_classroom = {
                'id': classroom.id,
                'name': classroom.name,
                'grade_level': classroom.grade_level,
                'section': classroom.section,
                'school_year': classroom.school_year,
                'teacher_name': f"{classroom.teacher.first_name} {classroom.teacher.last_name}".strip() if classroom.teacher else None,
                'class_code': classroom.class_code,
            }
        
        # Build history data from BOTH sources
        history_data = []
        seen_classrooms = set()  # Avoid duplicates
        
        # 1. Get history from StudentClassroomHistory (student-initiated archiving via "Archive School Year" button)
        classroom_history = StudentClassroomHistory.objects.filter(
            student=student
        ).select_related('classroom').order_by('-archived_at')
        
        for h in classroom_history:
            classroom_id = h.classroom.id if h.classroom else None
            # Use history record ID as fallback key if classroom was deleted
            history_key = classroom_id or f"history_{h.id}"
            if history_key not in seen_classrooms:
                seen_classrooms.add(history_key)
                history_data.append({
                    'id': h.id,
                    'classroom_id': classroom_id,
                    'classroom_name': h.classroom_name,
                    'grade_level': h.grade_level,
                    'section': h.section,
                    'school_year': h.school_year,
                    'teacher_name': h.teacher_name,
                    'joined_at': h.joined_at.isoformat() if h.joined_at else None,
                    'archived_at': h.archived_at.isoformat() if h.archived_at else None,
                    'source': 'student_archived'  # Track source for debugging
                })
        
        print(f"📚 Found {len(history_data)} records from StudentClassroomHistory for {student.username}")
        
        # 2. Also get history from StudentPromotionHistory (teacher-initiated promotions)
        promotion_history = StudentPromotionHistory.objects.filter(
            student=student,
            previous_classroom__isnull=False,
            is_undone=False
        ).select_related('previous_classroom', 'previous_classroom__teacher').order_by('-promoted_at')
        
        promotion_count = 0
        for h in promotion_history:
            if h.previous_classroom and h.previous_classroom.id not in seen_classrooms:
                seen_classrooms.add(h.previous_classroom.id)
                teacher_name = None
                if h.previous_classroom.teacher:
                    teacher_name = f"{h.previous_classroom.teacher.first_name} {h.previous_classroom.teacher.last_name}".strip()
                
                history_data.append({
                    'id': h.id,
                    'classroom_id': h.previous_classroom.id,
                    'classroom_name': h.previous_classroom.name,
                    'grade_level': h.previous_grade_level or h.previous_classroom.grade_level,
                    'section': h.previous_section or h.previous_classroom.section,
                    'school_year': h.previous_classroom.school_year,
                    'teacher_name': teacher_name,
                    'joined_at': None,  # Not tracked in promotion history
                    'archived_at': h.promoted_at.isoformat() if h.promoted_at else None,
                    'source': 'teacher_promoted'  # Track source for debugging
                })
                promotion_count += 1
        
        print(f"📚 Found {promotion_count} additional records from StudentPromotionHistory for {student.username}")
        
        # Sort by archived_at date (most recent first)
        history_data.sort(key=lambda x: x.get('archived_at') or '', reverse=True)
        
        print(f"✅ Total {len(history_data)} archived school years for student {student.username}")
        
        return Response({
            'has_classroom': classroom is not None,
            'current_classroom': current_classroom,
            'grade_level': student.grade_level,
            'section': student.section,
            'history': history_data,
            'history_count': len(history_data),
        })
        
    except Exception as e:
        import traceback
        print(f"❌ Error getting student school year info: {str(e)}")
        print(traceback.format_exc())
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
def student_archived_submissions_api(request):
    """
    Get student's archived submissions for a specific school year
    """
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.user.role != 'student':
        return Response({'error': 'Only students can access this endpoint'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        student = request.user
        school_year = request.query_params.get('school_year', '')
        classroom_id = request.query_params.get('classroom_id', '')
        
        if not school_year:
            return Response({'error': 'School year is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get submissions for this student from the specified school year
        submissions_query = StudentSubmission.objects.filter(
            student=student
        ).select_related('activity', 'activity__folder', 'activity__folder__classroom')
        
        # Filter by school year through the classroom
        if classroom_id:
            submissions_query = submissions_query.filter(
                activity__folder__classroom_id=classroom_id
            )
        else:
            submissions_query = submissions_query.filter(
                activity__folder__classroom__school_year=school_year
            )
        
        submissions_query = submissions_query.order_by('-submitted_at')
        
        submissions_data = []
        for sub in submissions_query:
            submissions_data.append({
                'id': sub.id,
                'activity_title': sub.activity.title if sub.activity else 'Unknown Activity',
                'folder_name': sub.activity.folder.name if sub.activity and sub.activity.folder else 'Unknown Folder',
                'score': sub.score,
                'status': sub.status,
                'submitted_at': sub.submitted_at.isoformat() if sub.submitted_at else None,
                'graded_at': sub.graded_at.isoformat() if sub.graded_at else None,
            })
        
        print(f"✅ Loaded {len(submissions_data)} archived submissions for student {student.username} (school year: {school_year})")
        
        return Response({
            'submissions': submissions_data,
            'count': len(submissions_data),
            'school_year': school_year,
        })
        
    except Exception as e:
        import traceback
        print(f"❌ Error getting student archived submissions: {str(e)}")
        print(traceback.format_exc())
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def student_archive_school_year_api(request):
    """
    Archive student's current school year (leave current classroom)
    """
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.user.role != 'student':
        return Response({'error': 'Only students can archive their school year'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        from .models import StudentClassroomHistory
        
        student = request.user
        classroom = student.classroom
        
        if not classroom:
            return Response({'error': 'You are not currently enrolled in any classroom'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create history record
        StudentClassroomHistory.objects.create(
            student=student,
            classroom=classroom,
            school_year=classroom.school_year,
            grade_level=classroom.grade_level,
            section=classroom.section,
            classroom_name=classroom.name,
            teacher_name=f"{classroom.teacher.first_name} {classroom.teacher.last_name}".strip() if classroom.teacher else None,
            joined_at=student.date_joined if hasattr(student, 'date_joined') else timezone.now(),
        )
        
        # Store the archived info for response
        archived_classroom_name = classroom.name
        archived_school_year = classroom.school_year
        
        # Clear student's classroom assignment
        student.classroom = None
        student.grade_level = None
        student.section = None
        student.save()
        
        print(f"✅ Student {student.username} archived school year {archived_school_year} from {archived_classroom_name}")
        
        return Response({
            'success': True,
            'message': f'Successfully archived school year {archived_school_year}',
            'archived_classroom': archived_classroom_name,
            'archived_school_year': archived_school_year,
        })
        
    except Exception as e:
        import traceback
        print(f"❌ Error archiving student school year: {str(e)}")
        print(traceback.format_exc())
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def student_join_classroom_api(request):
    """
    Join a classroom using class code
    """
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.user.role != 'student':
        return Response({'error': 'Only students can join classrooms'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        student = request.user
        class_code = request.data.get('class_code', '').strip()
        
        if not class_code:
            return Response({'error': 'Class code is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if student already has a classroom
        if student.classroom:
            return Response({
                'error': 'You are already enrolled in a classroom. Please archive your current school year first.',
                'current_classroom': student.classroom.name
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Find classroom by code
        try:
            classroom = Classroom.objects.get(class_code=class_code)
        except Classroom.DoesNotExist:
            return Response({'error': 'Invalid class code. Please check the code and try again.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if classroom is archived
        if classroom.is_archived:
            return Response({'error': 'This classroom is archived and no longer accepting students.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Assign student to classroom
        student.classroom = classroom
        student.grade_level = str(classroom.grade_level)
        student.section = classroom.section
        student.save()
        
        print(f"✅ Student {student.username} joined classroom {classroom.name} ({classroom.school_year}) using code {class_code}")
        
        return Response({
            'success': True,
            'message': f'Successfully joined {classroom.name}',
            'classroom': {
                'id': classroom.id,
                'name': classroom.name,
                'grade_level': classroom.grade_level,
                'section': classroom.section,
                'school_year': classroom.school_year,
                'teacher_name': f"{classroom.teacher.first_name} {classroom.teacher.last_name}".strip() if classroom.teacher else None,
            }
        })
        
    except Exception as e:
        import traceback
        print(f"❌ Error joining classroom: {str(e)}")
        print(traceback.format_exc())
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
def validate_class_code_api(request):
    """
    Validate a class code and return classroom info (without joining)
    """
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        class_code = request.query_params.get('code', '').strip()
        
        if not class_code:
            return Response({'error': 'Class code is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Find classroom by code
        try:
            classroom = Classroom.objects.get(class_code=class_code)
        except Classroom.DoesNotExist:
            return Response({
                'valid': False,
                'error': 'Invalid class code'
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'valid': True,
            'classroom': {
                'id': classroom.id,
                'name': classroom.name,
                'grade_level': classroom.grade_level,
                'section': classroom.section,
                'school_year': classroom.school_year,
                'teacher_name': f"{classroom.teacher.first_name} {classroom.teacher.last_name}".strip() if classroom.teacher else None,
                'student_count': classroom.student_count,
                'is_archived': classroom.is_archived,
            }
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
