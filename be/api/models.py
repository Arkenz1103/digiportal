from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """Custom User model with role-based access"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    email = models.EmailField(unique=True)
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return f"{self.username} ({self.role})"


class LessonPlan(models.Model):
    """Lesson plan model for teachers"""
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_plans')
    title = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    path = models.CharField(max_length=500)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    uploaded_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lesson_plans'
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class PortfolioFolder(models.Model):
    """Portfolio folder model"""
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio_folders', db_column='teacher_id')
    name = models.CharField(max_length=255)
    class_name = models.CharField(max_length=255, default='General')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'portfolio_folders'
    
    def __str__(self):
        return f"{self.name} - {self.teacher.username}"


class PortfolioActivity(models.Model):
    """Portfolio activity model"""
    ACTIVITY_TYPE_CHOICES = [
        ('Quiz', 'Quiz'),
        ('Assignment', 'Assignment'),
        ('Project', 'Project'),
        ('Exam', 'Exam'),
        ('Presentation', 'Presentation'),
        ('Other', 'Other'),
    ]
    
    folder = models.ForeignKey(PortfolioFolder, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=100, choices=ACTIVITY_TYPE_CHOICES, default='Quiz')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    file_path = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'portfolio_activities'
    
    def __str__(self):
        return f"{self.title} ({self.activity_type}) - {self.folder.name}"


class StudentSubmission(models.Model):
    """Student submission model for portfolio activities"""
    STATUS_CHOICES = [
        ('unscored', 'Unscored'),
        ('scored', 'Scored'),
    ]
    
    activity = models.ForeignKey(PortfolioActivity, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    caption = models.TextField(null=True, blank=True)
    file_path = models.CharField(max_length=500, null=True, blank=True)
    file_type = models.CharField(max_length=50, null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='unscored')
    submitted_at = models.DateTimeField(auto_now_add=True)
    scored_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'student_submissions'
        unique_together = ['activity', 'student']  # One submission per student per activity
    
    def __str__(self):
        return f"{self.student.username} - {self.activity.title} ({self.status})"
