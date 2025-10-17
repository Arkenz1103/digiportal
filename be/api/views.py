from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from inertia import render as inertia_render
from .middleware import teacher_required, student_required
from .models import User, PortfolioFolder, PortfolioActivity, StudentSubmission
from .serializer import PortfolioFolderSerializer, PortfolioActivitySerializer, StudentSubmissionSerializer
import json


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
    return inertia_render(request, 'Teacher/Sprogress')


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
            serializer = PortfolioFolderSerializer(folder)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if not request.user.is_authenticated or request.user.role != 'teacher':
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
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
                'file_path': data.get('file_path', '')
            }
            
            print(f"Activity data: {activity_data}")
            
            serializer = PortfolioActivitySerializer(data=activity_data)
            if serializer.is_valid():
                serializer.save()
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
        else:
            submissions = StudentSubmission.objects.filter(activity=activity, student=request.user)
        
        # Use lightweight serializer for list views (excludes large file_path)
        from .serializer import StudentSubmissionListSerializer
        serializer = StudentSubmissionListSerializer(submissions, many=True)
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
                submission = StudentSubmission.objects.create(
                    activity=activity,
                    student=request.user,
                    caption=data.get('caption', ''),
                    file_path=data.get('file_path', ''),
                    file_type=data.get('file_type', ''),
                    status='unscored',
                    post_to_feed=post_to_feed,
                    approval_status='pending' if post_to_feed else 'approved'
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
        # Get all unscored submissions
        submissions = StudentSubmission.objects.filter(status='unscored').order_by('-submitted_at')
        
        # Use lightweight serializer for list (excludes large file_path)
        from .serializer import StudentSubmissionListSerializer
        serializer = StudentSubmissionListSerializer(submissions, many=True)
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
        # Get all scored submissions
        submissions = StudentSubmission.objects.filter(status='scored').order_by('-scored_at')
        
        # Use lightweight serializer for list (excludes large file_path)
        from .serializer import StudentSubmissionListSerializer
        serializer = StudentSubmissionListSerializer(submissions, many=True)
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
        data = request.data
        action = data.get('action')  # 'approve' or 'reject'
        
        if action == 'approve':
            submission.approval_status = 'approved'
        elif action == 'reject':
            submission.approval_status = 'rejected'
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        
        submission.save()
        
        serializer = StudentSubmissionSerializer(submission)
        return Response(serializer.data)
    except Exception as e:
        print(f"Error approving submission: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
def newsfeed_api(request):
    """
    GET: Get all approved submissions for the newsfeed
    """
    # Temporarily allow unauthenticated access for development
    # TODO: Re-enable authentication in production
    # if not request.user.is_authenticated:
    #     return Response({'error': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Get all approved submissions that are marked for posting to feed
        submissions = StudentSubmission.objects.filter(
            post_to_feed=True,
            approval_status='approved'
        ).select_related('student', 'activity').order_by('-submitted_at')
        
        # Use full serializer for newsfeed (needs images to display)
        serializer = StudentSubmissionSerializer(submissions, many=True)
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
        scores = request.data.get('scores', {})
        feedback = request.data.get('feedback', '')
        total_score = request.data.get('total_score', 0)
        max_score = request.data.get('max_score', 30)
        
        # Update submission with score and feedback
        submission.score = total_score
        submission.feedback = feedback
        submission.status = 'scored'
        submission.scored_at = timezone.now()
        submission.save()
        
        # Create or update detailed score
        detailed_score, created = SubmissionScore.objects.update_or_create(
            submission=submission,
            defaults={
                'creativity_score': scores.get('creativity', 0),
                'creativity_max': scores.get('creativity_max', 10),
                'technical_skill_score': scores.get('technical_skill', 0),
                'technical_skill_max': scores.get('technical_skill_max', 10),
                'requirements_score': scores.get('requirements', 0),
                'requirements_max': scores.get('requirements_max', 10),
                'total_score': total_score,
                'max_score': max_score,
                'scored_by': request.user if request.user.is_authenticated else None
            }
        )
        
        serializer = StudentSubmissionSerializer(submission)
        return Response({
            'message': 'Submission scored successfully',
            'submission': serializer.data,
            'detailed_score': {
                'creativity': f"{detailed_score.creativity_score}/{detailed_score.creativity_max}",
                'technical_skill': f"{detailed_score.technical_skill_score}/{detailed_score.technical_skill_max}",
                'requirements': f"{detailed_score.requirements_score}/{detailed_score.requirements_max}",
                'total': f"{detailed_score.total_score}/{detailed_score.max_score}"
            }
        })
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
