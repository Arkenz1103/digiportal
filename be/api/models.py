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
    due_time = models.TimeField(null=True, blank=True)
    file_path = models.CharField(max_length=500, null=True, blank=True)
    scoring_criteria = models.TextField(null=True, blank=True)  # JSON string of criteria
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
    
    APPROVAL_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    activity = models.ForeignKey(PortfolioActivity, on_delete=models.CASCADE, related_name='submissions', null=True, blank=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    caption = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='submissions/%Y/%m/%d/', null=True, blank=True)  # Actual file storage
    file_path = models.TextField(null=True, blank=True)  # Keep for base64 compatibility
    file_type = models.CharField(max_length=50, null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    criteria_scores = models.TextField(null=True, blank=True)  # JSON string of criteria scores
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='unscored')
    post_to_feed = models.BooleanField(default=False)
    approval_status = models.CharField(max_length=50, choices=APPROVAL_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    scored_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'student_submissions'
    
    def __str__(self):
        activity_title = self.activity.title if self.activity else 'Sketch Pad'
        return f"{self.student.username} - {activity_title} ({self.status})"


class SubmissionScore(models.Model):
    """Detailed scoring criteria for student submissions"""
    submission = models.OneToOneField(StudentSubmission, on_delete=models.CASCADE, related_name='detailed_score')
    creativity_score = models.IntegerField(default=0)
    creativity_max = models.IntegerField(default=10)
    technical_skill_score = models.IntegerField(default=0)
    technical_skill_max = models.IntegerField(default=10)
    requirements_score = models.IntegerField(default=0)
    requirements_max = models.IntegerField(default=10)
    total_score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=30)
    scored_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='scored_submissions')
    scored_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'submission_scores'
    
    def __str__(self):
        return f"Score for {self.submission} - {self.total_score}/{self.max_score}"


class Sketch(models.Model):
    """Student sketch model for saving drawings"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sketches')
    title = models.CharField(max_length=255, default='Untitled Sketch')
    image_data = models.TextField()  # Base64 encoded image
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sketches'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.title}"


class NewsfeedPost(models.Model):
    """Newsfeed post model - separate from submissions so posts persist even if submission is deleted"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='newsfeed_posts')
    student_name = models.CharField(max_length=255)
    caption = models.TextField(blank=True, null=True)
    file_path = models.TextField(blank=True, null=True)  # Base64 encoded image/file
    file_type = models.CharField(max_length=50, default='image')
    activity_title = models.CharField(max_length=255, blank=True, null=True)
    activity_type = models.CharField(max_length=100, blank=True, null=True)
    
    # Optional reference to original submission (can be null if submission is deleted)
    original_submission = models.ForeignKey(
        'StudentSubmission', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='newsfeed_posts'
    )
    
    posted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'newsfeed_posts'
        ordering = ['-posted_at']
    
    def __str__(self):
        return f"{self.student_name} - {self.activity_title or 'Post'}"


class Remark(models.Model):
    """Remark model for teacher remarks to students"""
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='remarks_given')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='remarks_received')
    submission = models.ForeignKey('StudentSubmission', on_delete=models.CASCADE, related_name='remarks', null=True, blank=True)
    text = models.TextField()
    is_read = models.BooleanField(default=False)  # Kept for backward compatibility
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'remarks'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Remark from {self.teacher.username} to {self.student.username}"
    
    def is_read_by(self, user):
        """Check if this remark has been read by a specific user"""
        return RemarkReadStatus.objects.filter(remark=self, user=user).exists()


class RemarkReadStatus(models.Model):
    """Track which users have read which remarks"""
    remark = models.ForeignKey(Remark, on_delete=models.CASCADE, related_name='read_by')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='remarks_read')
    read_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'remark_read_status'
        unique_together = ['remark', 'user']  # Each user can only mark a remark as read once
        ordering = ['-read_at']
    
    def __str__(self):
        return f"{self.user.username} read remark {self.remark.id}"


class Notification(models.Model):
    """Notification model for user notifications"""
    NOTIFICATION_TYPES = [
        # Student notifications
        ('portfolio_created', 'Portfolio Created'),
        ('portfolio_updated', 'Portfolio Updated'),
        ('portfolio_deleted', 'Portfolio Deleted'),
        ('activity_created', 'Activity Created'),
        ('activity_updated', 'Activity Updated'),
        ('activity_deleted', 'Activity Deleted'),
        ('submission_approved', 'Submission Approved'),
        ('submission_rejected', 'Submission Rejected'),
        ('score_added', 'Score Added'),
        ('remark_added', 'Remark Added'),
        ('remark_updated', 'Remark Updated'),
        ('remark_deleted', 'Remark Deleted'),
        
        # Teacher notifications
        ('submission_received', 'Submission Received'),
        ('approval_requested', 'Approval Requested'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    
    # Optional references (SET_NULL so notifications persist after entity deletion)
    portfolio = models.ForeignKey(PortfolioFolder, on_delete=models.SET_NULL, null=True, blank=True)
    activity = models.ForeignKey(PortfolioActivity, on_delete=models.SET_NULL, null=True, blank=True)
    submission = models.ForeignKey(StudentSubmission, on_delete=models.SET_NULL, null=True, blank=True)
    remark = models.ForeignKey(Remark, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Metadata
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.recipient.username} - {self.title}"
