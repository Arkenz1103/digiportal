"""
Student Management API Views
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Avg, Count
from django.shortcuts import get_object_or_404
from .models import Student, User
from .serializer import StudentSerializer, StudentListSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing students
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['student_id', 'first_name', 'last_name', 'email']
    ordering_fields = ['student_id', 'last_name', 'grade_level', 'section', 'current_average']
    ordering = ['grade_level', 'section', 'last_name']
    
    def get_serializer_class(self):
        """Use lightweight serializer for list action"""
        if self.action == 'list':
            return StudentListSerializer
        return StudentSerializer
    
    def get_queryset(self):
        """Filter queryset based on user role and parameters"""
        queryset = super().get_queryset()
        user = self.request.user
        
        # Filter by grade level if provided
        grade_level = self.request.query_params.get('grade_level', None)
        if grade_level:
            queryset = queryset.filter(grade_level=grade_level)
        
        # Filter by section if provided
        section = self.request.query_params.get('section', None)
        if section:
            queryset = queryset.filter(section=section)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Filter by gender
        gender = self.request.query_params.get('gender', None)
        if gender:
            queryset = queryset.filter(gender=gender)
        
        # If user is a student, only show their own record
        if user.role == 'student':
            queryset = queryset.filter(user=user)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def by_grade_section(self, request):
        """Get students grouped by grade and section"""
        grade_level = request.query_params.get('grade_level')
        section = request.query_params.get('section')
        
        if not grade_level or not section:
            return Response(
                {'error': 'Both grade_level and section are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        students = self.get_queryset().filter(
            grade_level=grade_level,
            section=section
        )
        
        serializer = StudentListSerializer(students, many=True)
        
        return Response({
            'grade_level': grade_level,
            'section': section,
            'total_students': students.count(),
            'students': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get student statistics"""
        queryset = self.get_queryset()
        
        # Overall statistics
        total_students = queryset.count()
        active_students = queryset.filter(is_active=True).count()
        
        # Gender distribution
        male_count = queryset.filter(gender='M').count()
        female_count = queryset.filter(gender='F').count()
        
        # Grade level distribution
        grade_distribution = []
        for grade in range(1, 7):
            grade_data = {
                'grade': grade,
                'total': queryset.filter(grade_level=grade).count(),
                'section_a': queryset.filter(grade_level=grade, section='A').count(),
                'section_b': queryset.filter(grade_level=grade, section='B').count(),
            }
            grade_distribution.append(grade_data)
        
        # Academic performance
        avg_grade = queryset.aggregate(Avg('current_average'))['current_average__avg']
        avg_attendance = queryset.aggregate(Avg('attendance_percentage'))['attendance_percentage__avg']
        
        # Top performers (top 10)
        top_performers = queryset.filter(
            current_average__isnull=False
        ).order_by('-current_average')[:10]
        
        top_performers_data = StudentListSerializer(top_performers, many=True).data
        
        return Response({
            'total_students': total_students,
            'active_students': active_students,
            'inactive_students': total_students - active_students,
            'gender_distribution': {
                'male': male_count,
                'female': female_count
            },
            'grade_distribution': grade_distribution,
            'academic_performance': {
                'average_grade': round(avg_grade, 2) if avg_grade else 0,
                'average_attendance': round(avg_attendance, 2) if avg_attendance else 0
            },
            'top_performers': top_performers_data
        })
    
    @action(detail=True, methods=['post'])
    def update_grades(self, request, pk=None):
        """Update student's current average"""
        student = self.get_object()
        
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
        
        serializer = self.get_serializer(student)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_attendance(self, request, pk=None):
        """Update student's attendance percentage"""
        student = self.get_object()
        
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
        
        serializer = self.get_serializer(student)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Advanced search for students"""
        query = request.query_params.get('q', '')
        
        if not query:
            return Response(
                {'error': 'Search query is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Search in multiple fields
        students = self.get_queryset().filter(
            Q(student_id__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(guardian_name__icontains=query)
        )
        
        serializer = StudentListSerializer(students, many=True)
        
        return Response({
            'query': query,
            'count': students.count(),
            'results': serializer.data
        })
    
    @action(detail=False, methods=['post'])
    def bulk_update_section(self, request):
        """Bulk update section for multiple students"""
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
    
    @action(detail=False, methods=['get'])
    def export(self, request):
        """Export student data (simplified for now, can be extended to CSV/Excel)"""
        students = self.get_queryset()
        serializer = StudentSerializer(students, many=True)
        
        return Response({
            'total': students.count(),
            'data': serializer.data
        })
