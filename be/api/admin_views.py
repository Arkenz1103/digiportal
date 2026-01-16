"""
Admin Management API Views
"""
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import User, Classroom, SchoolYear, PortfolioActivity, StudentSubmission, StudentClassroomHistory


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_dashboard_api(request):
    """Get admin dashboard statistics"""
    if request.user.role != 'admin':
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Check if viewing a specific school year (archived)
        school_year_filter = request.query_params.get('school_year', None)
        
        if school_year_filter:
            # Viewing archived school year
            target_sy = SchoolYear.objects.filter(name=school_year_filter).first()
            if not target_sy:
                return Response({'error': 'School year not found'}, status=status.HTTP_404_NOT_FOUND)
            
            # Get all school years to calculate student ID ranges
            all_school_years_list = list(SchoolYear.objects.order_by('created_at').values_list('id', flat=True))
            try:
                sy_index = all_school_years_list.index(target_sy.id) + 1
            except ValueError:
                sy_index = 1
            
            # Classrooms for this school year
            classrooms = Classroom.objects.filter(school_year=school_year_filter)
            total_classrooms = classrooms.count()
            
            # Teachers assigned to classrooms in this school year
            total_teachers = classrooms.exclude(teacher__isnull=True).values('teacher').distinct().count()
            
            # Students based on ID number pattern
            min_prefix = (sy_index - 1) * 6 + 1
            max_prefix = sy_index * 6
            total_students = 0
            for prefix in range(min_prefix, max_prefix + 1):
                prefix_str = f"{prefix:03d}"
                total_students += User.objects.filter(role='student', id_number__startswith=prefix_str).count()
        else:
            # Current school year
            current_sy = SchoolYear.objects.filter(is_current=True, is_archived=False).first()
            
            if current_sy:
                current_classrooms = Classroom.objects.filter(school_year=current_sy.name, is_archived=False)
                total_classrooms = current_classrooms.count()
                total_students = User.objects.filter(role='student', classroom__school_year=current_sy.name).count()
                total_teachers = current_classrooms.exclude(teacher__isnull=True).values('teacher').distinct().count()
            else:
                total_students = 0
                total_teachers = User.objects.filter(role='teacher').count()
                total_classrooms = 0
        
        total_activities = PortfolioActivity.objects.count()
        total_submissions = StudentSubmission.objects.count()
        
        current_sy = SchoolYear.objects.filter(is_current=True, is_archived=False).first()
        recent_students = User.objects.filter(role='student').order_by('-date_joined')[:5]
        recent_teachers = User.objects.filter(role='teacher').order_by('-date_joined')[:5]
        
        return Response({
            'stats': {
                'total_students': total_students,
                'total_teachers': total_teachers,
                'total_classrooms': total_classrooms,
                'total_activities': total_activities,
                'total_submissions': total_submissions,
            },
            'current_school_year': {
                'id': current_sy.id,
                'name': current_sy.name,
            } if current_sy else None,
            'recent_students': [{
                'id': s.id,
                'name': f"{s.first_name} {s.last_name}".strip() or s.username,
                'id_number': s.id_number,
                'grade_level': s.grade_level,
                'date_joined': s.date_joined.isoformat(),
            } for s in recent_students],
            'recent_teachers': [{
                'id': t.id,
                'name': f"{t.first_name} {t.last_name}".strip() or t.username,
                'id_number': t.id_number,
                'date_joined': t.date_joined.isoformat(),
            } for t in recent_teachers],
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def admin_users_api(request):
    """GET: List all users, POST: Create a new user"""
    if request.user.role != 'admin':
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        try:
            role_filter = request.query_params.get('role', None)
            search = request.query_params.get('search', '')
            show_all = request.query_params.get('all', 'false').lower() == 'true'
            school_year_filter = request.query_params.get('school_year', None)
            
            users = User.objects.exclude(role='admin')
            
            if role_filter:
                users = users.filter(role=role_filter)
            
            if school_year_filter:
                # Viewing specific school year (archived)
                target_sy = SchoolYear.objects.filter(name=school_year_filter).first()
                if target_sy:
                    # Get all school years to calculate student ID ranges
                    all_school_years_list = list(SchoolYear.objects.order_by('created_at').values_list('id', flat=True))
                    try:
                        sy_index = all_school_years_list.index(target_sy.id) + 1
                    except ValueError:
                        sy_index = 1
                    
                    # Get classrooms for this school year
                    sy_classrooms = Classroom.objects.filter(school_year=school_year_filter)
                    
                    # Calculate student ID prefix range
                    min_prefix = (sy_index - 1) * 6 + 1
                    max_prefix = sy_index * 6
                    
                    # Build Q filter for students by ID prefix
                    from django.db.models import Q as DjangoQ
                    student_q = DjangoQ()
                    for prefix in range(min_prefix, max_prefix + 1):
                        prefix_str = f"{prefix:03d}"
                        student_q |= DjangoQ(role='student', id_number__startswith=prefix_str)
                    
                    # Teachers assigned to classrooms in this school year
                    teacher_q = DjangoQ(role='teacher', taught_classrooms__in=sy_classrooms)
                    
                    users = users.filter(student_q | teacher_q).distinct()
            elif not show_all:
                # Current school year
                current_sy = SchoolYear.objects.filter(is_current=True, is_archived=False).first()
                if current_sy:
                    current_classrooms = Classroom.objects.filter(school_year=current_sy.name, is_archived=False)
                    from django.db.models import Q as DjangoQ
                    users = users.filter(
                        DjangoQ(role='student', classroom__in=current_classrooms) |
                        DjangoQ(role='teacher', taught_classrooms__in=current_classrooms)
                    ).distinct()
            
            if search:
                users = users.filter(
                    Q(first_name__icontains=search) |
                    Q(last_name__icontains=search) |
                    Q(email__icontains=search) |
                    Q(id_number__icontains=search) |
                    Q(username__icontains=search)
                )
            
            users = users.order_by('role', 'last_name', 'first_name')
            
            users_data = []
            for user in users:
                # For teachers, get their assigned classroom
                assigned_classroom = None
                if user.role == 'teacher':
                    # If viewing archived, get classroom from that school year
                    if school_year_filter:
                        teacher_classroom = Classroom.objects.filter(teacher=user, school_year=school_year_filter).first()
                    else:
                        teacher_classroom = Classroom.objects.filter(teacher=user, is_archived=False).first()
                    if teacher_classroom:
                        assigned_classroom = {
                            'id': teacher_classroom.id,
                            'name': teacher_classroom.name,
                        }
                
                # For students viewing archived school year, get classroom history
                classroom_history = None
                if user.role == 'student' and school_year_filter:
                    history = StudentClassroomHistory.objects.filter(
                        student=user,
                        school_year=school_year_filter
                    ).first()
                    if history:
                        classroom_history = {
                            'classroom_name': history.classroom_name,
                            'grade_level': history.grade_level,
                            'section': history.section,
                            'teacher_name': history.teacher_name,
                            'joined_at': history.joined_at.isoformat() if history.joined_at else None,
                        }
                
                users_data.append({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'name': f"{user.first_name} {user.last_name}".strip() or user.username,
                    'role': user.role,
                    'id_number': user.id_number,
                    'grade_level': user.grade_level,
                    'section': user.section,
                    'classroom': {
                        'id': user.classroom.id,
                        'name': user.classroom.name,
                    } if user.classroom else None,
                    'assigned_classroom': assigned_classroom,  # For teachers
                    'classroom_history': classroom_history,  # For students in archived school year
                    'is_active': user.is_active,
                    'date_joined': user.date_joined.isoformat(),
                })
            
            return Response({'users': users_data, 'count': len(users_data)})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'POST':
        try:
            data = request.data
            role = data.get('role', 'student')
            first_name = data.get('first_name', '').strip()
            last_name = data.get('last_name', '').strip()
            email = data.get('email', '').strip()
            password = data.get('password', 'password123')
            grade_level = data.get('grade_level', None)
            
            if not first_name or not last_name:
                return Response({'error': 'First name and last name are required'}, status=status.HTTP_400_BAD_REQUEST)
            
            if not email:
                return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Generate username from email
            username = email.split('@')[0]
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            # Generate ID number based on role
            if role == 'student':
                if not grade_level:
                    return Response({'error': 'Grade level is required for students'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Check if a school year exists before creating students
                current_sy = SchoolYear.objects.filter(is_current=True, is_archived=False).first()
                if not current_sy:
                    return Response({'error': 'Please create a school year first before adding students'}, status=status.HTTP_400_BAD_REQUEST)
                
                id_number = User.generate_student_id(grade_level)
            elif role == 'teacher':
                id_number = User.generate_teacher_id()
            else:
                id_number = None
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=role,
                id_number=id_number,
                grade_level=str(grade_level) if grade_level else None,
            )
            
            return Response({
                'success': True,
                'message': f'{role.capitalize()} created successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'name': f"{user.first_name} {user.last_name}".strip(),
                    'role': user.role,
                    'id_number': user.id_number,
                    'grade_level': user.grade_level,
                },
                'default_password': password,
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def admin_user_detail_api(request, user_id):
    """GET: Get user details, PUT: Update user, DELETE: Delete user"""
    if request.user.role != 'admin':
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'name': f"{user.first_name} {user.last_name}".strip() or user.username,
            'role': user.role,
            'id_number': user.id_number,
            'grade_level': user.grade_level,
            'section': user.section,
            'classroom': {
                'id': user.classroom.id,
                'name': user.classroom.name,
            } if user.classroom else None,
            'is_active': user.is_active,
            'date_joined': user.date_joined.isoformat(),
        })
    
    elif request.method == 'PUT':
        try:
            data = request.data
            
            if 'first_name' in data:
                user.first_name = data['first_name'].strip()
            if 'last_name' in data:
                user.last_name = data['last_name'].strip()
            if 'email' in data:
                new_email = data['email'].strip()
                if new_email != user.email and User.objects.filter(email=new_email).exists():
                    return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
                user.email = new_email
            if 'is_active' in data:
                user.is_active = data['is_active']
            if 'password' in data and data['password']:
                user.set_password(data['password'])
            if 'grade_level' in data:
                user.grade_level = str(data['grade_level']) if data['grade_level'] else None
            
            user.save()
            
            return Response({
                'success': True,
                'message': 'User updated successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'name': f"{user.first_name} {user.last_name}".strip(),
                    'role': user.role,
                    'id_number': user.id_number,
                }
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'DELETE':
        try:
            if user.role == 'admin':
                return Response({'error': 'Cannot delete admin user'}, status=status.HTTP_400_BAD_REQUEST)
            
            username = user.username
            user.delete()
            
            return Response({'success': True, 'message': f'User {username} deleted successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def admin_classrooms_api(request):
    """GET: List all classrooms, POST: Create a new classroom"""
    if request.user.role != 'admin':
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        try:
            school_year_filter = request.query_params.get('school_year', None)
            include_archived = request.query_params.get('include_archived', 'false').lower() == 'true'
            
            classrooms = Classroom.objects.all()
            
            if not include_archived:
                classrooms = classrooms.filter(is_archived=False)
            
            if school_year_filter:
                classrooms = classrooms.filter(school_year=school_year_filter)
            
            classrooms = classrooms.order_by('grade_level', 'section')
            
            # Get school year index for student count calculation
            all_school_years_list = list(SchoolYear.objects.order_by('created_at').values_list('id', 'name'))
            sy_name_to_index = {name: idx + 1 for idx, (_, name) in enumerate(all_school_years_list)}
            
            classrooms_data = []
            for c in classrooms:
                # Calculate student count based on school year
                if c.is_archived:
                    # For archived classrooms, count students by ID prefix
                    sy_index = sy_name_to_index.get(c.school_year, 1)
                    grade_prefix = (sy_index - 1) * 6 + c.grade_level
                    prefix_str = f"{grade_prefix:03d}"
                    student_count = User.objects.filter(role='student', id_number__startswith=prefix_str).count()
                else:
                    student_count = c.student_count
                
                classrooms_data.append({
                    'id': c.id,
                    'name': c.name,
                    'grade_level': c.grade_level,
                    'section': c.section,
                    'school_year': c.school_year,
                    'class_code': c.class_code,
                    'teacher': {
                        'id': c.teacher.id,
                        'name': f"{c.teacher.first_name} {c.teacher.last_name}".strip() or c.teacher.username,
                    } if c.teacher else None,
                    'student_count': student_count,
                    'capacity': c.capacity,
                    'is_archived': c.is_archived,
                })
            
            return Response({'classrooms': classrooms_data, 'count': len(classrooms_data)})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'POST':
        try:
            data = request.data
            grade_level = data.get('grade_level')
            section = data.get('section', '').strip().upper()
            school_year = data.get('school_year', '')
            teacher_id = data.get('teacher_id', None)
            capacity = data.get('capacity', 30)
            
            if not grade_level or not section:
                return Response({'error': 'Grade level and section are required'}, status=status.HTTP_400_BAD_REQUEST)
            
            if not school_year:
                current_sy = SchoolYear.objects.filter(is_current=True, is_archived=False).first()
                if current_sy:
                    school_year = current_sy.name
                else:
                    return Response({'error': 'No active school year. Please create a school year first.'}, status=status.HTTP_400_BAD_REQUEST)
            
            name = f"Grade {grade_level} - {section}"
            if Classroom.objects.filter(name=name, school_year=school_year).exists():
                return Response({'error': f'Classroom {name} already exists for {school_year}'}, status=status.HTTP_400_BAD_REQUEST)
            
            teacher = None
            if teacher_id:
                try:
                    teacher = User.objects.get(id=teacher_id, role='teacher')
                except User.DoesNotExist:
                    return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
            
            classroom = Classroom.objects.create(
                name=name,
                grade_level=grade_level,
                section=section,
                school_year=school_year,
                teacher=teacher,
                capacity=capacity,
            )
            
            return Response({
                'success': True,
                'message': f'Classroom {classroom.name} created successfully',
                'classroom': {
                    'id': classroom.id,
                    'name': classroom.name,
                    'grade_level': classroom.grade_level,
                    'section': classroom.section,
                    'school_year': classroom.school_year,
                    'class_code': classroom.class_code,
                    'teacher': {
                        'id': teacher.id,
                        'name': f"{teacher.first_name} {teacher.last_name}".strip(),
                    } if teacher else None,
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def admin_assign_teacher_api(request, classroom_id):
    """Assign a teacher to a classroom"""
    if request.user.role != 'admin':
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        classroom = Classroom.objects.get(id=classroom_id)
        teacher_id = request.data.get('teacher_id')
        
        if teacher_id:
            teacher = User.objects.get(id=teacher_id, role='teacher')
            classroom.teacher = teacher
            classroom.save()
            
            return Response({
                'success': True,
                'message': f'Teacher {teacher.first_name} {teacher.last_name} assigned to {classroom.name}',
                'classroom': {
                    'id': classroom.id,
                    'name': classroom.name,
                    'teacher': {
                        'id': teacher.id,
                        'name': f"{teacher.first_name} {teacher.last_name}".strip(),
                    }
                }
            })
        else:
            classroom.teacher = None
            classroom.save()
            return Response({'success': True, 'message': f'Teacher removed from {classroom.name}'})
            
    except Classroom.DoesNotExist:
        return Response({'error': 'Classroom not found'}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def admin_school_years_api(request):
    """GET: List all school years, POST: Create a new school year"""
    if request.user.role != 'admin':
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        try:
            from .models import StudentClassroomHistory
            
            school_years = SchoolYear.objects.all().order_by('-created_at')
            all_school_years_list = list(SchoolYear.objects.order_by('created_at').values_list('id', flat=True))
            
            data = []
            for sy in school_years:
                classrooms = Classroom.objects.filter(school_year=sy.name)
                classrooms_count = classrooms.count()
                
                # Count teachers assigned to classrooms in this school year
                teachers_count = classrooms.exclude(teacher__isnull=True).values('teacher').distinct().count()
                
                # Count students based on their ID number pattern
                # Student IDs are BBBXXX where BBB = (school_year_num - 1) * 6 + grade_level
                # School Year 1: 001-006, School Year 2: 007-012, etc.
                try:
                    sy_index = all_school_years_list.index(sy.id) + 1  # 1-based index
                except ValueError:
                    sy_index = 1
                
                # Calculate the ID prefix range for this school year
                # SY1: 001-006, SY2: 007-012, SY3: 013-018
                min_prefix = (sy_index - 1) * 6 + 1  # e.g., SY1: 1, SY2: 7
                max_prefix = sy_index * 6  # e.g., SY1: 6, SY2: 12
                
                # Count students whose ID starts with prefixes in this range
                students_count = 0
                for prefix in range(min_prefix, max_prefix + 1):
                    prefix_str = f"{prefix:03d}"
                    students_count += User.objects.filter(
                        role='student',
                        id_number__startswith=prefix_str
                    ).count()
                
                data.append({
                    'id': sy.id,
                    'name': sy.name,
                    'is_current': sy.is_current,
                    'is_archived': sy.is_archived,
                    'archived_at': sy.archived_at.isoformat() if sy.archived_at else None,
                    'created_at': sy.created_at.isoformat(),
                    'classrooms_count': classrooms_count,
                    'teachers_count': teachers_count,
                    'students_count': students_count,
                })
            
            return Response({'school_years': data, 'count': len(data)})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'POST':
        try:
            data = request.data
            name = data.get('name', '').strip()
            
            if not name:
                return Response({'error': 'School year name is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            if SchoolYear.objects.filter(name=name).exists():
                return Response({'error': f'School year {name} already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Archive current school year if exists
            current_sy = SchoolYear.objects.filter(is_current=True, is_archived=False).first()
            if current_sy:
                current_sy.is_current = False
                current_sy.is_archived = True
                current_sy.archived_at = timezone.now()
                current_sy.save()
                
                # Get classrooms before archiving
                classrooms_to_archive = Classroom.objects.filter(school_year=current_sy.name, is_archived=False)
                
                # Save classroom history for all students before unassigning
                for classroom in classrooms_to_archive:
                    students_in_classroom = User.objects.filter(role='student', classroom=classroom)
                    teacher_name = f"{classroom.teacher.first_name} {classroom.teacher.last_name}".strip() if classroom.teacher else None
                    
                    for student in students_in_classroom:
                        # Check if history already exists
                        if not StudentClassroomHistory.objects.filter(student=student, school_year=current_sy.name).exists():
                            StudentClassroomHistory.objects.create(
                                student=student,
                                classroom=classroom,
                                school_year=current_sy.name,
                                grade_level=classroom.grade_level,
                                section=classroom.section,
                                classroom_name=classroom.name,
                                teacher_name=teacher_name,
                                joined_at=student.date_joined,
                            )
                
                # Archive classrooms
                classrooms_to_archive.update(
                    is_archived=True,
                    archived_at=timezone.now()
                )
                
                # Unassign students
                User.objects.filter(role='student', classroom__school_year=current_sy.name).update(
                    classroom=None,
                    grade_level=None,
                    section=None
                )
            
            new_sy = SchoolYear.objects.create(name=name, is_current=True)
            
            return Response({
                'success': True,
                'message': f'School year {name} created successfully',
                'school_year': {
                    'id': new_sy.id,
                    'name': new_sy.name,
                    'is_current': new_sy.is_current,
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def admin_archive_school_year_api(request, school_year_id):
    """Archive a school year"""
    if request.user.role != 'admin':
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        school_year = SchoolYear.objects.get(id=school_year_id)
        
        if school_year.is_archived:
            return Response({'error': 'School year is already archived'}, status=status.HTTP_400_BAD_REQUEST)
        
        school_year.is_current = False
        school_year.is_archived = True
        school_year.archived_at = timezone.now()
        school_year.save()
        
        # Get classrooms before archiving
        classrooms_to_archive = Classroom.objects.filter(school_year=school_year.name, is_archived=False)
        
        # Save classroom history for all students before unassigning
        for classroom in classrooms_to_archive:
            students_in_classroom = User.objects.filter(role='student', classroom=classroom)
            teacher_name = f"{classroom.teacher.first_name} {classroom.teacher.last_name}".strip() if classroom.teacher else None
            
            for student in students_in_classroom:
                # Check if history already exists
                if not StudentClassroomHistory.objects.filter(student=student, school_year=school_year.name).exists():
                    StudentClassroomHistory.objects.create(
                        student=student,
                        classroom=classroom,
                        school_year=school_year.name,
                        grade_level=classroom.grade_level,
                        section=classroom.section,
                        classroom_name=classroom.name,
                        teacher_name=teacher_name,
                        joined_at=student.date_joined,
                    )
        
        # Archive classrooms
        classrooms_to_archive.update(
            is_archived=True,
            archived_at=timezone.now()
        )
        
        # Unassign students
        User.objects.filter(role='student', classroom__school_year=school_year.name).update(
            classroom=None,
            grade_level=None,
            section=None
        )
        
        return Response({'success': True, 'message': f'School year {school_year.name} archived successfully'})
        
    except SchoolYear.DoesNotExist:
        return Response({'error': 'School year not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_teachers_list_api(request):
    """Get list of teachers for dropdown selection"""
    if request.user.role != 'admin':
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        teachers = User.objects.filter(role='teacher', is_active=True).order_by('last_name', 'first_name')
        
        data = []
        for t in teachers:
            assigned_classroom = Classroom.objects.filter(teacher=t, is_archived=False).first()
            
            data.append({
                'id': t.id,
                'name': f"{t.first_name} {t.last_name}".strip() or t.username,
                'id_number': t.id_number,
                'email': t.email,
                'assigned_classroom': {
                    'id': assigned_classroom.id,
                    'name': assigned_classroom.name,
                } if assigned_classroom else None,
            })
        
        return Response({'teachers': data, 'count': len(data)})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
